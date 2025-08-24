from typing import List
from domain.entities.categoria import Categoria
from domain.repositories.categoria_repository import CategoriaRepository

class ListarCategoriasUseCase:
    def __init__(self, categoria_repository: CategoriaRepository):
        self.categoria_repository = categoria_repository
    
    def execute(self) -> List[Categoria]:
        return self.categoria_repository.listar_todas()