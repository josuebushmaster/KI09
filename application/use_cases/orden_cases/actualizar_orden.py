from domain.entities.orden import Orden
from domain.repositories.orden_repository import OrdenRepository
from typing import Optional


class ActualizarOrdenUseCase:
    def __init__(self, orden_repository: OrdenRepository):
        self.orden_repository = orden_repository

    def execute(self, id_orden: int, id_cliente: Optional[int] = None, fecha_orden=None, estado_orden: Optional[str] = None) -> Optional[Orden]:
        # Construir objeto orden con los valores proporcionados (se asume que el repositorio maneja None si no aplica)
        orden = Orden(id_cliente=id_cliente or 0, fecha_orden=fecha_orden, estado_orden=estado_orden or "pendiente")
        return self.orden_repository.actualizar(id_orden, orden)
