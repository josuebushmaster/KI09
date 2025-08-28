from domain.repositories.orden_repository import OrdenRepository
from domain.entities.orden import Orden
from infrastructure.database.postgres_connection import get_db_connection
from typing import List, Optional
import psycopg2.extras


class PostgresOrdenRepository(OrdenRepository):
    def _map_estado_db(self, value):
        # Si la base de datos devuelve enteros, mapearlos a los strings esperados
        if value is None:
            return value
        if isinstance(value, int):
            mapping = {1: 'pendiente', 2: 'completada', 3: 'cancelada', 4: 'enviada'}
            return mapping.get(value, str(value))
        # si ya es string, devolver tal cual
        return value

    def crear(self, orden: Orden) -> Orden:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = """
                INSERT INTO orden (id_cliente, fecha_orden, estado_orden)
                VALUES (%s, %s, %s)
                RETURNING id_orden, id_cliente, fecha_orden, estado_orden;
            """
            cursor.execute(query, (orden.id_cliente, orden.fecha_orden, orden.estado_orden))

            result = cursor.fetchone()
            conn.commit()

            return Orden(
                id_orden=result['id_orden'],
                id_cliente=result['id_cliente'],
                fecha_orden=result['fecha_orden'],
                estado_orden=self._map_estado_db(result['estado_orden'])
            )

        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_orden: int) -> Optional[Orden]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = "SELECT * FROM orden WHERE id_orden = %s;"
            cursor.execute(query, (id_orden,))

            result = cursor.fetchone()
            if not result:
                return None

            return Orden(
                id_orden=result['id_orden'],
                id_cliente=result['id_cliente'],
                fecha_orden=result['fecha_orden'],
                estado_orden=self._map_estado_db(result['estado_orden'])
            )

        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def listar_todos(self) -> List[Orden]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = "SELECT * FROM orden ORDER BY id_orden;"
            cursor.execute(query)

            results = cursor.fetchall()
            return [
                Orden(
                    id_orden=row['id_orden'],
                    id_cliente=row['id_cliente'],
                    fecha_orden=row['fecha_orden'],
                    estado_orden=self._map_estado_db(row['estado_orden'])
                ) for row in results
            ]

        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def listar_por_cliente(self, id_cliente: int) -> List[Orden]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = "SELECT * FROM orden WHERE id_cliente = %s ORDER BY fecha_orden DESC;"
            cursor.execute(query, (id_cliente,))

            results = cursor.fetchall()
            return [
                Orden(
                    id_orden=row['id_orden'],
                    id_cliente=row['id_cliente'],
                    fecha_orden=row['fecha_orden'],
                    estado_orden=self._map_estado_db(row['estado_orden'])
                ) for row in results
            ]

        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def listar_por_fecha(self, fecha_inicio, fecha_fin) -> List[Orden]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = "SELECT * FROM orden WHERE fecha_orden BETWEEN %s AND %s ORDER BY fecha_orden DESC;"
            cursor.execute(query, (fecha_inicio, fecha_fin))

            results = cursor.fetchall()
            return [
                Orden(
                    id_orden=row['id_orden'],
                    id_cliente=row['id_cliente'],
                    fecha_orden=row['fecha_orden'],
                   estado_orden=self._map_estado_db(row['estado_orden'])
                ) for row in results
            ]

        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def actualizar(self, id_orden: int, orden: Orden) -> Optional[Orden]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = """
                UPDATE orden
                SET id_cliente = %s, fecha_orden = %s, estado_orden = %s
                WHERE id_orden = %s
                RETURNING *;
            """
            cursor.execute(query, (
                orden.id_cliente,
                orden.fecha_orden,
                orden.estado_orden,
                id_orden
            ))

            result = cursor.fetchone()
            conn.commit()

            if not result:
                return None

            return Orden(
                id_orden=result['id_orden'],
                id_cliente=result['id_cliente'],
                fecha_orden=result['fecha_orden'],
                estado_orden=self._map_estado_db(result['estado_orden'])
            )

        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def eliminar(self, id_orden: int) -> bool:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = "DELETE FROM orden WHERE id_orden = %s;"
            cursor.execute(query, (id_orden,))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
