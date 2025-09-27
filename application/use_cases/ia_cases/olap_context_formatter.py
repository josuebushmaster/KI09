from typing import Dict, List, Tuple

import pandas as pd


def format_olap_context(
    olap_data: Dict[str, object],
    *,
    max_rows: int = 5,
    max_columns: int = 10,
    max_numeric_stats: int = 5,
    max_categorical_stats: int = 3,
) -> str:
    """Genera un texto detallado para IA a partir de los DataFrames OLAP."""

    context_parts: List[str] = []

    for table, df in sorted(olap_data.items()):
        context_parts.append(f"\n--- Tabla: {table} ---")

        if not isinstance(df, pd.DataFrame):
            context_parts.append(f"Error al extraer datos: {df}")
            continue

        rows, cols = len(df), len(df.columns)
        context_parts.append(f"Filas: {rows}, Columnas: {cols}")

        if rows == 0:
            context_parts.append("Tabla vacía.")
            continue

        numeric_stats = _summarize_numeric_columns(df, max_numeric_stats)
        categorical_stats = _summarize_categorical_columns(df, max_categorical_stats)
        null_summary = _summarize_nulls(df)

        if numeric_stats:
            context_parts.append("Variables numéricas:")
            context_parts.extend([f"  - {stat}" for stat in numeric_stats])
        if categorical_stats:
            context_parts.append("Variables categóricas:")
            context_parts.extend([f"  - {stat}" for stat in categorical_stats])
        if null_summary:
            context_parts.append("Nulos por columna:")
            context_parts.extend([f"  - {col}: {count}" for col, count in null_summary])

        preview_df = df.iloc[:max_rows, :max_columns]
        context_parts.append(
            f"Vista previa (primeras {min(max_rows, rows)} filas, hasta {min(max_columns, cols)} columnas):"
        )
        context_parts.append(preview_df.to_string(index=False))

    return "\n".join(context_parts)


def compact_olap_context(
    olap_data: Dict[str, object],
    *,
    max_tables: int = 5,
    rows_per_table: int = 3,
    max_columns: int = 6,
) -> str:
    """Genera un contexto compacto priorizando visibilidad sobre volumen de datos."""

    parts: List[str] = []
    tables = list(sorted(olap_data.items()))[:max_tables]

    for table, df in tables:
        parts.append(f"TABLE: {table}")
        if not isinstance(df, pd.DataFrame):
            parts.append(f"error={df}")
            continue

        parts.append(f"rows={len(df)}, cols={len(df.columns)}")

        if df.empty:
            parts.append("preview=[]")
            continue

        preview_records = (
            df.iloc[:rows_per_table, :max_columns]
            .convert_dtypes()
            .to_dict(orient="records")
        )
        parts.append(f"preview={preview_records}")

    return "\n".join(parts)


def _summarize_numeric_columns(df: pd.DataFrame, limit: int) -> List[str]:
    stats: List[str] = []
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    for col in numeric_cols[:limit]:
        series = df[col].dropna()
        if series.empty:
            stats.append(f"{col}: sin datos numéricos")
            continue
        stats.append(
            f"{col}: media={series.mean():.2f}, mediana={series.median():.2f}, min={series.min():.2f}, max={series.max():.2f}"
        )

    return stats


def _summarize_categorical_columns(df: pd.DataFrame, limit: int) -> List[str]:
    stats: List[str] = []
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    for col in categorical_cols[:limit]:
        series = df[col].dropna()
        if series.empty:
            stats.append(f"{col}: sin datos no numéricos")
            continue
        top_value = series.mode().iloc[0] if not series.mode().empty else "—"
        top_freq = series.value_counts().iloc[0] if not series.value_counts().empty else 0
        stats.append(f"{col}: valor más frecuente='{top_value}' (freq={top_freq})")

    return stats


def _summarize_nulls(df: pd.DataFrame) -> List[Tuple[str, int]]:
    null_counts = df.isna().sum()
    non_zero = null_counts[null_counts > 0]
    return list(non_zero.items())
