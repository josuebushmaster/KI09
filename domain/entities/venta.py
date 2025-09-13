from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Venta:
    id_venta: Optional[int] = None
    id_orden: int = 0
    fecha_venta: datetime = datetime.utcnow()
    total_venta: float = 0.0
    metodo_pago: str = ""
