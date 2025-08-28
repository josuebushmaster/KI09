from domain.entities.categoria import Categoria
from domain.repositories.categoria_repository import CategoriaRepository

class CrearCategoriaUseCase:
    def __init__(self, categoria_repository: CategoriaRepository):
        self.categoria_repository = categoria_repository
    
    def execute(self, nombre_categoria: str, descripcion: str) -> Categoria:
        categoria = Categoria(nombre_categoria=nombre_categoria, descripcion=descripcion)
        return self.categoria_repository.crear(categoria)