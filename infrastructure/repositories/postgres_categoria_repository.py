from domain.repositories.categoria_repository import CategoriaRepository
from domain.entities.categoria import Categoria
from infrastructure.database.postgres_connection import get_db_connection
from typing import List, Optional

class PostgresCategoriaRepository(CategoriaRepository):
    def crear(self, categoria: Categoria) -> Categoria:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO categoria (nombre_categoria, descripcion)
                VALUES (%s, %s)
                RETURNING id_categoria, nombre_categoria, descripcion;
            """
            cursor.execute(query, (categoria.nombre_categoria, categoria.descripcion))
            
            result = cursor.fetchone()
            conn.commit()
            
            return Categoria(
                id_categoria=result['id_categoria'],
                nombre_categoria=result['nombre_categoria'],
                descripcion=result['descripcion']
            )
            
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def obtener_por_id(self, id_categoria: int) -> Optional[Categoria]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM categoria WHERE id_categoria = %s;"
            cursor.execute(query, (id_categoria,))
            
            result = cursor.fetchone()
            if not result:
                return None
                
            return Categoria(
                id_categoria=result['id_categoria'],
                nombre_categoria=result['nombre_categoria'],
                descripcion=result['descripcion']
            )
            
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def listar_todas(self) -> List[Categoria]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "SELECT * FROM categoria ORDER BY id_categoria;"
            cursor.execute(query)
            
            results = cursor.fetchall()
            return [
                Categoria(
                    id_categoria=row['id_categoria'],
                    nombre_categoria=row['nombre_categoria'],
                    descripcion=row['descripcion']
                ) for row in results
            ]
            
        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def actualizar(self, id_categoria: int, categoria: Categoria) -> Optional[Categoria]:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE categoria 
                SET nombre_categoria = %s, descripcion = %s
                WHERE id_categoria = %s
                RETURNING *;
            """
            cursor.execute(query, (
                categoria.nombre_categoria,
                categoria.descripcion,
                id_categoria
            ))
            
            result = cursor.fetchone()
            conn.commit()
            
            if not result:
                return None
                
            return Categoria(
                id_categoria=result['id_categoria'],
                nombre_categoria=result['nombre_categoria'],
                descripcion=result['descripcion']
            )
            
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    def eliminar(self, id_categoria: int) -> bool:
        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            query = "DELETE FROM categoria WHERE id_categoria = %s;"
            cursor.execute(query, (id_categoria,))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()