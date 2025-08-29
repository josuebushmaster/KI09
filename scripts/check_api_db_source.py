import os
from dotenv import load_dotenv
from pathlib import Path
import sys
import requests

project_root = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=project_root / '.env')
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from infrastructure.database.postgres_connection import get_db_connection

print('DATABASE_URL env=', os.getenv('RAILWAY_DATABASE_URL') or os.getenv('DATABASE_URL'))
print('DB_HOST env=', os.getenv('DB_HOST'))

# Probar conexión directa
try:
    conn = get_db_connection()
    print('Conexión directa OK:', conn)
    conn.close()
except Exception as e:
    print('Conexión directa ERROR:', e)

# Probar endpoint local (suponiendo que la app esté corriendo en 8000)
try:
    r = requests.get('http://127.0.0.1:8000/categorias/')
    print('GET /categorias/ ->', r.status_code)
    print('Respuesta:', r.text)
except Exception as e:
    print('No se pudo consultar la API local:', e)
