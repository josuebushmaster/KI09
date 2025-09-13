from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.venta import Venta

class VentaRepository(ABC):
    @abstractmethod
    def crear(self, venta: Venta) -> Venta:
        pass

    @abstractmethod
    def obtener_por_id(self, id_venta: int) -> Optional[Venta]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Venta]:
        pass

    @abstractmethod
    def actualizar(self, id_venta: int, venta: Venta) -> Optional[Venta]:
        pass

    @abstractmethod
    def eliminar(self, id_venta: int) -> bool:
        pass