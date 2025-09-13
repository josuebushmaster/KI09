from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Orden:
    id_orden: Optional[int] = None
    id_cliente: int = 0
    fecha_orden: datetime = datetime.utcnow()
    estado_orden: str = "pendiente"
    direccion_envio: str = ""
    total_orden: float = 0.0
    ciudad_envio: str = ""
    codigo_postal_envio: str = ""
    pais_envio: str = ""
    metodo_envio: str = ""
    costo_envio: float = 0.0
    estado_envio: str = ""
