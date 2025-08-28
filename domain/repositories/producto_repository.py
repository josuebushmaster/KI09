from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.producto import Producto

class ProductoRepository(ABC):
    @abstractmethod
    def crear(self, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def obtener_por_id(self, id_producto: int) -> Optional[Producto]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Producto]:
        pass

    @abstractmethod
    def actualizar(self, id_producto: int, producto: Producto) -> Optional[Producto]:
        pass

    @abstractmethod
    def eliminar(self, id_producto: int) -> bool:
        pass