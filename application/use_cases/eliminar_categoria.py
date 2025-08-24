from domain.repositories.categoria_repository import CategoriaRepository

class EliminarCategoriaUseCase:
    def __init__(self, categoria_repository: CategoriaRepository):
        self.categoria_repository = categoria_repository
    
    def execute(self, id_categoria: int) -> bool:
        return self.categoria_repository.eliminar(id_categoria)