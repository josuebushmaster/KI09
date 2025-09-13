from pydantic import BaseModel, Field, field_validator
# `Optional` se usa para indicar campos que pueden ser None
from typing import Optional
# `datetime` para manejar fechas de orden
from datetime import datetime
# `Enum` para definir los estados posibles de la orden
from enum import Enum

class OrdenEstado(str, Enum):
    # Enum de strings que lista los estados válidos de una orden
    # Hereda de `str` para que los valores sean tratables como cadenas
    PENDIENTE = "pendiente"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"
    ENVIADA = "enviada"

class OrdenCreateDTO(BaseModel):
    id_cliente: int
    fecha_orden: Optional[datetime] = None
    estado_orden: str = "pendiente"
    direccion_envio: str
    total_orden: float
    ciudad_envio: str
    codigo_postal_envio: str
    pais_envio: str
    metodo_envio: str
    costo_envio: float
    estado_envio: str

class OrdenUpdateDTO(BaseModel):
    id_cliente: Optional[int] = None
    fecha_orden: Optional[datetime] = None
    estado_orden: Optional[str] = None
    direccion_envio: Optional[str] = None
    total_orden: Optional[float] = None
    ciudad_envio: Optional[str] = None
    codigo_postal_envio: Optional[str] = None
    pais_envio: Optional[str] = None
    metodo_envio: Optional[str] = None
    costo_envio: Optional[float] = None
    estado_envio: Optional[str] = None

class OrdenResponseDTO(BaseModel):
    id_orden: int
    id_cliente: int
    fecha_orden: datetime
    estado_orden: str
    direccion_envio: str
    total_orden: float
    ciudad_envio: str
    codigo_postal_envio: str
    pais_envio: str
    metodo_envio: str
    costo_envio: float
    estado_envio: str