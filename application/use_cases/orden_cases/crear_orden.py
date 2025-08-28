from domain.entities.orden import Orden
from domain.repositories.orden_repository import OrdenRepository


class CrearOrdenUseCase:
    def __init__(self, orden_repository: OrdenRepository):
        self.orden_repository = orden_repository

    def execute(self, id_cliente: int, fecha_orden=None, estado_orden: str = "pendiente") -> Orden:
        orden = Orden(id_cliente=id_cliente, fecha_orden=fecha_orden, estado_orden=estado_orden)
        return self.orden_repository.crear(orden)
