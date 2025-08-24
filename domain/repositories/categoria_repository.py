from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.categoria import Categoria

class CategoriaRepository(ABC):
    @abstractmethod
    def crear(self, categoria: Categoria) -> Categoria:
        pass
    
    @abstractmethod
    def obtener_por_id(self, id_categoria: int) -> Optional[Categoria]:
        pass
    
    @abstractmethod
    def listar_todas(self) -> List[Categoria]:
        pass
    
    @abstractmethod
    def actualizar(self, id_categoria: int, categoria: Categoria) -> Optional[Categoria]:
        pass
    
    @abstractmethod
    def eliminar(self, id_categoria: int) -> bool:
        pass