"""Repositorio para la extracción de datos OLAP."""

from __future__ import annotations

import logging
import os
import re
from contextlib import contextmanager
from typing import Dict, List, Optional, Tuple

import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("OLAP_REPOSITORY")
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
    logger.addHandler(handler)
logger.setLevel(os.getenv("OLAP_LOG_LEVEL", "INFO").upper())


class OlapDataRepository:
    """Permite extraer datos de un almacén OLAP de forma controlada."""

    def __init__(self) -> None:
        self.conn_str = os.getenv("OLAP_DATABASE_URL")
        if not self.conn_str:
            raise RuntimeError("OLAP_DATABASE_URL no encontrada en variables de entorno")

        self.schema = os.getenv("OLAP_SCHEMA", "public")
        self.chunk_size = max(1000, int(os.getenv("OLAP_CHUNK_SIZE", "5000")))
        self.timeout_ms = self._resolve_timeout_ms()
        self.explicit_tables = self._parse_table_list(os.getenv("OLAP_TABLES"))
        self.max_tables = int(os.getenv("OLAP_MAX_TABLES", "0"))

        self._cached_schema: Optional[List[Tuple[str, str]]] = None
        logger.debug(
            "Repositorio OLAP inicializado",
            extra={"schema": self.schema, "chunk_size": self.chunk_size, "timeout_ms": self.timeout_ms},
        )

    def get_table_df(self, table_name: str, *, use_chunking: bool = True) -> pd.DataFrame:
        """Extrae toda la data de una tabla/vista y la retorna como DataFrame."""

        if not self._is_valid_identifier(table_name):
            raise ValueError(f"Nombre de tabla inválido: {table_name}")

        qualified_name = self._qualify_table(table_name)
        logger.debug("Extrayendo tabla %s (chunking=%s)", qualified_name, use_chunking)

        total_rows = self._count_rows(qualified_name)
        logger.info("%s -> %s filas totales", qualified_name, total_rows)

        if use_chunking and total_rows > self.chunk_size:
            logger.info(
                "%s excede chunk_size=%s. Leyendo en bloques...",
                qualified_name,
                self.chunk_size,
            )
            return self._read_in_chunks(qualified_name, total_rows)

        with self._get_connection() as conn:
            query = f"SELECT * FROM {qualified_name}"
            df = pd.read_sql_query(query, conn)
        logger.debug("%s -> %s filas x %s columnas", qualified_name, len(df), len(df.columns))
        return df

    def get_all_olap_data(self) -> Dict[str, object]:
        """Extrae información de todas las tablas/vistas configuradas en el esquema OLAP."""

        tables = self._resolve_table_list()
        if self.max_tables and len(tables) > self.max_tables:
            logger.warning(
                "La cantidad de tablas (%s) supera OLAP_MAX_TABLES=%s. Solo se procesarán las primeras %s.",
                len(tables),
                self.max_tables,
                self.max_tables,
            )
            tables = tables[: self.max_tables]

        logger.info("Extrayendo %s tablas/vistas del esquema '%s'", len(tables), self.schema)

        dataframes: Dict[str, object] = {}
        total_rows = 0
        successful = 0

        for table in tables:
            key = self._normalize_identifier(table)
            qualified = self._qualify_table(table)
            try:
                df = self.get_table_df(qualified)
                dataframes[key] = df
                if isinstance(df, pd.DataFrame):
                    total_rows += len(df)
                    successful += 1
                    logger.info("✅ %s extraída (%s filas, %s columnas)", key, len(df), len(df.columns))
                else:
                    logger.warning("⚠️  %s retornó un objeto no esperado (%s)", key, type(df))
            except Exception as exc:  # pylint: disable=broad-except
                error_msg = f"Error: {exc}"
                dataframes[key] = error_msg
                logger.error("❌ %s no pudo extraerse: %s", key, exc)

        logger.info(
            "Extracción OLAP completada: %s/%s tablas exitosas. Total filas: %s",
            successful,
            len(tables),
            total_rows,
        )

        return dataframes

    # ------------------------------------------------------------------
    # Utilidades internas
    # ------------------------------------------------------------------

    def _resolve_table_list(self) -> List[str]:
        if self.explicit_tables:
            return self.explicit_tables
        schema_objects = self._discover_schema_objects()
        return [name for name, _ in schema_objects]

    def _discover_schema_objects(self) -> List[Tuple[str, str]]:
        if self._cached_schema is not None:
            return self._cached_schema

        query = (
            "SELECT table_name, table_type "
            "FROM information_schema.tables "
            "WHERE table_schema = %s "
            "ORDER BY table_type, table_name"
        )
        with self._get_connection() as conn:
            df = pd.read_sql_query(query, conn, params=(self.schema,))

        objects = [(row["table_name"], row["table_type"]) for _, row in df.iterrows()]
        self._cached_schema = objects
        logger.info("Schema '%s': %s tablas/vistas encontradas", self.schema, len(objects))
        return objects

    def _count_rows(self, qualified_name: str) -> int:
        query = f"SELECT COUNT(*) AS total FROM {qualified_name}"
        with self._get_connection() as conn:
            result = pd.read_sql_query(query, conn)
        return int(result.iloc[0]["total"])

    def _read_in_chunks(self, qualified_name: str, total_rows: int) -> pd.DataFrame:
        chunks: List[pd.DataFrame] = []
        offset = 0

        with self._get_connection() as conn:
            while offset < total_rows:
                query = (
                    f"SELECT * FROM {qualified_name} "
                    f"LIMIT {self.chunk_size} OFFSET {offset}"
                )
                chunk = pd.read_sql_query(query, conn)
                if chunk.empty:
                    break
                chunks.append(chunk)
                offset += self.chunk_size
                logger.debug(
                    "%s -> chunk %s (%s filas acumuladas)",
                    qualified_name,
                    len(chunks),
                    sum(len(c) for c in chunks),
                )

        if not chunks:
            return pd.DataFrame()
        return pd.concat(chunks, ignore_index=True)

    def _qualify_table(self, table_name: str) -> str:
        if "." in table_name:
            return table_name
        return f"{self.schema}.{table_name}"

    @staticmethod
    def _normalize_identifier(identifier: str) -> str:
        return identifier.split(".")[-1]

    @staticmethod
    def _parse_table_list(raw: Optional[str]) -> List[str]:
        if not raw:
            return []
        return [item.strip() for item in raw.split(",") if item.strip()]

    @staticmethod
    def _resolve_timeout_ms() -> int:
        custom_ms = os.getenv("OLAP_TIMEOUT_MS")
        if custom_ms:
            return int(custom_ms)
        timeout_seconds = float(os.getenv("OLAP_TIMEOUT", "300"))
        return int(timeout_seconds * 1000)

    @staticmethod
    def _is_valid_identifier(name: str) -> bool:
        if not isinstance(name, str) or not name:
            return False
        pattern = r"^(?:[A-Za-z_][A-Za-z0-9_]*\.)?[A-Za-z_][A-Za-z0-9_]*$"
        return re.match(pattern, name) is not None

    @contextmanager
    def _get_connection(self):
        conn = psycopg2.connect(self.conn_str)
        try:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute("SET statement_timeout = %s", (self.timeout_ms,))
            yield conn
        finally:
            conn.close()


if __name__ == "__main__":
    repository = OlapDataRepository()
    datasets = repository.get_all_olap_data()
    for table_name, df in datasets.items():
        if isinstance(df, pd.DataFrame):
            print(f"Tabla: {table_name} -> filas: {len(df)}, columnas: {len(df.columns)}")
        else:
            print(f"Tabla: {table_name} -> {df}")