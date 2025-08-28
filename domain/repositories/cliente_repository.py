from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.cliente import Cliente

class ClienteRepository(ABC):
    @abstractmethod
    def crear(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def obtener_por_id(self, id_cliente: int) -> Optional[Cliente]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Cliente]:
        pass

    @abstractmethod
    def actualizar(self, id_cliente: int, cliente: Cliente) -> Optional[Cliente]:
        pass

    @abstractmethod
    def eliminar(self, id_cliente: int) -> bool:
        pass