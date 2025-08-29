import os
import traceback
from dotenv import load_dotenv

# Cargar .env del proyecto
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=project_root / '.env', verbose=False)

print('Usando .env en:', project_root / '.env')
print('DATABASE_URL=', os.getenv('RAILWAY_DATABASE_URL') or os.getenv('DATABASE_URL'))
print('DB_HOST=', os.getenv('DB_HOST'))

try:
    import sys
    # Asegurar que el directorio raíz del proyecto está en sys.path para poder importar paquetes
    if str(project_root) not in sys.path:
        sys.path.append(str(project_root))

    from infrastructure.database.railway_connection import get_railway_connection
except Exception as e:
    print('No se pudo importar get_railway_connection:', e)
    raise

try:
    conn = get_railway_connection()
    print('Conexión establecida:', conn)
    conn.close()
    print('Conexión cerrada correctamente')
except Exception as e:
    print('Error al conectar a Railway:')
    traceback.print_exc()
    raise
