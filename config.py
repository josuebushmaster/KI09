import os
from psycopg2.extras import RealDictCursor

# Configuración de la base de datos
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "ki09"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "cassa"),
    "port": os.getenv("DB_PORT", "5432"),
    "cursor_factory": RealDictCursor
}