import sys
import os
from pathlib import Path

# Obtener el directorio raíz del proyecto (3 niveles arriba desde este archivo)
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent

# Agregar el directorio raíz al path de Python
sys.path.append(str(project_root))

print(f"Directorio raíz agregado: {project_root}")

from fastapi import FastAPI
from interfaces.api.controllers.categoria_controller import router as categorias_router
from interfaces.api.controllers.producto_controller import router as productos_router
from interfaces.api.controllers.cliente_controller import router as clientes_router


app = FastAPI(
    title="API de Categorías",
    description="API para gestionar categorías con Clean Architecture",
    version="1.0.0"
)

# Incluir rutas
app.include_router(categorias_router)
app.include_router(productos_router)
app.include_router(clientes_router)
@app.get("/")
async def root():
    return {"mensaje": "API de Categorías funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)