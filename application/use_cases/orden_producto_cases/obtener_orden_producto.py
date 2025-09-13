from typing import Optional
from domain.entities.orden_producto import OrdenProducto
from domain.repositories.orden_producto_repository import OrdenProductoRepository

class ObtenerOrdenProductoUseCase:
    def __init__(self, orden_producto_repository: OrdenProductoRepository):
        self.orden_producto_repository = orden_producto_repository

    def execute(self, id_ordenProd: int) -> Optional[OrdenProducto]:
        return self.orden_producto_repository.obtener_por_id(id_ordenProd)