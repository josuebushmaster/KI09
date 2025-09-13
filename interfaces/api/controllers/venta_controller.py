
import sys
import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, status
from application.use_cases.venta_cases.crear_venta import CrearVentaUseCase
from application.use_cases.venta_cases.obtener_venta import ObtenerVentaUseCase
from application.use_cases.venta_cases.listar_ventas import ListarVentasUseCase
from application.use_cases.venta_cases.actualizar_venta import ActualizarVentaUseCase
from application.use_cases.venta_cases.eliminar_venta import EliminarVentaUseCase
from infrastructure.repositories.postgres_venta_repository import PostgresVentaRepository
from interfaces.api.dtos.venta_dto import VentaCreateDTO, VentaUpdateDTO, VentaResponseDTO

router = APIRouter(prefix="/ventas", tags=["ventas"])

# Inyección de dependencias
venta_repository = PostgresVentaRepository()

@router.post("/", response_model=VentaResponseDTO, status_code=status.HTTP_201_CREATED)
async def crear_venta(venta_dto: VentaCreateDTO):
    try:
        use_case = CrearVentaUseCase(venta_repository)
        venta = use_case.execute(
            venta_dto.id_orden,
            venta_dto.fecha_venta,
            venta_dto.total_venta,
            venta_dto.metodo_pago
        )
        return venta
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear venta: {str(e)}"
        )

@router.get("/{id_venta}", response_model=VentaResponseDTO)
async def obtener_venta(id_venta: int):
    use_case = ObtenerVentaUseCase(venta_repository)
    venta = use_case.execute(id_venta)
    if not venta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )
    return venta

@router.get("/", response_model=list[VentaResponseDTO])
async def listar_ventas():
    use_case = ListarVentasUseCase(venta_repository)
    return use_case.execute()

@router.put("/{id_venta}", response_model=VentaResponseDTO)
async def actualizar_venta(id_venta: int, venta_dto: VentaUpdateDTO):
    if all(
        getattr(venta_dto, field) is None for field in [
            "id_orden", "fecha_venta", "total_venta", "metodo_pago"
        ]
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se debe proporcionar al menos un campo para actualizar"
        )
    use_case = ActualizarVentaUseCase(venta_repository)
    venta_actualizada = use_case.execute(
        id_venta,
        venta_dto.dict(exclude_unset=True)
    )
    if not venta_actualizada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )
    return venta_actualizada

@router.delete("/{id_venta}", status_code=status.HTTP_200_OK)
async def eliminar_venta(id_venta: int):
    use_case = EliminarVentaUseCase(venta_repository)
    eliminado = use_case.execute(id_venta)
    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada"
        )
    return {"mensaje": "Venta eliminada exitosamente"}
