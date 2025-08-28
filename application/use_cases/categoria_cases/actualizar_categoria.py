from typing import Optional
from domain.entities.categoria import Categoria
from domain.repositories.categoria_repository import CategoriaRepository

class ActualizarCategoriaUseCase:
    def __init__(self, categoria_repository: CategoriaRepository):
        self.categoria_repository = categoria_repository
    
    def execute(self, id_categoria: int, nombre_categoria: str, descripcion: str) -> Optional[Categoria]:
        categoria = Categoria(
            id_categoria=id_categoria,
            nombre_categoria=nombre_categoria,
            descripcion=descripcion
        )
        return self.categoria_repository.actualizar(id_categoria, categoria)