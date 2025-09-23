
import os
import re
import json
import requests
import logging
from dotenv import load_dotenv

# Cargar .env si existe
load_dotenv()

API_URL = os.getenv('GROK_API_URL', 'https://api.groq.com/openai/v1/chat/completions')
API_KEY = os.getenv('GROKIA_API_KEY') or os.getenv('GROK_API_KEY')

# Logging local de peticiones/respuestas (no incluir claves)
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'grok_requests.log')
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s', handlers=[logging.FileHandler(log_file, encoding='utf-8')])

HEADERS = {
    "Content-Type": "application/json"
}
if API_KEY:
    HEADERS["Authorization"] = f"Bearer {API_KEY}"


def analyze_prompt(prompt: str, context_text: str = None) -> str:
    """
    Envía el prompt y el contexto OLAP a la API Grok.
    Si no hay API key disponible, devuelve una respuesta mock para pruebas locales.
    Registra la petición y la respuesta (sin keys) en `logs/grok_requests.log`.
    """
    # Preparar instrucciones claras para forzar el uso del contexto
    system_instructions = (
        "Usa exclusivamente la información proporcionada en el bloque CONTEXT para responder. "
        "Si falta información, indica qué datos adicionales se necesitan. Responde en lenguaje claro y con puntos concretos."
        "No hagas suposiciones fuera del contexto. Si el CONTEXT está vacío, indica que no hay datos disponibles."
    )

    # Incluir todo el contexto proporcionado sin truncar
    if context_text:
        full_content = (
            f"CONTEXT:\n{context_text}\n\nINSTRUCTIONS:\n{system_instructions}\n\nUSER QUESTION:\n{prompt}"
        )
    else:
        full_content = f"INSTRUCTIONS:\n{system_instructions}\n\nUSER QUESTION:\n{prompt}"

    # Instrucciones suaves: permitir un análisis extenso en texto pero exigir
    # que al final se incluya un bloque JSON valido con la estructura esperada.
    # Esto evita que el modelo se contenga por cumplir un formato estricto
    # y al mismo tiempo conserva la estructura machine-readable al final.
    system_json_instruction = (
        "Proporciona un análisis extenso y detallado usando la información del bloque CONTEXT. "
        "Primero entrega el análisis en lenguaje natural (múltiples párrafos, listas y ejemplos). "
        "Al final, incluye un bloque JSON delimitado con ```json ... ``` que contenga el resumen estructurado con las siguientes claves: \n"
        "- resumen: string con los hallazgos clave\n"
        "- tendencias: array de strings describiendo insights (añade números o porcentajes cuando sea posible)\n"
        "- recomendaciones: array de strings con acciones concretas\n"
        "- analysis_by_category: objeto con claves por categoría y un breve análisis\n"
        "- missing_fields: array de strings indicando datos faltantes\n"
        "- note: string con observaciones adicionales\n"
        "El bloque JSON debe ser válido y parsable; si falta información, Indícalo en 'missing_fields'. No limites la longitud del análisis en texto."
    )
    # Preparar mensajes para la API
    messages = [
        {"role": "system", "content": system_json_instruction},
        {"role": "user", "content": full_content}
    ]
    data = {"model": "llama-3.1-8b-instant", "messages": messages}

    # Registrar la petición (truncando el contenido si es muy largo)
    try:
        log_payload = {"model": data["model"], "messages": [messages[1]]}
        if len(full_content) > 5000:
            log_payload["messages"][0]["content"] = full_content[:5000] + '...'
        logging.info("Grok request payload: %s", json.dumps(log_payload, ensure_ascii=False))
    except Exception:
        logging.exception("Error logueando payload")

    # Si no hay API key, devolver mock para permitir pruebas locales
    if not API_KEY:
        mock_resp = f"MOCK_RESPONSE: recibí contexto de {len(context_text) if context_text else 0} chars; pregunta: {prompt[:200]}"
        logging.info("Grok mock response: %s", mock_resp)
        return mock_resp

    # Realizar la petición real
    try:
        response = requests.post(API_URL, headers=HEADERS, json=data, timeout=30)
        # Loggear la respuesta completa (texto), truncando si es muy larga
        resp_text = response.text
        to_log = resp_text if len(resp_text) < 5000 else resp_text[:5000] + '...'
        logging.info("Grok response (truncated): %s", to_log)

        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            content = result["choices"][0].get("message", {}).get("content") or result["choices"][0].get("text")
            # Intentar parsear JSON
            # Primero intentamos extraer un bloque JSON del contenido (maneja triple backticks y texto adicional)
            def _extract_json_from_text(text: str) -> str | None:
                if not text:
                    return None
                # Buscar bloque ```json ... ```
                m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
                if m:
                    return m.group(1)
                # Buscar cualquier bloque de triple backticks que contenga JSON
                m = re.search(r"```(?:.*?)?\s*(\{.*?\})\s*```", text, re.DOTALL)
                if m:
                    return m.group(1)
                # Buscar el primer objeto JSON basado en llaves balanceadas
                start = text.find('{')
                if start == -1:
                    return None
                stack = 0
                for i in range(start, len(text)):
                    ch = text[i]
                    if ch == '{':
                        stack += 1
                    elif ch == '}':
                        stack -= 1
                        if stack == 0:
                            return text[start:i+1]
                return None

            json_text = _extract_json_from_text(content)
            if json_text:
                try:
                    parsed = json.loads(json_text)
                    logging.info("Grok parsed JSON response (extracted): %s", parsed)
                    return parsed
                except Exception:
                    logging.exception("Error parseando JSON extraído, intentando parseo directo...")
            # Fallback: intentar parseo directo del content tal cual
            try:
                parsed = json.loads(content)
                logging.info("Grok parsed JSON response: %s", parsed)
                return parsed
            except Exception:
                logging.warning("Grok response no es JSON válido, retornando texto crudo.")
                return content
        logging.error("Grok API estructura inesperada: %s", result)
        return result
    except Exception as e:
        logging.exception("Error llamando a Grok API: %s", e)
        return {"error": str(e)}