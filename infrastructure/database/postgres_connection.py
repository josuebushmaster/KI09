import psycopg2
from config import DB_CONFIG

def get_db_connection():
    """Establece y retorna una conexión a PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        raise Exception(f"Error al conectar a PostgreSQL: {str(e)}")