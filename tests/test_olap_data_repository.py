import os
import pandas as pd
import types

# Asegurar que la variable de entorno necesaria exista durante las pruebas
os.environ.setdefault('OLAP_DATABASE_URL', 'postgresql://user:pass@localhost/testdb')

from infrastructure.repositories.olap_data_repository import OlapDataRepository


class DummyConn:
    def __enter__(self):
        return object()
    def __exit__(self, exc_type, exc, tb):
        return False

def test_get_table_df_returns_dataframe(monkeypatch):
    # Preparar un DataFrame de ejemplo
    expected_df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

    # Mockear psycopg2.connect para no abrir una conexión real
    import psycopg2
    monkeypatch.setattr(psycopg2, 'connect', lambda conn_str: DummyConn())

    # Mockear pd.read_sql_query para devolver el DataFrame esperado
    monkeypatch.setattr(pd, 'read_sql_query', lambda query, conn: expected_df)

    repo = OlapDataRepository()
    df = repo.get_table_df('ventas')

    assert isinstance(df, pd.DataFrame)
    assert df.equals(expected_df)


def test_get_all_olap_data_handles_errors(monkeypatch):
    # Simular get_table_df: devolver df para la primera tables, y lanzar error para 'otra_tabla'
    sample_df = pd.DataFrame({"x": [10]})

    def fake_get_table_df(self, table_name):
        # Hacer que la última tabla (dim_metodo_pago) falle para comprobar el manejo de errores
        if table_name == 'dim_metodo_pago':
            raise Exception('tabla no existe')
        return sample_df

    monkeypatch.setattr(OlapDataRepository, 'get_table_df', fake_get_table_df)

    repo = OlapDataRepository()
    data = repo.get_all_olap_data()

    # Las tablas definidas en la implementación actual son:
    expected_tables = [
        "hecho_ventas",
        "dim_cliente",
        "dim_producto",
        "dim_tiempo",
        "dim_envio",
        "dim_categoria",
        "dim_metodo_pago",
    ]

    for tbl in expected_tables:
        if tbl == 'dim_metodo_pago':
            # simulamos que esta tabla lanza error en fake_get_table_df
            assert isinstance(data[tbl], str) and data[tbl].startswith('Error:')
        else:
            assert isinstance(data[tbl], pd.DataFrame)
