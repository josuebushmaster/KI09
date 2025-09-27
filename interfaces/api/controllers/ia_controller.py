from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import sys
import os
from pathlib import Path

# Agregar el path del proyecto para importar grok_client si es necesario
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from scripts import grok_client
from application.use_cases.ia_cases.analyze_olap_use_case import AnalyzeOlapUseCase
import pandas as pd
import logging

# Configurar logger para IA
logger = logging.getLogger("IA_CONTROLLER")
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/ia", tags=["ia"])

class PromptRequest(BaseModel):
    prompt: str

@router.post("/analizar")
async def analyze_prompt(request: PromptRequest):
    """
    Recibe un prompt del frontend, construye contexto desde la BD OLAP
    (DataFrames/dicts) y lo envía junto al prompt al modelo de IA.
    """
    print(f"\n🤖 IA REQUEST: '{request.prompt}'")
    logger.info(f"IA Request recibida: {request.prompt}")
    
    try:
        context_text = None
        missing = []
        olap_tables_count = 0

        # Construir contexto desde la BD OLAP
        try:
            print("📊 EXTRAYENDO DATOS OLAP...")
            uc = AnalyzeOlapUseCase()
            uc_result = uc.run(request.prompt)
            context_text = uc_result.get('context_text')
            missing = uc_result.get('missing') or []
            olap_data = uc_result.get('olap_data') or {}
            
            # Contar tablas exitosas
            for name, val in olap_data.items():
                if isinstance(val, pd.DataFrame) and len(val) > 0:
                    olap_tables_count += 1
            
            if context_text and len(context_text) > 0:
                print(f"✅ CONTEXTO OLAP GENERADO: {len(context_text)} caracteres")
                print(f"📋 TABLAS CON DATOS: {olap_tables_count}")
                logger.info(f"Contexto OLAP construido: {len(context_text)} chars, {olap_tables_count} tablas")
            else:
                print("❌ ALERTA: CONTEXTO OLAP VACÍO")
                logger.warning("Contexto OLAP está vacío o None")
                
        except Exception as ctx_err:
            print(f"❌ ERROR EXTRAYENDO OLAP: {ctx_err}")
            logger.error(f"Error construyendo contexto OLAP: {ctx_err}")
            missing = [f"context_error:{ctx_err}"]

        # Llamar al modelo con prompt + contexto
        print("🧠 ENVIANDO A IA CON CONTEXTO...")
        result = grok_client.analyze_prompt(request.prompt, context_text=context_text)
        
        final_response = {
            "result": result,
            "missing": missing,
            "context_size": len(context_text) if context_text else 0,
        }
        
        print(f"✅ RESPUESTA IA COMPLETADA - Context size: {final_response['context_size']}")
        if missing:
            print(f"⚠️  MISSING DATA: {missing}")
            
        return final_response
        
    except Exception as e:
        print(f"❌ ERROR EN IA ENDPOINT: {e}")
        logger.error(f"Error en endpoint IA: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/context")
async def get_context(prompt: str | None = None):
    """
    Devuelve el contexto generado desde la BD OLAP para un prompt dado (o genérico).
    Útil para depurar si el modelo dice que no hay datos.
    """
    prompt = prompt or "diagnostico: generar contexto"
    print(f"\n🔍 DEBUG CONTEXT REQUEST: '{prompt}'")
    
    try:
        print("📊 EXTRAYENDO DATOS OLAP PARA DEBUG...")
        uc = AnalyzeOlapUseCase()
        uc_result = uc.run(prompt)
        context_text = uc_result.get('context_text') or ''
        olap_data = uc_result.get('olap_data') or {}
        missing = uc_result.get('missing') or []

        # Resumen por tabla
        tables_summary = {}
        tables_with_data = 0
        for name, val in olap_data.items():
            if isinstance(val, pd.DataFrame):
                try:
                    rows, cols = val.shape
                    if rows > 0:
                        tables_with_data += 1
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
        
        print(f"📋 TABLAS ENCONTRADAS: {len(tables_summary)}")
        print(f"📊 TABLAS CON DATOS: {tables_with_data}")
        print(f"📝 CONTEXTO SIZE: {len(context_text)} chars")
        if missing:
            print(f"⚠️  MISSING: {missing}")

        return {
            "prompt": prompt,
            "context_size": len(context_text),
            "missing": missing,
            "tables": tables_summary,
            "context_sample": context_text[:1200]  # muestra para inspección rápida
        }
    except Exception as e:
        print(f"❌ ERROR EN DEBUG CONTEXT: {e}")
        raise HTTPException(status_code=500, detail=str(e))
