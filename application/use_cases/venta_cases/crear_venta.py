# CrearVentaUseCase siguiendo el patrón de producto
from domain.entities.venta import Venta
from domain.repositories.venta_repository import VentaRepository

class CrearVentaUseCase:
	def __init__(self, venta_repository: VentaRepository):
		self.venta_repository = venta_repository

	def execute(self, id_orden: int, fecha_venta, total_venta: float, metodo_pago: str) -> Venta:
		venta = Venta(id_orden=id_orden, fecha_venta=fecha_venta, total_venta=total_venta, metodo_pago=metodo_pago)
		return self.venta_repository.crear(venta)
