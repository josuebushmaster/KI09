
import os
import requests
from dotenv import load_dotenv

# Cargar .env si existe
import os
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


def analyze_prompt(prompt: str, context_text: str = None, max_context_chars: int = 15000) -> str:
    """
    Envía el prompt y el contexto OLAP a la API Grok.
    Si no hay API key disponible, devuelve una respuesta mock para pruebas locales.
    Registra la petición y la respuesta (sin keys) en `logs/grok_requests.log`.
    """
    # Preparar instrucciones claras para forzar el uso del contexto
    system_instructions = (
        "Usa exclusivamente la información proporcionada en el bloque CONTEXT para responder. "
        "Si falta información, indica qué datos adicionales se necesitan. Responde en lenguaje claro y con "
        "puntos concretos (máximo 8 ítems)."
    )

    if context_text:
        if len(context_text) > max_context_chars:
            context_text = context_text[:max_context_chars]
        full_content = (
            f"CONTEXT:\n{context_text}\n\nINSTRUCTIONS:\n{system_instructions}\n\nUSER QUESTION:\n{prompt}"
        )
    else:
        full_content = f"INSTRUCTIONS:\n{system_instructions}\n\nUSER QUESTION:\n{prompt}"

    # Instrucciones al sistema para salida JSON estructurada
    system_json_instruction = (
        "Responde exclusivamente en formato JSON con las claves: \n"
        "- resumen: string breve\n"
        "- tendencias: array de strings\n"
        "- recomendaciones: array de strings\n"
        "- missing_fields: array de strings indicando campos/tables faltantes (si aplica)\n"
        "- note: string con aclaraciones opcionales\n"
        "Si el contexto no contiene los campos solicitados para el análisis (por ejemplo ventas por cliente en enero 2024), no rehúyas: realiza el mejor análisis posible usando los datos disponibles y en 'missing_fields' lista lo que falta. Devuelve únicamente JSON válido, sin texto adicional."
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