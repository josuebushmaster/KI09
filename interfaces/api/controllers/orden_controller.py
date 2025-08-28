import sys
from pathlib import Path

# Asegurar import path al root del proyecto
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent.parent.parent
sys.path.append(str(project_root))

from fastapi import APIRouter, HTTPException, status
from infrastructure.repositories.postgres_orden_repository import PostgresOrdenRepository
from application.use_cases.orden_cases.crear_orden import CrearOrdenUseCase
from application.use_cases.orden_cases.obtener_orden import ObtenerOrdenUseCase
from application.use_cases.orden_cases.listar_por_cliente import ListarOrdenesPorClienteUseCase
from application.use_cases.orden_cases.listar_ordenes import ListarOrdenesUseCase
from application.use_cases.orden_cases.actualizar_orden import ActualizarOrdenUseCase
from application.use_cases.orden_cases.eliminar_orden import EliminarOrdenUseCase
from application.use_cases.orden_cases.listar_por_fecha import ListarOrdenesPorFechaUseCase
from datetime import datetime
from interfaces.api.dtos.orden_dto import (
    OrdenCreateDTO,
    OrdenUpdateDTO,
    OrdenResponseDTO
)

router = APIRouter(prefix="/ordenes", tags=["ordenes"])

# Inyección simple
orden_repository = PostgresOrdenRepository()


@router.post("/", response_model=OrdenResponseDTO, status_code=status.HTTP_201_CREATED)
async def crear_orden(orden_dto: OrdenCreateDTO):
    try:
        use_case = CrearOrdenUseCase(orden_repository)
        orden = use_case.execute(orden_dto.id_cliente, orden_dto.fecha_orden, orden_dto.estado_orden)
        return orden
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{id_orden}", response_model=OrdenResponseDTO)
async def obtener_orden(id_orden: int):
    use_case = ObtenerOrdenUseCase(orden_repository)
    orden = use_case.execute(id_orden)
    if not orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return orden


@router.get("/cliente/{id_cliente}", response_model=list[OrdenResponseDTO])
async def listar_ordenes_por_cliente(id_cliente: int):
    use_case = ListarOrdenesPorClienteUseCase(orden_repository)
    return use_case.execute(id_cliente)


@router.get("/", response_model=list[OrdenResponseDTO])
async def listar_ordenes():
    use_case = ListarOrdenesUseCase(orden_repository)
    return use_case.execute()


@router.get("/reportes", response_model=list[OrdenResponseDTO])
async def reportes_ordenes(fecha_inicio: datetime, fecha_fin: datetime):
    # Ambos parámetros son obligatorios y FastAPI los parseará como datetime
    if fecha_inicio is None or fecha_fin is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="fecha_inicio y fecha_fin son requeridos")

    use_case = ListarOrdenesPorFechaUseCase(orden_repository)
    return use_case.execute(fecha_inicio, fecha_fin)


@router.put("/{id_orden}", response_model=OrdenResponseDTO)
async def actualizar_orden(id_orden: int, orden_dto: OrdenUpdateDTO):
    # Validar al menos un campo
    if orden_dto.id_cliente is None and orden_dto.fecha_orden is None and orden_dto.estado_orden is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Se debe proporcionar al menos un campo para actualizar")

    use_case = ActualizarOrdenUseCase(orden_repository)
    orden_actualizada = use_case.execute(
        id_orden,
        id_cliente=orden_dto.id_cliente,
        fecha_orden=orden_dto.fecha_orden,
        estado_orden=orden_dto.estado_orden
    )

    if not orden_actualizada:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")

    return orden_actualizada


@router.delete("/{id_orden}", status_code=status.HTTP_200_OK)
async def eliminar_orden(id_orden: int):
    use_case = EliminarOrdenUseCase(orden_repository)
    eliminado = use_case.execute(id_orden)
    if not eliminado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    return {"mensaje": "Orden eliminada exitosamente"}
