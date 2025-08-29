import os
import psycopg2
from typing import Any

__all__ = ["get_railway_connection"]


def get_railway_connection() -> Any:
    """Establece y devuelve una conexión a PostgreSQL en Railway.

    Prioriza las variables de entorno en este orden:
      1. RAILWAY_DATABASE_URL
      2. DATABASE_URL
      3. Variables por componentes: DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

    Usa `sslmode` por defecto en 'require' (puedes controlar con DB_SSLMODE).
    Lanza una excepción con mensaje claro si faltan variables o la conexión falla.
    """
    database_url = os.getenv("RAILWAY_DATABASE_URL") or os.getenv("DATABASE_URL")

    if database_url:
        database_url = database_url.strip()
        # Quitar corchetes accidentales y espacios
        database_url = database_url.replace("[", "").replace("]", "")
        sslmode = os.getenv("DB_SSLMODE", "require")
        try:
            return psycopg2.connect(database_url, sslmode=sslmode)
        except Exception as e:
            raise Exception(f"Error conectando a Railway (URL): {e}")

    # Fallback a variables por componentes
    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    dbname = os.getenv("DB_NAME")
    port = os.getenv("DB_PORT", "5432")

    missing = [name for name, val in (
        ("DB_HOST", host), ("DB_USER", user), ("DB_PASSWORD", password), ("DB_NAME", dbname)
    ) if not val]
    if missing:
        raise Exception(
            "Faltan variables de entorno para la conexión a Railway: " + ", ".join(missing) +
            ". Defina RAILWAY_DATABASE_URL o las variables DB_HOST/DB_USER/DB_PASSWORD/DB_NAME."
        )

    sslmode = os.getenv("DB_SSLMODE", "require")
    try:
        return psycopg2.connect(host=host, user=user, password=password, dbname=dbname, port=port, sslmode=sslmode)
    except Exception as e:
        raise Exception(f"Error conectando a Railway (componentes): {e}")
