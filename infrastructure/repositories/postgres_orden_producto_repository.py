from domain.repositories.orden_producto_repository import OrdenProductoRepository
from domain.entities.orden_producto import OrdenProducto
from infrastructure.database.postgres_connection import get_db_connection
from typing import List, Optional

class PostgresOrdenProductoRepository(OrdenProductoRepository):

    def listar_todos(self) -> List[OrdenProducto]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = 'SELECT * FROM orden_producto ORDER BY "id_ordenProd";'
            cursor.execute(query)
            rows = cursor.fetchall()
            desc = [d[0] for d in cursor.description]
            result_list = []
            for row in rows:
                if isinstance(row, dict):
                    result = row
                else:
                    result = dict(zip(desc, row))
                result_list.append(OrdenProducto(
                    id_ordenProd=result['id_ordenprod'] if 'id_ordenprod' in result else result['id_ordenProd'],
                    id_producto=result['id_producto'],
                    cantidad=result['cantidad'],
                    precio_unitario=result['precio_unitario'],
                    id_orden=result['id_orden']
                ))
            return result_list
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()
    def crear(self, orden_producto: OrdenProducto) -> OrdenProducto:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                INSERT INTO orden_producto (id_producto, cantidad, precio_unitario, id_orden)
                VALUES (%s, %s, %s, %s)
                RETURNING "id_ordenProd", id_producto, cantidad, precio_unitario, id_orden;
            """
            cursor.execute(query, (
                orden_producto.id_producto,
                orden_producto.cantidad,
                orden_producto.precio_unitario,
                orden_producto.id_orden
            ))
            row = cursor.fetchone()
            conn.commit()
            if not row:
                raise Exception("No se pudo crear el registro de orden_producto.")
            # Adaptar a dict si es necesario
            if isinstance(row, dict):
                result = row
            else:
                desc = [d[0] for d in cursor.description]
                result = dict(zip(desc, row))
            return OrdenProducto(
                id_ordenProd=result['id_ordenprod'] if 'id_ordenprod' in result else result['id_ordenProd'],
                id_producto=result['id_producto'],
                cantidad=result['cantidad'],
                precio_unitario=result['precio_unitario'],
                id_orden=result['id_orden']
            )
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_ordenProd: int) -> Optional[OrdenProducto]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = 'SELECT * FROM orden_producto WHERE "id_ordenProd" = %s;'
            cursor.execute(query, (id_ordenProd,))
            row = cursor.fetchone()
            if not row:
                return None
            if isinstance(row, dict):
                result = row
            else:
                desc = [d[0] for d in cursor.description]
                result = dict(zip(desc, row))
            return OrdenProducto(
                id_ordenProd=result['id_ordenprod'] if 'id_ordenprod' in result else result['id_ordenProd'],
                id_producto=result['id_producto'],
                cantidad=result['cantidad'],
                precio_unitario=result['precio_unitario'],
                id_orden=result['id_orden']
            )
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def listar_por_orden(self, id_orden: int) -> List[OrdenProducto]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = 'SELECT * FROM orden_producto WHERE id_orden = %s ORDER BY "id_ordenProd";'
            cursor.execute(query, (id_orden,))
            rows = cursor.fetchall()
            desc = [d[0] for d in cursor.description]
            result_list = []
            for row in rows:
                if isinstance(row, dict):
                    result = row
                else:
                    result = dict(zip(desc, row))
                result_list.append(OrdenProducto(
                    id_ordenProd=result['id_ordenprod'] if 'id_ordenprod' in result else result['id_ordenProd'],
                    id_producto=result['id_producto'],
                    cantidad=result['cantidad'],
                    precio_unitario=result['precio_unitario'],
                    id_orden=result['id_orden']
                ))
            return result_list
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def actualizar(self, id_ordenProd: int, orden_producto: OrdenProducto) -> Optional[OrdenProducto]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = """
                UPDATE orden_producto
                SET id_producto = %s, cantidad = %s, precio_unitario = %s, id_orden = %s
                WHERE "id_ordenProd" = %s
                RETURNING *;
            """
            cursor.execute(query, (
                orden_producto.id_producto,
                orden_producto.cantidad,
                orden_producto.precio_unitario,
                orden_producto.id_orden,
                id_ordenProd
            ))
            row = cursor.fetchone()
            conn.commit()
            if not row:
                return None
            if isinstance(row, dict):
                result = row
            else:
                desc = [d[0] for d in cursor.description]
                result = dict(zip(desc, row))
            return OrdenProducto(
                id_ordenProd=result['id_ordenprod'] if 'id_ordenprod' in result else result['id_ordenProd'],
                id_producto=result['id_producto'],
                cantidad=result['cantidad'],
                precio_unitario=result['precio_unitario'],
                id_orden=result['id_orden']
            )
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def eliminar(self, id_ordenProd: int) -> bool:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = 'DELETE FROM orden_producto WHERE "id_ordenProd" = %s;'
            cursor.execute(query, (id_ordenProd,))
            deleted = cursor.rowcount > 0
            conn.commit()
            return deleted
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
