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
        # Si la respuesta es estructura (dict), devolver directamente JSON
        if isinstance(ai_response, dict):
            return ai_response
        # En caso contrario, envolver en campo texto
        return {"respuesta": ai_response, "context_summary": context_text[:1000]}
    except Exception as e:
        logging.error(f"Error en análisis OLAP: {e}")
        raise HTTPException(status_code=500, detail=str(e))
