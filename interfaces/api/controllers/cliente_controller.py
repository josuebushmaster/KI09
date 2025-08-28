import sys
from pathlib import Path

# Asegurar que el root del proyecto esté en sys.path (coherente con otros controllers)
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent
sys.path.append(str(project_root))

from fastapi import APIRouter, HTTPException, status
from application.use_cases.cliente_cases.crear_cliente import CrearClienteUseCase
from application.use_cases.cliente_cases.obtener_cliente import ObtenerClienteUseCase
from application.use_cases.cliente_cases.listar_clientes import ListarClientesUseCase
from application.use_cases.cliente_cases.actualizar_cliente import ActualizarClienteUseCase
from application.use_cases.cliente_cases.eliminar_cliente import EliminarClienteUseCase
from infrastructure.repositories.postgres_cliente_repository import PostgresClienteRepository
from interfaces.api.dtos.cliente_dto import (
    ClienteCreateDTO,
    ClienteUpdateDTO,
    ClienteResponseDTO
)

router = APIRouter(prefix="/clientes", tags=["clientes"])

# Inyección de dependencia simple
cliente_repository = PostgresClienteRepository()


@router.post("/", response_model=ClienteResponseDTO, status_code=status.HTTP_201_CREATED)
async def crear_cliente(cliente_dto: ClienteCreateDTO):
    try:
        use_case = CrearClienteUseCase(cliente_repository)
        cliente = use_case.execute(cliente_dto.nombre, cliente_dto.apellido, cliente_dto.edad)
        return cliente
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{id_cliente}", response_model=ClienteResponseDTO)
async def obtener_cliente(id_cliente: int):
    use_case = ObtenerClienteUseCase(cliente_repository)
    cliente = use_case.execute(id_cliente)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return cliente


@router.get("/", response_model=list[ClienteResponseDTO])
async def listar_clientes():
    use_case = ListarClientesUseCase(cliente_repository)
    return use_case.execute()


@router.put("/{id_cliente}", response_model=ClienteResponseDTO)
async def actualizar_cliente(id_cliente: int, cliente_dto: ClienteUpdateDTO):
    # Validar al menos un campo
    if cliente_dto.nombre is None and cliente_dto.apellido is None and cliente_dto.edad is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Se debe proporcionar al menos un campo para actualizar")

    use_case = ActualizarClienteUseCase(cliente_repository)
    cliente_actualizado = use_case.execute(
        id_cliente,
        cliente_dto.nombre or "",
        cliente_dto.apellido or "",
        cliente_dto.edad if cliente_dto.edad is not None else 0
    )

    if not cliente_actualizado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")

    return cliente_actualizado


@router.delete("/{id_cliente}", status_code=status.HTTP_200_OK)
async def eliminar_cliente(id_cliente: int):
    use_case = EliminarClienteUseCase(cliente_repository)
    eliminado = use_case.execute(id_cliente)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return {"mensaje": "Cliente eliminado exitosamente"}
