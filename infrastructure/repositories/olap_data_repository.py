import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class OlapDataRepository:
    def __init__(self):
        self.conn_str = os.getenv('OLAP_DATABASE_URL')
        if not self.conn_str:
            raise RuntimeError('OLAP_DATABASE_URL no encontrada en variables de entorno')

    def get_table_df(self, table_name: str) -> pd.DataFrame:
        """Extrae toda la data de una tabla y la retorna como DataFrame."""
        query = f"SELECT * FROM {table_name}"
        with psycopg2.connect(self.conn_str) as conn:
            df = pd.read_sql_query(query, conn)
        return df

    def get_all_olap_data(self) -> dict:
        """
        Extrae toda la información de las 7 tablas OLAP y retorna un dict de DataFrames.
        Modifica los nombres de las tablas según tu modelo.
        """
        tables = [
            "hecho_ventas",
            "dim_cliente",
            "dim_producto",
            "dim_tiempo",
            "dim_envio",
            "dim_categoria",
            "dim_metodo_pago",
            "vw_kpi_clientes_unicos_mes",
            "vw_kpi_ventas_categoria",
            "vw_productos_mejor_margen",
            "vw_ventas_por_mes",
            "vw_kpi_margen_promedio_producto",
            "vw_kpi_top_clientes",
            "vw_kpi_top_productos",
            "vw_kpi_ventas_pago_envio",
            "vw_kpi_ventas_pais_anio",
            "vw_kpi_ventas_trimestre",
            "vw_top_clientes",
            "vw_ventas_trimestre_categoria",
            "vw_kpi_ventas_mensual",
            "vw_ventas_producto_mes",
            "vw_ventas_metodo_envio",
            "vw_ventas_pais_anio",
            "vw_kpi_retencion_clientes",
            "vw_ventas_tiempo_producto",
            "vw_ventas_cliente",
            "vw_ventas_metodo_pago_envio"
            
        ]
        dataframes = {}
        for table in tables:
            try:
                dataframes[table] = self.get_table_df(table)
            except Exception as e:
                dataframes[table] = f"Error: {e}"
        return dataframes

# Ejemplo de uso:
if __name__ == "__main__":
    repo = OlapDataRepository()
    olap_data = repo.get_all_olap_data()
    for table, df in olap_data.items():
        if isinstance(df, pd.DataFrame):
            print(f"Tabla: {table}, Filas: {len(df)}")
            print(df.head())
        else:
            print(f"Tabla: {table}, Error: {df}")