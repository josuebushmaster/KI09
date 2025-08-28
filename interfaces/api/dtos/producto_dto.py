from pydantic import BaseModel
from typing import Optional

class ProductoCreateDTO(BaseModel):
    nombre_producto: str
    precio: float
    id_categoria: int

class ProductoUpdateDTO(BaseModel):
    nombre_producto: Optional[str] = None
    precio: Optional[float] = None
    id_categoria: Optional[int] = None

class ProductoResponseDTO(BaseModel):
    id_producto: int
    nombre_producto: str
    precio: float
    id_categoria:Optional[int] = None
    