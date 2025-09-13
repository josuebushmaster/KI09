from domain.entities.orden_producto import OrdenProducto
from domain.repositories.orden_producto_repository import OrdenProductoRepository

class CrearOrdenProductoUseCase:
    def __init__(self, orden_producto_repository: OrdenProductoRepository):
        self.orden_producto_repository = orden_producto_repository

    def execute(self, id_producto: int, cantidad: int, precio_unitario: float, id_orden: int) -> OrdenProducto:
        orden_producto = OrdenProducto(
            id_producto=id_producto,
            cantidad=cantidad,
            precio_unitario=precio_unitario,
            id_orden=id_orden
        )
        return self.orden_producto_repository.crear(orden_producto)