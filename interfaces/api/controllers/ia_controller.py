from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import sys
import os
from pathlib import Path

# Agregar el path del proyecto para importar grok_client
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent
sys.path.append(str(project_root))

from scripts import grok_client

router = APIRouter(prefix="/ia", tags=["ia"])

class PromptRequest(BaseModel):
    prompt: str

@router.post("/analizar")
async def analyze_prompt(request: PromptRequest):
    try:
        result = grok_client.analyze_prompt(request.prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
