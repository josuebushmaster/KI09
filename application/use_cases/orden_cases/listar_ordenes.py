from domain.entities.orden import Orden
from domain.repositories.orden_repository import OrdenRepository
from typing import List


class ListarOrdenesUseCase:
    def __init__(self, orden_repository: OrdenRepository):
        self.orden_repository = orden_repository

    def execute(self) -> List[Orden]:
        return self.orden_repository.listar_todos()
