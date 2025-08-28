from typing import Optional
from domain.entities.cliente import Cliente
from domain.repositories.cliente_repository import ClienteRepository

class ObtenerClienteUseCase:
    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self, id_cliente: int) -> Optional[Cliente]:
        return self.cliente_repository.obtener_por_id(id_cliente)