from pydantic import BaseModel
from typing import Optional

class ProductoCreateDTO(BaseModel):
    nombre_producto: str
    precio: float
    costo: float
    id_categoria: int
    descripcion: str
    stock: int
    imagen_url: str

class ProductoUpdateDTO(BaseModel):
    nombre_producto: Optional[str] = None
    precio: Optional[float] = None
    costo: Optional[float] = None
    id_categoria: Optional[int] = None
    descripcion: Optional[str] = None
    stock: Optional[int] = None
    imagen_url: Optional[str] = None

class ProductoResponseDTO(BaseModel):
    id_producto: int
    nombre_producto: str
    precio: float
    costo: float
    id_categoria: int
    descripcion: str
    stock: int
    imagen_url: str
    