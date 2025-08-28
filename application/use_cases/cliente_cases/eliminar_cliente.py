from domain.repositories.cliente_repository import ClienteRepository

class EliminarClienteUseCase:
    def __init__(self, cliente_repository: ClienteRepository):
        self.cliente_repository = cliente_repository

    def execute(self, id_cliente: int) -> bool:
        return self.cliente_repository.eliminar(id_cliente)