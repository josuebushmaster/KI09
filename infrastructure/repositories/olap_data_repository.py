import os
import re
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
        """
        Extrae toda la data de una tabla y la retorna como DataFrame.
        Valida el nombre de la tabla para evitar inyecciones/errores.
        """
        if not self._is_valid_identifier(table_name):
            raise ValueError(f"Nombre de tabla inválido: {table_name}")
        query = f"SELECT * FROM {table_name}"
        with psycopg2.connect(self.conn_str) as conn:
            df = pd.read_sql_query(query, conn)
        return df

    def get_all_olap_data(self) -> dict:
        """
        Extrae SOLO información de las tablas/vistas del esquema 'public' (de negocio).
        Ignora metadatos y tablas del sistema.
        """
        print("📊 INICIANDO EXTRACCIÓN DE OLAP DEL ESQUEMA 'public'...")

        # Obtener lista de tablas y vistas del esquema 'public'
        schema_query = """
        SELECT table_name, table_type
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_type, table_name;
        """

        try:
            with psycopg2.connect(self.conn_str) as conn:
                schema_df = pd.read_sql_query(schema_query, conn)
        except Exception as e:
            return {'error': f"Error al obtener esquema: {e}"}

        tables = schema_df['table_name'].tolist()
        print(f"📊 Tablas/vistas encontradas en 'public': {tables}")

        dataframes = {}
        successful_extractions = 0
        total_rows_extracted = 0

        for table in tables:
            try:
                df = self.get_table_df(f"public.{table}")
                dataframes[table] = df
                if isinstance(df, pd.DataFrame) and len(df) > 0:
                    successful_extractions += 1
                    total_rows_extracted += len(df)
                    print(f"✅ {table}: {len(df)} filas, {len(df.columns)} cols")
                else:
                    print(f"⚠️  {table}: vacío")
            except Exception as e:
                error_msg = f"Error: {e}"
                dataframes[table] = error_msg
                print(f"❌ {table}: {error_msg}")

        print(f"📊 EXTRACCIÓN COMPLETADA:")
        print(f"✅ Tablas exitosas: {successful_extractions}/{len(tables)}")
        print(f"📈 Total filas extraídas: {total_rows_extracted:,}")

        return dataframes

    @staticmethod
    def _is_valid_identifier(name: str) -> bool:
        """
        Valida un identificador simple de tabla/vista (opcionalmente con schema: schema.table).
        Acepta letras, números, underscore y punto para separar schema.
        """
        if not isinstance(name, str) or len(name) == 0:
            return False
        # Permite schema.tabla o solo tabla; ambos con [A-Za-z_][A-Za-z0-9_]*
        pattern = r"^(?:[A-Za-z_][A-Za-z0-9_]*\.)?[A-Za-z_][A-Za-z0-9_]*$"
        return re.match(pattern, name) is not None

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