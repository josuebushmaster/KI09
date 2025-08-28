from typing import List
from domain.entities.cliente import Cliente
from domain.repositories.cliente_repository import ClienteRepository

class ListarClientesUseCase:
    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self) -> List[Cliente]:
        return self.cliente_repository.listar_todos()