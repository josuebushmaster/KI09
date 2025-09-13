from pydantic import BaseModel
from typing import Optional

class OrdenProductoCreateDTO(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: float
    id_orden: int

class OrdenProductoResponseDTO(BaseModel):
    id_ordenProd: int
    id_producto: int
    cantidad: int
    precio_unitario: float
    id_orden: int
