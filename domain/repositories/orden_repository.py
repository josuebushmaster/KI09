from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.orden import Orden


class OrdenRepository(ABC):
    @abstractmethod
    def crear(self, orden: Orden) -> Orden:
        pass

    @abstractmethod
    def obtener_por_id(self, id_orden: int) -> Optional[Orden]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Orden]:
        pass

    @abstractmethod
    def listar_por_cliente(self, id_cliente: int) -> List[Orden]:
        pass

    @abstractmethod
    def listar_por_fecha(self, fecha_inicio, fecha_fin) -> List[Orden]:
        pass

    @abstractmethod
    def actualizar(self, id_orden: int, orden: Orden) -> Optional[Orden]:
        pass

    @abstractmethod
    def eliminar(self, id_orden: int) -> bool:
        pass
