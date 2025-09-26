# CrearVentaUseCase siguiendo el patrón de producto
from domain.entities.venta import Venta
from domain.repositories.venta_repository import VentaRepository
from domain.repositories.orden_producto_repository import OrdenProductoRepository
from domain.repositories.producto_repository import ProductoRepository
from infrastructure.database.postgres_connection import get_db_connection

class CrearVentaUseCase:
	def __init__(self, venta_repository: VentaRepository,
				 orden_producto_repository: OrdenProductoRepository,
				 producto_repository: ProductoRepository):
		self.venta_repository = venta_repository
		self.orden_producto_repository = orden_producto_repository
		self.producto_repository = producto_repository

	def execute(self, id_orden: int, fecha_venta, total_venta: float, metodo_pago: str) -> Venta:
		conn = None
		try:
			conn = get_db_connection()
			cursor = conn.cursor()

			# Obtener líneas de la orden usando la misma conexión
			cursor.execute('SELECT id_producto, cantidad FROM orden_producto WHERE id_orden = %s AND (eliminado IS NULL OR eliminado = FALSE);', (id_orden,))
			rows = cursor.fetchall()

			if not rows:
				raise Exception(f"La orden {id_orden} no tiene items o no existe")

			# Disminuir stock por cada item usando la misma conexión
			for row in rows:
				# row puede ser dict o tuple según cursor_factory; normalizar
				if isinstance(row, dict):
					id_producto = row.get('id_producto')
					cantidad = row.get('cantidad')
				else:
					id_producto = row[0]
					cantidad = row[1]

				ok = self.producto_repository.disminuir_stock(id_producto, cantidad, conn=conn)
				if not ok:
					raise Exception(f"Stock insuficiente para producto {id_producto}")

			# Crear la venta usando la misma conexión
			venta = Venta(id_orden=id_orden, fecha_venta=fecha_venta, total_venta=total_venta, metodo_pago=metodo_pago)
			created = self.venta_repository.crear(venta, conn=conn)

			conn.commit()
			return created
		except Exception as e:
			if conn:
				conn.rollback()
			raise e
		finally:
			if conn:
				conn.close()
