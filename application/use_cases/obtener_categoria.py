from typing import Optional
from domain.entities.categoria import Categoria
from domain.repositories.categoria_repository import CategoriaRepository

class ObtenerCategoriaUseCase:
    def __init__(self, categoria_repository: CategoriaRepository):
        self.categoria_repository = categoria_repository
    
    def execute(self, id_categoria: int) -> Optional[Categoria]:
        return self.categoria_repository.obtener_por_id(id_categoria)