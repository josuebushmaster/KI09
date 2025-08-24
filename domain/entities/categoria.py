from dataclasses import dataclass
from typing import Optional

@dataclass
class Categoria:
    id_categoria: Optional[int] = None
    nombre_categoria: str = ""
    descripcion: str = ""