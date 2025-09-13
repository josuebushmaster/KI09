from domain.entities.producto import Producto
from domain.repositories.producto_repository import ProductoRepository

class CrearProductoUseCase:
    def __init__(self, producto_repository: ProductoRepository):
        self.producto_repository = producto_repository

    def execute(self, nombre_producto: str, precio: float, costo: float, id_categoria: int, descripcion: str, stock: int, imagen_url: str) -> Producto:
        producto = Producto(
            nombre_producto=nombre_producto,
            precio=precio,
            costo=costo,
            id_categoria=id_categoria,
            descripcion=descripcion,
            stock=stock,
            imagen_url=imagen_url
        )
        return self.producto_repository.crear(producto)