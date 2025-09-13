from pydantic import BaseModel
from typing import Optional


class ClienteCreateDTO(BaseModel):
    nombre: str
    apellido: str
    edad: int
    email: str
    telefono: str
    direccion: str

class ClienteUpdateDTO(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    edad: Optional[int] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ClienteResponseDTO(BaseModel):
    id_cliente: int
    nombre: str
    apellido: str
    edad: int
    email: str
    telefono: str
    direccion: str
