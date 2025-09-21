import pandas as pd

def format_olap_context(olap_data: dict, max_rows: int = 5) -> str:
    """
    Recibe un dict de DataFrames OLAP y genera un texto resumen para IA.
    Incluye estadísticas y vista previa de cada tabla.
    """
    context_parts = []
    for table, df in olap_data.items():
        context_parts.append(f"\n--- Tabla: {table} ---")
        if isinstance(df, pd.DataFrame):
            context_parts.append(f"Filas: {len(df)}, Columnas: {len(df.columns)}")
            # Estadísticas básicas
            try:
                stats = df.describe(include='all').transpose().to_string()
                context_parts.append(f"Estadísticas:\n{stats}")
            except Exception:
                context_parts.append("No se pudieron calcular estadísticas.")
            # Vista previa
            preview = df.head(max_rows).to_string(index=False)
            context_parts.append(f"Vista previa (primeras {max_rows} filas):\n{preview}")
        else:
            context_parts.append(f"Error al extraer datos: {df}")
    return '\n'.join(context_parts)


def compact_olap_context(olap_data: dict, max_tables: int = 5, rows_per_table: int = 3) -> str:
    """
    Genera un contexto compacto: por cada tabla devuelve nombre, filas, columnas, y up to `rows_per_table` de vista previa.
    Limitado a `max_tables` tablas (las más relevantes se toman en orden de aparición).
    """
    parts = []
    tables = list(olap_data.items())[:max_tables]
    for table, df in tables:
        parts.append(f"TABLE: {table}")
        if isinstance(df, pd.DataFrame):
            parts.append(f"rows={len(df)}, cols={len(df.columns)}")
            try:
                preview = df.head(rows_per_table).to_dict(orient='records')
                parts.append(f"preview={preview}")
            except Exception:
                parts.append("preview_error")
        else:
            parts.append(f"error={df}")
    return '\n'.join(parts)
