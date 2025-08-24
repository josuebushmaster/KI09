from pydantic import BaseModel
from typing import Optional

class CategoriaCreateDTO(BaseModel):
    nombre_categoria: str
    descripcion: str

class CategoriaUpdateDTO(BaseModel):
    nombre_categoria: Optional[str] = None
    descripcion: Optional[str] = None

class CategoriaResponseDTO(BaseModel):
    id_categoria: int
    nombre_categoria: str
    descripcion: str