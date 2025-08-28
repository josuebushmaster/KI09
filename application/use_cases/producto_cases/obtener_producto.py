from typing import Optional
from domain.entities.producto import Producto   
from domain.repositories.producto_repository import ProductoRepository

class ObtenerProductoUseCase:
    def __init__(self, producto_repository: ProductoRepository):
        self.producto_repository = producto_repository

    def execute(self, id_producto: int) -> Optional[Producto]:
        return self.producto_repository.obtener_por_id(id_producto)