import os
import psycopg2
from config import DB_CONFIG
from psycopg2.extras import RealDictCursor


def get_db_connection():
    """Establece y retorna una conexión a PostgreSQL.

    Prioriza (en este orden): RAILWAY_DATABASE_URL, DATABASE_URL, y luego
    la configuración por componentes definida en `DB_CONFIG`.
    """
    # Priorizar URL completa (Railway o genérica)
    database_url = os.getenv('RAILWAY_DATABASE_URL') or os.getenv('DATABASE_URL')
    if database_url:
        database_url = database_url.strip()
        database_url = database_url.replace('[', '').replace(']', '')
        sslmode = os.getenv('DB_SSLMODE', 'require')
        try:
            # Asegurar que el cursor devuelva diccionarios como el fallback
            return psycopg2.connect(database_url, sslmode=sslmode, cursor_factory=RealDictCursor)
        except Exception as e:
            raise Exception(f"Error al conectar a PostgreSQL usando DATABASE_URL: {e}")

    # Fallback: usar configuración por componentes (host, user, ...)
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        raise Exception(f"Error al conectar a PostgreSQL (DB_CONFIG): {str(e)}")