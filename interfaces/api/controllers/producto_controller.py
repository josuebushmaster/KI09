import sys
import os
from pathlib import Path

# Obtener el directorio raíz del proyecto (4 niveles arriba desde este archivo)
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent

# Agregar el directorio raíz al path de Python
sys.path.append(str(project_root))

from fastapi import APIRouter, HTTPException, status
from application.use_cases.producto_cases.crear_producto import CrearProductoUseCase
from application.use_cases.producto_cases.obtener_producto import ObtenerProductoUseCase
from application.use_cases.producto_cases.listar_producto import ListarProductosUseCase
from application.use_cases.producto_cases.actualizar_producto import ActualizarProductoUseCase
from application.use_cases.producto_cases.eliminar_producto import EliminarProductoUseCase
from infrastructure.repositories.postgres_producto_repository import PostgresProductoRepository
from interfaces.api.dtos.producto_dto import ProductoCreateDTO, ProductoUpdateDTO, ProductoResponseDTO

router = APIRouter(prefix="/productos", tags=["productos"])

# Inyección de dependencias
producto_repository = PostgresProductoRepository()

@router.post("/", response_model=ProductoResponseDTO, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto_dto: ProductoCreateDTO):
    try:
        use_case = CrearProductoUseCase(producto_repository)
        producto = use_case.execute(
            producto_dto.nombre_producto,
            producto_dto.precio,
            producto_dto.id_categoria
        )
        return producto
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear producto: {str(e)}"
        )

@router.get("/{id_producto}", response_model=ProductoResponseDTO)
async def obtener_producto(id_producto: int):
    use_case = ObtenerProductoUseCase(producto_repository)
    producto = use_case.execute(id_producto)
    
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    return producto

@router.get("/", response_model=list[ProductoResponseDTO])
async def listar_productos():
    use_case = ListarProductosUseCase(producto_repository)
    return use_case.execute()

@router.put("/{id_producto}", response_model=ProductoResponseDTO)
async def actualizar_producto(id_producto: int, producto_dto: ProductoUpdateDTO):
    # Validar que al menos un campo sea proporcionado
    if (
        producto_dto.nombre_producto is None and
        producto_dto.precio is None and
        producto_dto.id_categoria is None
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se debe proporcionar al menos un campo para actualizar"
        )
    
    use_case = ActualizarProductoUseCase(producto_repository)
    producto_actualizado = use_case.execute(
        id_producto,
        producto_dto.nombre_producto or "",
        producto_dto.precio if producto_dto.precio is not None else 0.0,
        producto_dto.id_categoria if producto_dto.id_categoria is not None else 0
    )
    
    if not producto_actualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    return producto_actualizado

@router.delete("/{id_producto}", status_code=status.HTTP_200_OK)
async def eliminar_producto(id_producto: int):
    use_case = EliminarProductoUseCase(producto_repository)
    eliminado = use_case.execute(id_producto)
    
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )
    
    return {"mensaje": "Producto eliminado exitosamente"}