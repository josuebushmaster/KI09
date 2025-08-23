from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import uvicorn
from typing import Optional

app = FastAPI()

# Configuración de PostgreSQL (¡Ajusta estos valores!)
DB_CONFIG = {
    "host": "localhost",
    "database": "ki09",
    "user": "postgres",  # Ej: "postgres"
    "password": "cassa",
    "port": "5432",
    "cursor_factory": RealDictCursor  # Para obtener resultados como diccionarios
}

# Modelo Pydantic para validar los datos de entrada
class Categoria(BaseModel):
    nombre_categoria: str
    descripcion: str

class CategoriaUpdate(BaseModel):
    nombre_categoria: Optional[str] = None
    descripcion: Optional[str] = None

# Conexión a la base de datos
def get_db():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn


# Endpoint POST para crear una categoría
@app.post("/categorias/", status_code=status.HTTP_201_CREATED)
async def crear_categoria(categoria: Categoria):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        query = """
            INSERT INTO categoria (nombre_categoria, descripcion)
            VALUES (%s, %s)
            RETURNING id_categoria;
        """
        cursor.execute(query, (
            categoria.nombre_categoria,
            categoria.descripcion
        ))

        new_id = cursor.fetchone()["id_categoria"]
        conn.commit()

        return {
            "mensaje": "Categoría creada exitosamente",
            "id_categoria": new_id
        }

    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en PostgreSQL: {str(e)}"
        )
    finally:
        if conn:
            conn.close()
# Endpoint GET para buscar categoría por ID
@app.get("/categorias/{id_categoria}")
async def obtener_categoria(id_categoria: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM categoria WHERE id_categoria = %s;",
            (id_categoria,)
        )
        categoria = cursor.fetchone()

        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )

        return {"categoria": categoria}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar PostgreSQL: {str(e)}"
        )
    finally:
        if conn:
            conn.close()

# Endpoint GET para listar todas las categorías
@app.get("/categorias/")
async def listar_categorias():
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM categoria ORDER BY id_categoria;")
        categorias = cursor.fetchall()

        return {"categorias": categorias}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al consultar PostgreSQL: {str(e)}"
        )
    finally:
        if conn:
            conn.close()

# Endpoint PUT para actualizar una categoría
@app.put("/categorias/{id_categoria}")
async def actualizar_categoria(
    id_categoria: int,
    categoria: CategoriaUpdate  # Ahora está definida antes de usarse
):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Verificar si existe la categoría
        cursor.execute(
            "SELECT 1 FROM categoria WHERE id_categoria = %s;",
            (id_categoria,)
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )

        # Construir query dinámica
        update_fields = []
        params = []
        
        if categoria.nombre_categoria is not None:
            update_fields.append("nombre_categoria = %s")
            params.append(categoria.nombre_categoria)
        
        if categoria.descripcion is not None:
            update_fields.append("descripcion = %s")
            params.append(categoria.descripcion)

        if not update_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )

        params.append(id_categoria)
        query = f"""
            UPDATE categoria
            SET {', '.join(update_fields)}
            WHERE id_categoria = %s
            RETURNING *;
        """
        
        cursor.execute(query, params)
        updated_categoria = cursor.fetchone()
        conn.commit()

        return {
            "mensaje": "Categoría actualizada exitosamente",
            "categoria": updated_categoria
        }

    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en PostgreSQL: {str(e)}"
        )
    finally:
        if conn:
            conn.close()

# Endpoint DELETE para eliminar una categoría
@app.delete("/categorias/{id_categoria}", status_code=status.HTTP_200_OK)
async def eliminar_categoria(id_categoria: int):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Verificar si la categoría existe
        cursor.execute(
            "SELECT 1 FROM categoria WHERE id_categoria = %s;",
            (id_categoria,)
        )
        if not cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )

        # Eliminar la categoría
        cursor.execute(
            "DELETE FROM categoria WHERE id_categoria = %s RETURNING *;",
            (id_categoria,)
        )
        deleted_categoria = cursor.fetchone()
        conn.commit()

        return {
            "mensaje": "Categoría eliminada exitosamente",
            "categoria": deleted_categoria
        }

    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en PostgreSQL: {str(e)}"
        )
    finally:
        if conn:
            conn.close()



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)