
import os
import requests
from dotenv import load_dotenv

# Cargar .env si existe
load_dotenv()

API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = os.getenv('GROKIA_API_KEY') or os.getenv('GROK_API_KEY')
if not API_KEY:
    raise RuntimeError("GROKIA_API_KEY (o GROK_API_KEY) no encontrada en variables de entorno")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def analyze_prompt(prompt: str) -> str:
    data = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(API_URL, headers=HEADERS, json=data)
    try:
        result = response.json()
        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            raise RuntimeError(f"Error en la respuesta: {result}")
    except Exception as e:
        raise RuntimeError(f"No se pudo procesar la respuesta: {e}")