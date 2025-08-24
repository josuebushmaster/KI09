import sys
import os
from pathlib import Path

# Obtener el directorio raíz del proyecto (4 niveles arriba desde este archivo)
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent

# Agregar el directorio raíz al path de Python
sys.path.append(str(project_root))

from fastapi import APIRouter, HTTPException, status
from application.use_cases.crear_categoria import CrearCategoriaUseCase
from application.use_cases.obtener_categoria import ObtenerCategoriaUseCase
from application.use_cases.listar_categorias import ListarCategoriasUseCase
from application.use_cases.actualizar_categoria import ActualizarCategoriaUseCase
from application.use_cases.eliminar_categoria import EliminarCategoriaUseCase
from infrastructure.repositories.postgres_categoria_repository import PostgresCategoriaRepository
from interfaces.api.dtos.categoria_dto import CategoriaCreateDTO, CategoriaUpdateDTO, CategoriaResponseDTO

router = APIRouter(prefix="/categorias", tags=["categorias"])

# Inyección de dependencias
categoria_repository = PostgresCategoriaRepository()

@router.post("/", response_model=CategoriaResponseDTO, status_code=status.HTTP_201_CREATED)
async def crear_categoria(categoria_dto: CategoriaCreateDTO):
    try:
        use_case = CrearCategoriaUseCase(categoria_repository)
        categoria = use_case.execute(categoria_dto.nombre_categoria, categoria_dto.descripcion)
        return categoria
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear categoría: {str(e)}"
        )

@router.get("/{id_categoria}", response_model=CategoriaResponseDTO)
async def obtener_categoria(id_categoria: int):
    use_case = ObtenerCategoriaUseCase(categoria_repository)
    categoria = use_case.execute(id_categoria)
    
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    return categoria

@router.get("/", response_model=list[CategoriaResponseDTO])
async def listar_categorias():
    use_case = ListarCategoriasUseCase(categoria_repository)
    return use_case.execute()

@router.put("/{id_categoria}", response_model=CategoriaResponseDTO)
async def actualizar_categoria(id_categoria: int, categoria_dto: CategoriaUpdateDTO):
    # Validar que al menos un campo sea proporcionado
    if categoria_dto.nombre_categoria is None and categoria_dto.descripcion is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se debe proporcionar al menos un campo para actualizar"
        )
    
    use_case = ActualizarCategoriaUseCase(categoria_repository)
    categoria_actualizada = use_case.execute(
        id_categoria, 
        categoria_dto.nombre_categoria or "",
        categoria_dto.descripcion or ""
    )
    
    if not categoria_actualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    return categoria_actualizada

@router.delete("/{id_categoria}", status_code=status.HTTP_200_OK)
async def eliminar_categoria(id_categoria: int):
    use_case = EliminarCategoriaUseCase(categoria_repository)
    eliminada = use_case.execute(id_categoria)
    
    if not eliminada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    return {"mensaje": "Categoría eliminada exitosamente"}