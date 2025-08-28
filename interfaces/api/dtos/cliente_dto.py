from pydantic import BaseModel
from typing import Optional


class ClienteCreateDTO(BaseModel):
    nombre: str
    apellido: str
    edad: int


class ClienteUpdateDTO(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    edad: Optional[int] = None


class ClienteResponseDTO(BaseModel):
    id_cliente: int
    nombre: str
    apellido: str
    edad: int
