from typing import Optional
from domain.entities.orden_producto import OrdenProducto
from domain.repositories.orden_producto_repository import OrdenProductoRepository

class ActualizarOrdenProductoUseCase:
    def __init__(self, orden_producto_repository: OrdenProductoRepository):
        self.orden_producto_repository = orden_producto_repository

    def execute(self, id_ordenProd: int, orden_producto: OrdenProducto) -> Optional[OrdenProducto]:
        return self.orden_producto_repository.actualizar(id_ordenProd, orden_producto)