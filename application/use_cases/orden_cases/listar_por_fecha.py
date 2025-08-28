from domain.entities.orden import Orden
from domain.repositories.orden_repository import OrdenRepository
from typing import List


class ListarOrdenesPorFechaUseCase:
    def __init__(self, orden_repository: OrdenRepository):
        self.orden_repository = orden_repository

    def execute(self, fecha_inicio, fecha_fin) -> List[Orden]:
        return self.orden_repository.listar_por_fecha(fecha_inicio, fecha_fin)
