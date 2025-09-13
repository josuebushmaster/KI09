from typing import Optional
from domain.entities.venta import Venta
from domain.repositories.venta_repository import VentaRepository

class ObtenerVentaUseCase:
    def __init__(self, venta_repository: VentaRepository):
        self.venta_repository = venta_repository

    def execute(self, id_venta: int) -> Optional[Venta]:
        return self.venta_repository.obtener_por_id(id_venta)
