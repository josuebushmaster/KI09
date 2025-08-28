from domain.entities.orden import Orden
from domain.repositories.orden_repository import OrdenRepository
from typing import List


class ListarOrdenesPorClienteUseCase:
    def __init__(self, orden_repository: OrdenRepository):
        self.orden_repository = orden_repository

    def execute(self, id_cliente: int) -> List[Orden]:
        return self.orden_repository.listar_por_cliente(id_cliente)
