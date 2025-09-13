from typing import List
from domain.entities.venta import Venta
from domain.repositories.venta_repository import VentaRepository

class ListarVentasUseCase:
    def __init__(self, venta_repository: VentaRepository):
        self.venta_repository = venta_repository

    def execute(self) -> List[Venta]:
        return self.venta_repository.listar_todos()
