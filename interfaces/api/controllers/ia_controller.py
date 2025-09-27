from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import sys
import os
import logging
from pathlib import Path

# Agregar el path del proyecto para importar grok_client si es necesario
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from scripts import grok_client
from application.use_cases.ia_cases.analyze_olap_use_case import AnalyzeOlapUseCase
import pandas as pd

# Configurar logger específico para IA
logger = logging.getLogger("ia_controller")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s [IA] %(levelname)s: %(message)s'))
    logger.addHandler(handler)

router = APIRouter(prefix="/ia", tags=["ia"])

class PromptRequest(BaseModel):
    prompt: str

@router.post("/analizar")
async def analyze_prompt(request: PromptRequest):
    """
    Recibe un prompt del frontend, construye contexto desde la BD OLAP
    (DataFrames/dicts) y lo envía junto al prompt al modelo de IA.
    """
    logger.info(f"🤖 INICIO - Pregunta IA: '{request.prompt[:100]}{'...' if len(request.prompt) > 100 else ''}'")
    
    try:
        context_text = None
        missing = []
        tables_info = {}

        # Construir contexto desde la BD OLAP
        logger.info("📊 EXTRAYENDO datos OLAP...")
        try:
            uc = AnalyzeOlapUseCase()
            uc_result = uc.run(request.prompt)
            context_text = uc_result.get('context_text')
            missing = uc_result.get('missing') or []
            olap_data = uc_result.get('olap_data') or {}
            
            # Analizar las tablas extraídas
            for name, val in olap_data.items():
                if isinstance(val, pd.DataFrame):
                    rows, cols = val.shape
                    tables_info[name] = {"rows": rows, "cols": cols}
                else:
                    tables_info[name] = {"error": str(val)}
            
            context_size = len(context_text) if context_text else 0
            logger.info(f"✅ CONTEXTO OLAP generado: {context_size} caracteres")
            
            # Mostrar resumen de tablas
            tablas_ok = [name for name, info in tables_info.items() if 'rows' in info and info['rows'] > 0]
            tablas_error = [name for name, info in tables_info.items() if 'error' in info]
            
            if tablas_ok:
                logger.info(f"📈 TABLAS CON DATOS: {len(tablas_ok)} -> {', '.join(tablas_ok[:5])}{'...' if len(tablas_ok) > 5 else ''}")
                total_rows = sum(info['rows'] for info in tables_info.values() if 'rows' in info)
                logger.info(f"📊 TOTAL FILAS DISPONIBLES: {total_rows}")
            
            if tablas_error:
                logger.warning(f"⚠️  TABLAS CON ERROR: {len(tablas_error)} -> {', '.join(tablas_error[:3])}")
                
            if missing:
                logger.warning(f"⚠️  DATOS FALTANTES: {missing}")
                
        except Exception as ctx_err:
            logger.error(f"❌ ERROR al extraer contexto OLAP: {ctx_err}")
            missing = [f"context_error:{ctx_err}"]
            context_text = None

        # Llamar al modelo con prompt + contexto
        if context_text:
            logger.info(f"🚀 ENVIANDO al LLM: prompt + contexto OLAP ({len(context_text)} chars)")
        else:
            logger.warning("⚠️  ENVIANDO al LLM: solo prompt (SIN contexto OLAP)")
            
        result = grok_client.analyze_prompt(request.prompt, context_text=context_text)
        
        # Verificar si el resultado indica uso del contexto
        result_str = str(result).lower()
        if context_text and any(keyword in result_str for keyword in ['no hay datos', 'no disponible', 'falta información']):
            logger.warning("⚠️  EL LLM DICE QUE NO HAY DATOS - Posible problema con el contexto")
        elif context_text:
            logger.info("✅ RESPUESTA LLM completada - Contexto OLAP fue utilizado")
        else:
            logger.info("✅ RESPUESTA LLM completada - Sin contexto OLAP")
            
        return {
            "result": result,
            "missing": missing,
            "context_size": len(context_text) if context_text else 0,
        }
    except Exception as e:
        logger.error(f"❌ ERROR GENERAL en endpoint IA: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/context")
async def get_context(prompt: str | None = None):
    """
    Devuelve el contexto generado desde la BD OLAP para un prompt dado (o genérico).
    Útil para depurar si el modelo dice que no hay datos.
    """
    try:
        prompt = prompt or "diagnostico: generar contexto"
        uc = AnalyzeOlapUseCase()
        uc_result = uc.run(prompt)
        context_text = uc_result.get('context_text') or ''
        olap_data = uc_result.get('olap_data') or {}
        missing = uc_result.get('missing') or []

        # Resumen por tabla
        tables_summary = {}
        for name, val in olap_data.items():
            if isinstance(val, pd.DataFrame):
                try:
                    rows, cols = val.shape
                except Exception:
                    rows, cols = None, None
                tables_summary[name] = {
                    "type": "dataframe",
                    "rows": rows,
                    "cols": cols,
                }
            elif isinstance(val, str):
                tables_summary[name] = {"type": "error", "message": val}
            else:
                tables_summary[name] = {"type": str(type(val))}

        return {
            "prompt": prompt,
            "context_size": len(context_text),
            "missing": missing,
            "tables": tables_summary,
            "context_sample": context_text[:1200]  # muestra para inspección rápida
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
