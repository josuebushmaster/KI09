from typing import List
from domain.entities.orden_producto import OrdenProducto
from domain.repositories.orden_producto_repository import OrdenProductoRepository

class ListarTodosOrdenProductoUseCase:
    def __init__(self, orden_producto_repository: OrdenProductoRepository):
        self.orden_producto_repository = orden_producto_repository

    def execute(self) -> List[OrdenProducto]:
        return self.orden_producto_repository.listar_todos()
