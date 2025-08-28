from typing import Optional
from domain.entities.producto import Producto
from domain.repositories.producto_repository import ProductoRepository

class ActualizarProductoUseCase:
    def __init__(self, producto_repository: ProductoRepository):
        self.producto_repository = producto_repository

    def execute(self, id_producto: int, nombre_producto: str, precio: float, id_categoria: int) -> Optional[Producto]:
        producto = Producto(
            id_producto=id_producto,
            nombre_producto=nombre_producto,
            precio=precio,
            id_categoria=id_categoria
        )
        return self.producto_repository.actualizar(id_producto, producto)