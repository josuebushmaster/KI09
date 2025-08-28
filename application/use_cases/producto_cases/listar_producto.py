from typing import List
from domain.entities.producto import Producto
from domain.repositories.producto_repository import ProductoRepository

class ListarProductosUseCase:
    def __init__(self, producto_repository: ProductoRepository):
        self.producto_repository = producto_repository

    def execute(self) -> List[Producto]:
        return self.producto_repository.listar_todos()