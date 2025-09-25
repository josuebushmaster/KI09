from domain.repositories.cliente_repository import ClienteRepository
from domain.entities.cliente import Cliente
from infrastructure.database.postgres_connection import get_db_connection
from typing import List, Optional
import psycopg2.extras


class PostgresClienteRepository(ClienteRepository):
    def crear(self, cliente: Cliente) -> Cliente:
        conn = None
        try:
            conn = get_db_connection()
            # usar cursor que devuelva dicts para mantener compatibilidad con otros repos
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = """
                INSERT INTO clientes (nombre, apellido, edad, email, telefono, direccion)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_cliente, nombre, apellido, edad, email, telefono, direccion;
            """
            cursor.execute(query, (
                cliente.nombre,
                cliente.apellido,
                cliente.edad,
                cliente.email,
                cliente.telefono,
                cliente.direccion
            ))

            result = cursor.fetchone()
            conn.commit()

            return Cliente(
                id_cliente=result['id_cliente'],
                nombre=result['nombre'],
                apellido=result['apellido'],
                edad=result['edad'],
                email=result['email'],
                telefono=result['telefono'],
                direccion=result['direccion']
            )

        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_cliente: int) -> Optional[Cliente]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = "SELECT * FROM clientes WHERE id_cliente = %s AND (eliminado IS NULL OR eliminado = FALSE);"
            cursor.execute(query, (id_cliente,))

            result = cursor.fetchone()
            if not result:
                return None

            return Cliente(
                id_cliente=result['id_cliente'],
                nombre=result['nombre'],
                apellido=result['apellido'],
                edad=result['edad'],
                email=result['email'],
                telefono=result['telefono'],
                direccion=result['direccion']
            )

        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def listar_todos(self) -> List[Cliente]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            query = "SELECT * FROM clientes WHERE (eliminado IS NULL OR eliminado = FALSE) ORDER BY id_cliente;"
            cursor.execute(query)

            results = cursor.fetchall()
            return [
                Cliente(
                    id_cliente=row['id_cliente'],
                    nombre=row['nombre'],
                    apellido=row['apellido'],
                    edad=row['edad'],
                    email=row['email'],
                    telefono=row['telefono'],
                    direccion=row['direccion']
                ) for row in results
            ]

        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def actualizar(self, id_cliente: int, cliente: Cliente) -> Optional[Cliente]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            query = """
                UPDATE clientes
                SET nombre = %s, apellido = %s, edad = %s, email = %s, telefono = %s, direccion = %s
                WHERE id_cliente = %s
                RETURNING *;
            """
            cursor.execute(query, (
                cliente.nombre,
                cliente.apellido,
                cliente.edad,
                cliente.email,
                cliente.telefono,
                cliente.direccion,
                id_cliente
            ))

            result = cursor.fetchone()
            conn.commit()

            if not result:
                return None

            return Cliente(
                id_cliente=result['id_cliente'],
                nombre=result['nombre'],
                apellido=result['apellido'],
                edad=result['edad'],
                email=result['email'],
                telefono=result['telefono'],
                direccion=result['direccion']
            )

        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def eliminar(self, id_cliente: int) -> bool:
        conn = None
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            query = "UPDATE clientes SET eliminado = TRUE WHERE id_cliente = %s;"
            cursor.execute(query, (id_cliente,))

            conn.commit()
            actualizado = cursor.rowcount > 0

            return actualizado

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
