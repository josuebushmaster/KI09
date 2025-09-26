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
                INSERT INTO productos (nombre_producto, precio, costo, id_categoria, descripcion, stock, imagen_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id_producto, nombre_producto, precio, costo, id_categoria, descripcion, stock, imagen_url;
            """
            cursor.execute(query, (
                producto.nombre_producto,
                producto.precio,
                producto.costo,
                producto.id_categoria,
                producto.descripcion,
                producto.stock,
                producto.imagen_url
            ))
            result = cursor.fetchone()
            conn.commit()
            return Producto(
                id_producto=result['id_producto'],
                nombre_producto=result['nombre_producto'],
                precio=result['precio'],
                costo=result['costo'],
                id_categoria=result['id_categoria'],
                descripcion=result['descripcion'],
                stock=result['stock'],
                imagen_url=result['imagen_url']
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
            query = "SELECT * FROM productos WHERE id_producto = %s AND (eliminado IS NULL OR eliminado = FALSE);"
            cursor.execute(query, (id_producto,))
            result = cursor.fetchone()
            if not result:
                return None
            return Producto(
                id_producto=result['id_producto'],
                nombre_producto=result['nombre_producto'],
                precio=result['precio'],
                costo=result['costo'],
                id_categoria=result['id_categoria'],
                descripcion=result['descripcion'],
                stock=result['stock'],
                imagen_url=result['imagen_url']
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
            query = "SELECT * FROM productos WHERE (eliminado IS NULL OR eliminado = FALSE) ORDER BY id_producto;"
            cursor.execute(query)
            results = cursor.fetchall()
            return [
                Producto(
                    id_producto=row['id_producto'],
                    nombre_producto=row['nombre_producto'],
                    precio=row['precio'],
                    costo=row['costo'],
                    id_categoria=row['id_categoria'],
                    descripcion=row['descripcion'],
                    stock=row['stock'],
                    imagen_url=row['imagen_url']
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
                SET nombre_producto = %s, precio = %s, costo = %s, id_categoria = %s, descripcion = %s, stock = %s, imagen_url = %s
                WHERE id_producto = %s
                RETURNING *;
            """
            cursor.execute(query, (
                producto.nombre_producto,
                producto.precio,
                producto.costo,
                producto.id_categoria,
                producto.descripcion,
                producto.stock,
                producto.imagen_url,
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
                costo=result['costo'],
                id_categoria=result['id_categoria'],
                descripcion=result['descripcion'],
                stock=result['stock'],
                imagen_url=result['imagen_url']
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
        cursor = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Verificar si existen referencias en orden_producto (para diagnóstico / futura lógica)
            cursor.execute("SELECT 1 FROM orden_producto WHERE id_producto = %s LIMIT 1;", (id_producto,))
            tiene_refs = cursor.fetchone() is not None

            # Si hay referencias en orden_producto, marcarlas como eliminadas (borrado lógico en cascada)
            if tiene_refs:
                cursor.execute("UPDATE orden_producto SET eliminado = TRUE WHERE id_producto = %s;", (id_producto,))

            # Borrado lógico: marcar producto como eliminado para evitar violaciones de FK y preservar historial
            query = "UPDATE productos SET eliminado = TRUE WHERE id_producto = %s;"
            cursor.execute(query, (id_producto,))

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

    def disminuir_stock(self, id_producto: int, cantidad: int, conn=None) -> bool:
        """Disminuye el stock de un producto. Si se pasa `conn`, usa esa conexión (no commit/rollback);
        de lo contrario abre una nueva conexión.
        Retorna True si se aplicó la disminución (stock suficiente), False si no.
        """
        own_conn = False
        cursor = None
        try:
            if conn is None:
                conn = get_db_connection()
                own_conn = True
            cursor = conn.cursor()
            query = """
                UPDATE productos
                SET stock = stock - %s
                WHERE id_producto = %s AND (eliminado IS NULL OR eliminado = FALSE) AND stock >= %s
            """
            cursor.execute(query, (cantidad, id_producto, cantidad))
            if own_conn:
                conn.commit()
            return cursor.rowcount > 0
        except Exception:
            if own_conn and conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if own_conn and conn:
                try:
                    conn.close()
                except Exception:
                    pass