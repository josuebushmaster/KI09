from domain.entities.orden import Orden
from domain.repositories.orden_repository import OrdenRepository
from typing import Optional


class ObtenerOrdenUseCase:
    def __init__(self, orden_repository: OrdenRepository):
        self.orden_repository = orden_repository

    def execute(self, id_orden: int) -> Optional[Orden]:
        return self.orden_repository.obtener_por_id(id_orden)
