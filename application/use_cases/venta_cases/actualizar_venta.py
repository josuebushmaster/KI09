from typing import Optional
from domain.entities.venta import Venta
from domain.repositories.venta_repository import VentaRepository

class ActualizarVentaUseCase:
    def __init__(self, venta_repository: VentaRepository):
        self.venta_repository = venta_repository

    def execute(self, venta_id: int, venta_data: dict) -> Optional[Venta]:
        return self.venta_repository.actualizar(venta_id, venta_data)
