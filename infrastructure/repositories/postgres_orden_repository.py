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
                INSERT INTO orden (
                    id_cliente, fecha_orden, estado_orden, direccion_envio, total_orden, ciudad_envio, codigo_postal_envio, pais_envio, metodo_envio, costo_envio, estado_envio
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_orden, id_cliente, fecha_orden, estado_orden, direccion_envio, total_orden, ciudad_envio, codigo_postal_envio, pais_envio, metodo_envio, costo_envio, estado_envio;
            """
            cursor.execute(query, (
                orden.id_cliente,
                orden.fecha_orden,
                orden.estado_orden,
                orden.direccion_envio,
                orden.total_orden,
                orden.ciudad_envio,
                orden.codigo_postal_envio,
                orden.pais_envio,
                orden.metodo_envio,
                orden.costo_envio,
                orden.estado_envio
            ))

            result = cursor.fetchone()
            conn.commit()

            return Orden(
                id_orden=result['id_orden'],
                id_cliente=result['id_cliente'],
                fecha_orden=result['fecha_orden'],
                estado_orden=self._map_estado_db(result['estado_orden']),
                direccion_envio=result['direccion_envio'],
                total_orden=result['total_orden'],
                ciudad_envio=result['ciudad_envio'],
                codigo_postal_envio=result['codigo_postal_envio'],
                pais_envio=result['pais_envio'],
                metodo_envio=result['metodo_envio'],
                costo_envio=result['costo_envio'],
                estado_envio=result['estado_envio']
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

            query = "SELECT * FROM orden WHERE id_orden = %s AND (eliminado IS NULL OR eliminado = FALSE);"
            cursor.execute(query, (id_orden,))

            result = cursor.fetchone()
            if not result:
                return None

            return Orden(
                id_orden=result['id_orden'],
                id_cliente=result['id_cliente'],
                fecha_orden=result['fecha_orden'],
                estado_orden=self._map_estado_db(result['estado_orden']),
                direccion_envio=result['direccion_envio'],
                total_orden=result['total_orden'],
                ciudad_envio=result['ciudad_envio'],
                codigo_postal_envio=result['codigo_postal_envio'],
                pais_envio=result['pais_envio'],
                metodo_envio=result['metodo_envio'],
                costo_envio=result['costo_envio'],
                estado_envio=result['estado_envio']
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

            query = "SELECT * FROM orden WHERE (eliminado IS NULL OR eliminado = FALSE) ORDER BY id_orden;"
            cursor.execute(query)

            results = cursor.fetchall()
            return [
                Orden(
                    id_orden=row['id_orden'],
                    id_cliente=row['id_cliente'],
                    fecha_orden=row['fecha_orden'],
                    estado_orden=self._map_estado_db(row['estado_orden']),
                    direccion_envio=row['direccion_envio'],
                    total_orden=row['total_orden'],
                    ciudad_envio=row['ciudad_envio'],
                    codigo_postal_envio=row['codigo_postal_envio'],
                    pais_envio=row['pais_envio'],
                    metodo_envio=row['metodo_envio'],
                    costo_envio=row['costo_envio'],
                    estado_envio=row['estado_envio']
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

            query = "SELECT * FROM orden WHERE id_cliente = %s AND (eliminado IS NULL OR eliminado = FALSE) ORDER BY fecha_orden DESC;"
            cursor.execute(query, (id_cliente,))

            results = cursor.fetchall()
            return [
                Orden(
                    id_orden=row['id_orden'],
                    id_cliente=row['id_cliente'],
                    fecha_orden=row['fecha_orden'],
                    estado_orden=self._map_estado_db(row['estado_orden']),
                    direccion_envio=row['direccion_envio'],
                    total_orden=row['total_orden'],
                    ciudad_envio=row['ciudad_envio'],
                    codigo_postal_envio=row['codigo_postal_envio'],
                    pais_envio=row['pais_envio'],
                    metodo_envio=row['metodo_envio'],
                    costo_envio=row['costo_envio'],
                    estado_envio=row['estado_envio']
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

            query = "SELECT * FROM orden WHERE fecha_orden BETWEEN %s AND %s AND (eliminado IS NULL OR eliminado = FALSE) ORDER BY fecha_orden DESC;"
            cursor.execute(query, (fecha_inicio, fecha_fin))

            results = cursor.fetchall()
            return [
                Orden(
                    id_orden=row['id_orden'],
                    id_cliente=row['id_cliente'],
                    fecha_orden=row['fecha_orden'],
                    estado_orden=self._map_estado_db(row['estado_orden']),
                    direccion_envio=row['direccion_envio'],
                    total_orden=row['total_orden'],
                    ciudad_envio=row['ciudad_envio'],
                    codigo_postal_envio=row['codigo_postal_envio'],
                    pais_envio=row['pais_envio'],
                    metodo_envio=row['metodo_envio'],
                    costo_envio=row['costo_envio'],
                    estado_envio=row['estado_envio']
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

            # Obtener la orden actual
            cursor.execute("SELECT * FROM orden WHERE id_orden = %s;", (id_orden,))
            actual = cursor.fetchone()
            if not actual:
                return None

            # Merge: usar el valor nuevo si no es None, si es None usar el actual
            merged = {
                'id_cliente': orden.id_cliente if orden.id_cliente is not None else actual['id_cliente'],
                'fecha_orden': orden.fecha_orden if orden.fecha_orden is not None else actual['fecha_orden'],
                'estado_orden': orden.estado_orden if orden.estado_orden is not None else actual['estado_orden'],
                'direccion_envio': orden.direccion_envio if orden.direccion_envio is not None else actual['direccion_envio'],
                'total_orden': orden.total_orden if orden.total_orden is not None else actual['total_orden'],
                'ciudad_envio': orden.ciudad_envio if orden.ciudad_envio is not None else actual['ciudad_envio'],
                'codigo_postal_envio': orden.codigo_postal_envio if orden.codigo_postal_envio is not None else actual['codigo_postal_envio'],
                'pais_envio': orden.pais_envio if orden.pais_envio is not None else actual['pais_envio'],
                'metodo_envio': orden.metodo_envio if orden.metodo_envio is not None else actual['metodo_envio'],
                'costo_envio': orden.costo_envio if orden.costo_envio is not None else actual['costo_envio'],
                'estado_envio': orden.estado_envio if orden.estado_envio is not None else actual['estado_envio'],
            }

            query = """
                UPDATE orden
                SET id_cliente = %s, fecha_orden = %s, estado_orden = %s, direccion_envio = %s, total_orden = %s, ciudad_envio = %s, codigo_postal_envio = %s, pais_envio = %s, metodo_envio = %s, costo_envio = %s, estado_envio = %s
                WHERE id_orden = %s
                RETURNING *;
            """
            cursor.execute(query, (
                merged['id_cliente'],
                merged['fecha_orden'],
                merged['estado_orden'],
                merged['direccion_envio'],
                merged['total_orden'],
                merged['ciudad_envio'],
                merged['codigo_postal_envio'],
                merged['pais_envio'],
                merged['metodo_envio'],
                merged['costo_envio'],
                merged['estado_envio'],
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
                estado_orden=self._map_estado_db(result['estado_orden']),
                direccion_envio=result['direccion_envio'],
                total_orden=result['total_orden'],
                ciudad_envio=result['ciudad_envio'],
                codigo_postal_envio=result['codigo_postal_envio'],
                pais_envio=result['pais_envio'],
                metodo_envio=result['metodo_envio'],
                costo_envio=result['costo_envio'],
                estado_envio=result['estado_envio']
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
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Borrado lógico: marcar eliminado y cancelar la orden para preservar historial
            query = "UPDATE orden SET eliminado = TRUE, estado_orden = %s WHERE id_orden = %s;"
            cursor.execute(query, (3, id_orden))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass
