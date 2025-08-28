from domain.repositories.producto_repository import ProductoRepository

class EliminarProductoUseCase:
    def __init__(self, producto_repository: ProductoRepository):
        self.producto_repository = producto_repository

    def execute(self, id_producto: int) -> bool:
        return self.producto_repository.eliminar(id_producto)