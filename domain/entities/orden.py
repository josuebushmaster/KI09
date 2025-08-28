from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Orden:
    id_orden: Optional[int] = None
    id_cliente: int = 0
    fecha_orden: datetime = datetime.utcnow()
    estado_orden: str = "pendiente"
