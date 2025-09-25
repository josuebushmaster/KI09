from domain.repositories.venta_repository import VentaRepository
from domain.entities.venta import Venta
from infrastructure.database.postgres_connection import get_db_connection
from typing import List, Optional

class PostgresVentaRepository(VentaRepository):
    def crear(self, venta: Venta) -> Venta:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO ventas (id_orden, fecha_venta, total_venta, metodo_pago)
                VALUES (%s, %s, %s, %s)
                RETURNING id_venta, id_orden, fecha_venta, total_venta, metodo_pago;
            """
            cursor.execute(query, (
                venta.id_orden,
                venta.fecha_venta,
                venta.total_venta,
                venta.metodo_pago
            ))
            result = cursor.fetchone()
            conn.commit()
            return Venta(
                id_venta=result['id_venta'],
                id_orden=result['id_orden'],
                fecha_venta=result['fecha_venta'],
                total_venta=result['total_venta'],
                metodo_pago=result['metodo_pago']
            )
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_venta: int) -> Optional[Venta]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM ventas WHERE id_venta = %s AND (eliminado IS NULL OR eliminado = FALSE);"
            cursor.execute(query, (id_venta,))
            result = cursor.fetchone()
            if not result:
                return None
            return Venta(
                id_venta=result['id_venta'],
                id_orden=result['id_orden'],
                fecha_venta=result['fecha_venta'],
                total_venta=result['total_venta'],
                metodo_pago=result['metodo_pago']
            )
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def listar_todos(self) -> List[Venta]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM ventas WHERE (eliminado IS NULL OR eliminado = FALSE) ORDER BY id_venta;"
            cursor.execute(query)
            results = cursor.fetchall()
            return [
                Venta(
                    id_venta=row['id_venta'],
                    id_orden=row['id_orden'],
                    fecha_venta=row['fecha_venta'],
                    total_venta=row['total_venta'],
                    metodo_pago=row['metodo_pago']
                ) for row in results
            ]
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def actualizar(self, id_venta: int, venta: Venta) -> Optional[Venta]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                UPDATE ventas
                SET id_orden = %s, fecha_venta = %s, total_venta = %s, metodo_pago = %s
                WHERE id_venta = %s AND (eliminado IS NULL OR eliminado = FALSE)
                RETURNING *;
            """
            # aceptar tanto objeto Venta como dict con las mismas keys
            if isinstance(venta, dict):
                id_orden_val = venta.get('id_orden')
                fecha_venta_val = venta.get('fecha_venta')
                total_venta_val = venta.get('total_venta')
                metodo_pago_val = venta.get('metodo_pago')
            else:
                id_orden_val = venta.id_orden
                fecha_venta_val = venta.fecha_venta
                total_venta_val = venta.total_venta
                metodo_pago_val = venta.metodo_pago

            cursor.execute(query, (
                id_orden_val,
                fecha_venta_val,
                total_venta_val,
                metodo_pago_val,
                id_venta
            ))
            result = cursor.fetchone()
            conn.commit()
            if not result:
                return None
            return Venta(
                id_venta=result['id_venta'],
                id_orden=result['id_orden'],
                fecha_venta=result['fecha_venta'],
                total_venta=result['total_venta'],
                metodo_pago=result['metodo_pago']
            )
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def eliminar(self, id_venta: int) -> bool:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Soft delete: marcar como eliminado para preservar histórico
            query = "UPDATE ventas SET eliminado = TRUE WHERE id_venta = %s;"
            cursor.execute(query, (id_venta,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
