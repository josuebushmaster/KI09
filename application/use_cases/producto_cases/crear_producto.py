from domain.entities.producto import Producto
from domain.repositories.producto_repository import ProductoRepository

class CrearProductoUseCase:
    def __init__(self, producto_repository: ProductoRepository):
        self.producto_repository = producto_repository

    def execute(self, nombre_producto: str, precio: float, id_categoria: int) -> Producto:
        producto = Producto(nombre_producto=nombre_producto, id_categoria=id_categoria, precio=precio)
        return self.producto_repository.crear(producto)