from abc import ABC, abstractmethod
from typing import List
from domain.entities.orden_producto import OrdenProducto

from typing import Optional

class OrdenProductoRepository(ABC):
    @abstractmethod
    def listar_todos(self) -> List[OrdenProducto]:
        pass
    @abstractmethod
    def crear(self, orden_producto: OrdenProducto) -> OrdenProducto:
        pass

    @abstractmethod
    def obtener_por_id(self, id_ordenProd: int) -> Optional[OrdenProducto]:
        pass

    @abstractmethod
    def listar_por_orden(self, id_orden: int) -> List[OrdenProducto]:
        pass

    @abstractmethod
    def actualizar(self, id_ordenProd: int, orden_producto: OrdenProducto) -> Optional[OrdenProducto]:
        pass

    @abstractmethod
    def eliminar(self, id_ordenProd: int) -> bool:
        pass
