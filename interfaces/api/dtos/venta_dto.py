from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VentaCreateDTO(BaseModel):
	id_orden: int
	fecha_venta: datetime
	total_venta: float
	metodo_pago: str

class VentaUpdateDTO(BaseModel):
	id_orden: Optional[int] = None
	fecha_venta: Optional[datetime] = None
	total_venta: Optional[float] = None
	metodo_pago: Optional[str] = None

class VentaResponseDTO(BaseModel):
	id_venta: int
	id_orden: int
	fecha_venta: datetime
	total_venta: float
	metodo_pago: str
