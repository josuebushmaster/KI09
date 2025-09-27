import os
from contextlib import contextmanager

import pandas as pd

# Asegurar que la variable de entorno necesaria exista durante las pruebas
os.environ.setdefault("OLAP_DATABASE_URL", "postgresql://user:pass@localhost/testdb")

from infrastructure.repositories.olap_data_repository import OlapDataRepository


@contextmanager
def _fake_connection():
    yield object()


def test_get_table_df_returns_dataframe(monkeypatch):
    monkeypatch.setenv("OLAP_TABLES", "ventas")

    expected_df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

    monkeypatch.setattr(OlapDataRepository, "_get_connection", lambda self: _fake_connection())
    monkeypatch.setattr(OlapDataRepository, "_count_rows", lambda self, _: len(expected_df))
    monkeypatch.setattr(pd, "read_sql_query", lambda query, conn: expected_df)

    repo = OlapDataRepository()
    df = repo.get_table_df("ventas")

    assert isinstance(df, pd.DataFrame)
    assert df.equals(expected_df)


def test_get_all_olap_data_handles_errors(monkeypatch):
    monkeypatch.setenv("OLAP_TABLES", "hecho_ventas,dim_metodo_pago")

    sample_df = pd.DataFrame({"x": [10]})

    def fake_get_table_df(self, table_name, *, use_chunking=True):  # noqa: ARG001
        if table_name.endswith("dim_metodo_pago"):
            raise Exception("tabla no existe")
        return sample_df

    monkeypatch.setattr(OlapDataRepository, "_get_connection", lambda self: _fake_connection())
    monkeypatch.setattr(OlapDataRepository, "_count_rows", lambda self, _: len(sample_df))
    monkeypatch.setattr(OlapDataRepository, "get_table_df", fake_get_table_df)

    repo = OlapDataRepository()
    data = repo.get_all_olap_data()

    assert isinstance(data["hecho_ventas"], pd.DataFrame)
    assert isinstance(data["dim_metodo_pago"], str)
    assert data["dim_metodo_pago"].startswith("Error:")
