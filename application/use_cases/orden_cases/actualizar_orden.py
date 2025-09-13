from domain.entities.orden import Orden
from domain.repositories.orden_repository import OrdenRepository
from typing import Optional


class ActualizarOrdenUseCase:
    def __init__(self, orden_repository: OrdenRepository):
        self.orden_repository = orden_repository

    def execute(
        self,
        id_orden: int,
        id_cliente: int,
        fecha_orden,
        estado_orden: str,
        direccion_envio: str,
        total_orden: float,
        ciudad_envio: str,
        codigo_postal_envio: str,
        pais_envio: str,
        metodo_envio: str,
        costo_envio: float,
        estado_envio: str
    ) -> Optional[Orden]:
        orden = Orden(
            id_cliente=id_cliente,
            fecha_orden=fecha_orden,
            estado_orden=estado_orden,
            direccion_envio=direccion_envio,
            total_orden=total_orden,
            ciudad_envio=ciudad_envio,
            codigo_postal_envio=codigo_postal_envio,
            pais_envio=pais_envio,
            metodo_envio=metodo_envio,
            costo_envio=costo_envio,
            estado_envio=estado_envio
        )
        return self.orden_repository.actualizar(id_orden, orden)
