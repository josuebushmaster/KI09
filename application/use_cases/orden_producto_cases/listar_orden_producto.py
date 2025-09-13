from typing import List
from domain.entities.orden_producto import OrdenProducto
from domain.repositories.orden_producto_repository import OrdenProductoRepository

class ListarOrdenProductosPorOrdenUseCase:
    def __init__(self, orden_producto_repository: OrdenProductoRepository):
        self.orden_producto_repository = orden_producto_repository

    def execute(self, id_orden: int) -> List[OrdenProducto]:
        return self.orden_producto_repository.listar_por_orden(id_orden)