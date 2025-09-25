from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
import os
from pathlib import Path
import logging

# Agregar el path del proyecto para importar módulos locales
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent
sys.path.append(str(project_root))

# Configuración de logging a archivo
log_dir = os.path.join(project_root, 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'olap_analysis.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.FileHandler(log_file, encoding='utf-8')]
)

from scripts import grok_client
from application.use_cases.ia_cases.analyze_olap_use_case import AnalyzeOlapUseCase
from application.use_cases.ia_cases.ai_response_verifier import verify_ai_response

router = APIRouter(prefix="/ia", tags=["ia"])


class PromptRequest(BaseModel):
    prompt: str


@router.post("/analizar")
async def analyze_prompt(request: PromptRequest):
    use_case = AnalyzeOlapUseCase()
    try:
        uc_result = use_case.run(request.prompt)
        olap_data = uc_result.get('olap_data', {})

        # Preparar líneas de log con cantidad de filas por tabla
        log_lines = ["--- FILAS POR TABLA OLAP ---"]
        for table, df in olap_data.items():
            if hasattr(df, 'shape'):
                log_lines.append(f"{table}: {df.shape[0]} filas")
            else:
                log_lines.append(f"{table}: {df}")
        log_lines.append("--- FIN FILAS POR TABLA ---\n")

        context_text = uc_result.get('context_text', '')
        log_lines.append("--- CONTEXTO ENVIADO A LA IA ---")
        log_lines.append(context_text[:2000])
        log_lines.append("--- FIN DEL CONTEXTO ---\n")

        # Escribir log
        logging.info('\n'.join(log_lines))

        # Llamar al cliente Grok con el contexto
        ai_response = grok_client.analyze_prompt(request.prompt, context_text=context_text)
        # Registrar la respuesta completa recibida del cliente Grok
        try:
            logging.info("AI raw response: %s", ai_response)
        except Exception:
            logging.exception("Error logueando respuesta AI")
        # Si la respuesta es estructura (dict), verificar heurísticamente contra olap_data
        re_evaluations = []
        if isinstance(ai_response, dict):
            verification = verify_ai_response(ai_response, olap_data)

            # Si no pasa la verificación, pedir re-evaluación automática hasta 2 veces
            max_retries = 2
            attempt = 0
            while not verification.get('verified', False) and attempt < max_retries:
                attempt += 1
                try:
                    follow_up_prompt = (
                        "Reevalua y corrige TU RESPUESTA PREVIA. "
                        "Se detectaron los siguientes issues: %s. "
                        "Usa exclusivamente el bloque CONTEXT enviado. Para cada afirmación numérica, "
                        "incluye el cálculo exacto (consulta/filtrado o agregación) y referencia a la tabla/columna/filas que la respaldan. "
                        "Si no puedes verificar una afirmación, indica claramente 'UNVERIFIABLE' para esa afirmación. "
                        "Responde primero con el análisis textual y al final agrega un bloque JSON con la misma estructura que antes (resumen, tendencias, recomendaciones, analysis_by_category, missing_fields, note)."
                    ) % (verification.get('issues') or [])

                    logging.info("Re-evaluación intento %d: enviando follow-up a la IA", attempt)
                    follow_resp = grok_client.analyze_prompt(follow_up_prompt, context_text=context_text)
                    # Volver a verificar
                    follow_ver = verify_ai_response(follow_resp if isinstance(follow_resp, dict) else {}, olap_data)
                    re_evaluations.append({"attempt": attempt, "ai_response": follow_resp, "verification": follow_ver})
                    # Si la re-evaluación pasó, reemplazar ai_response/verification por la versión verificada
                    if follow_ver.get('verified'):
                        ai_response = follow_resp
                        verification = follow_ver
                        break
                except Exception as e:
                    logging.exception("Error durante re-evaluación automática: %s", e)
                    re_evaluations.append({"attempt": attempt, "error": str(e)})

            return {"ai_response": ai_response, "verification": verification, "re_evaluations": re_evaluations}

        # En caso contrario, envolver en campo texto y marcar como no verificado
        return {"respuesta": ai_response, "verification": {"verified": False, "issues": ["response_not_structured"]}, "context_summary": context_text[:1000]}
    except Exception as e:
        logging.error(f"Error en análisis OLAP: {e}")
        raise HTTPException(status_code=500, detail=str(e))
