instala las dependencias:

pip install fastapi uvicorn psycopg2-binary
o
pip install python-dotenv


------------------------------------------------------
Crear entorno virtual e instalar dependencias:

python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# o
.venv\Scripts\activate  # Windows
pip install -r requirements.txt


-----------------------------------------------------
Ejecutar run.py para correr el servidor

check_structure.py para ver que todos los __init__ esten en el proyecto


------------------------------------------------------
ejecutar limpiar_pycache.py para borrar todas las carpetas que se crean automaticamente:

# Ejecutar normalmente
python limpiar_pycache.py

# Modo silencioso
python limpiar_pycache.py --silent

# Solo ver qué se eliminaría (sin hacer cambios)
python limpiar_pycache.py --dry-run
