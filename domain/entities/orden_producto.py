from dataclasses import dataclass
from typing import Optional

@dataclass
class OrdenProducto:
    id_ordenProd: Optional[int] = None
    id_producto: int = 0
    cantidad: int = 0
    precio_unitario: float = 0.0
    id_orden: int = 0
