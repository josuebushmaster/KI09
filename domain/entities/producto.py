from dataclasses import dataclass
from typing import Optional

@dataclass
class Producto:
    id_producto: Optional[int] = None
    nombre_producto: str = ""
    precio: float = 0.0
    id_categoria: int = 0