from domain.repositories.producto_repository import ProductoRepository
from domain.entities.producto import Producto
from infrastructure.database.postgres_connection import get_db_connection
from typing import List, Optional

class PostgresProductoRepository(ProductoRepository):
    def crear(self, producto: Producto) -> Producto:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO productos (nombre_producto, precio, id_categoria)
                VALUES (%s, %s, %s)
                RETURNING id_producto, nombre_producto, precio, id_categoria;
            """
            cursor.execute(query, (producto.nombre_producto, producto.precio, producto.id_categoria))
            
            result = cursor.fetchone()
            conn.commit()
            
            return Producto(
                id_producto=result['id_producto'],
                nombre_producto=result['nombre_producto'],
                precio=result['precio'],
                id_categoria=result['id_categoria']
            )
            
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_producto: int) -> Optional[Producto]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM productos WHERE id_producto = %s;"
            cursor.execute(query, (id_producto,))
            
            result = cursor.fetchone()
            if not result:
                return None
                
            return Producto(
                id_producto=result['id_producto'],
                nombre_producto=result['nombre_producto'],
                precio=result['precio'],
                id_categoria=result['id_categoria']
            )
            
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def listar_todos(self) -> List[Producto]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM productos ORDER BY id_producto;"
            cursor.execute(query)
            
            results = cursor.fetchall()
            return [
                Producto(
                    id_producto=row['id_producto'],
                    nombre_producto=row['nombre_producto'],
                    precio=row['precio'],
                    id_categoria=row['id_categoria']
                ) for row in results
            ]
            
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def actualizar(self, id_producto: int, producto: Producto) -> Optional[Producto]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE productos
                SET nombre_producto = %s, precio = %s, id_categoria = %s
                WHERE id_producto = %s
                RETURNING *;
            """
            cursor.execute(query, (
                producto.nombre_producto,
                producto.precio,
                producto.id_categoria,
                id_producto
            ))
            
            result = cursor.fetchone()
            conn.commit()
            
            if not result:
                return None
                
            return Producto(
                id_producto=result['id_producto'],
                nombre_producto=result['nombre_producto'],
                precio=result['precio'],
                id_categoria=result['id_categoria']
            )
            
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def eliminar(self, id_producto: int) -> bool:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM productos WHERE id_producto = %s;"
            cursor.execute(query, (id_producto,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()