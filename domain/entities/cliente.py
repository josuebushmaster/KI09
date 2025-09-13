from dataclasses import dataclass
from typing import Optional

@dataclass
class Cliente:
    id_cliente: Optional[int] = None
    nombre: str = ""
    apellido: str = ""
    edad: int = 0
    email: str = ""
    telefono: str = ""
    direccion: str = ""