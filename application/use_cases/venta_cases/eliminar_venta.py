from typing import Optional
from domain.entities.venta import Venta
from domain.repositories.venta_repository import VentaRepository

class EliminarVentaUseCase:
    def __init__(self, venta_repository: VentaRepository):
        self.venta_repository = venta_repository

    def execute(self, venta_id: int) -> Optional[Venta]:
        return self.venta_repository.eliminar(venta_id)
