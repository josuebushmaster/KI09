# run.py
import sys
import os

# Agregar el directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

print(f"Directorio actual: {current_dir}")
print(f"Sys.path actualizado")

# Verificar si los módulos existen
try:
    from interfaces.api.main import app
    print("✓ Módulo interfaces.api.main importado correctamente")
except ImportError as e:
    print(f"✗ Error importando interfaces.api.main: {e}")
    print("Verifica que existan los archivos __init__.py")
    exit(1)

import uvicorn

if __name__ == "__main__":
    print("Iniciando servidor API...")
    uvicorn.run(app, host="0.0.0.0", port=8000)