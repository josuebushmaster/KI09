import pandas as pd
from matplotlib import pyplot as plt
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Obtener la URL de conexión
db_url = os.getenv("DATABASE_URL")

# Crear el engine
engine = create_engine(db_url)

# Consultar la base de datos
query = "SELECT * FROM categoria"
df = pd.read_sql(query, engine)

