import sys
import os
from pathlib import Path

# Obtener el directorio raíz del proyecto (3 niveles arriba desde este archivo)
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent

# Agregar el directorio raíz al path de Python
sys.path.append(str(project_root))

print(f"Directorio raíz agregado: {project_root}")
from dotenv import load_dotenv

# Cargar variables de entorno desde el .env del proyecto lo antes posible
load_dotenv(dotenv_path=project_root / '.env', verbose=True)

from fastapi import FastAPI
from interfaces.api.controllers.categoria_controller import router as categorias_router
from interfaces.api.controllers.producto_controller import router as productos_router
from interfaces.api.controllers.cliente_controller import router as clientes_router
from interfaces.api.controllers.orden_controller import router as ordenes_router
from infrastructure.database.postgres_connection import get_db_connection


app = FastAPI(
    title="API de Categorías",
    description="API para gestionar categorías con Clean Architecture",
    version="1.0.0"
)

# Incluir rutas
app.include_router(categorias_router)
app.include_router(productos_router)
app.include_router(clientes_router)
app.include_router(ordenes_router)
@app.get("/")
async def root():
    return {"mensaje": "API de Categorías funcionando correctamente"}


@app.on_event("startup")
def startup_event():
    # Mostrar qué variables de entorno se están usando para la DB
    db_url = os.getenv('RAILWAY_DATABASE_URL') or os.getenv('DATABASE_URL')
    db_host = os.getenv('DB_HOST')
    print('Startup: DATABASE_URL=', db_url)
    print('Startup: DB_HOST=', db_host)
    # Probar conexión rápida para verificar origen de datos
    try:
        conn = get_db_connection()
        conn.close()
        print('Startup: conexión a DB OK')
    except Exception as e:
        import traceback
        traceback.print_exc()
        print('Startup: advertencia — no se pudo conectar a la DB (la app seguirá funcionando)')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)