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

prompt = """Analiza la siguiente información financiera:
Enero: ingresos 1000, gastos 500
Febrero: ingresos 1200, gastos 700
Marzo: ingresos 900, gastos 400
"""

data = {
    "model": "llama-3.1-8b-instant", 
    "messages": [
        {"role": "user", "content": prompt}
    ]
}

response = requests.post(API_URL, headers=HEADERS, json=data)

# Primero mostramos toda la respuesta
print("Respuesta cruda:", response.text)

try:
    result = response.json()
    if "choices" in result:
        print("\nRespuesta del modelo:\n")
        print(result["choices"][0]["message"]["content"])
    else:
        print("Error en la respuesta:", result)
except Exception as e:
    print("No se pudo procesar la respuesta:", e)