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

    def disminuir_stock(self, id_producto: int, cantidad: int, conn=None) -> bool:
        """Disminuye el stock del producto en la cantidad especificada.
        Si se proporciona `conn`, usa esa conexión (no hace commit/rollback);
        si no, abrirá su propia conexión y la manejará.
        Retorna True si se actualizó el stock (suficiente stock), False si no.
        """
        raise NotImplementedError()