from domain.repositories.orden_producto_repository import OrdenProductoRepository

class EliminarOrdenProductoUseCase:
    def __init__(self, orden_producto_repository: OrdenProductoRepository):
        self.orden_producto_repository = orden_producto_repository

    def execute(self, id_ordenProd: int) -> bool:
        return self.orden_producto_repository.eliminar(id_ordenProd)