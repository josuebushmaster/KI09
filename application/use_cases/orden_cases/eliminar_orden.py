from domain.repositories.orden_repository import OrdenRepository


class EliminarOrdenUseCase:
    def __init__(self, orden_repository: OrdenRepository):
        self.orden_repository = orden_repository

    def execute(self, id_orden: int) -> bool:
        return self.orden_repository.eliminar(id_orden)
