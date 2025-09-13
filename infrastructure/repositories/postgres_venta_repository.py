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
            query = "SELECT * FROM ventas WHERE id_venta = %s;"
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
            query = "SELECT * FROM ventas ORDER BY id_venta;"
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
                WHERE id_venta = %s
                RETURNING *;
            """
            cursor.execute(query, (
                venta.id_orden,
                venta.fecha_venta,
                venta.total_venta,
                venta.metodo_pago,
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
            query = "DELETE FROM ventas WHERE id_venta = %s;"
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
