import re
from typing import Dict, Any, List
import pandas as pd


def _extract_numbers(text: str) -> List[str]:
    # Extrae números y porcentajes sencillos
    return re.findall(r"\d+[\.,]?\d*%?", text)


def _search_value_in_df(df: pd.DataFrame, term: str) -> bool:
    # Busca term en todas las columnas de tipo objeto (string)
    try:
        for col in df.select_dtypes(include=['object', 'string']).columns:
            # lowercase search
            vals = df[col].astype(str).str.lower()
            if vals.str.contains(term.lower(), na=False).any():
                return True
    except Exception:
        return False
    return False


def verify_ai_response(ai_response: Dict[str, Any], olap_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Heurísticamente verifica la respuesta de la IA contra los DataFrames OLAP.
    - Comprueba si las tendencias/recomendaciones mencionan tablas o valores existentes.
    - Detecta reclamaciones numéricas (nº o %) y marca si no se puede verificar.
    Retorna un dict con 'verified' (bool), 'issues' (lista) y 'evidence' (lista).
    """
    issues: List[str] = []
    evidence: List[str] = []

    # Normalizar mapping de tablas -> df
    df_map = {k: v for k, v in olap_data.items() if isinstance(v, pd.DataFrame)}

    # Si la respuesta no es un dict, no podemos verificar estructuradamente
    if not isinstance(ai_response, dict):
        return {"verified": False, "issues": ["ai_response_not_structured"], "evidence": []}

    # Revisar missing_fields declarado por la IA
    missing_fields = ai_response.get('missing_fields', []) if isinstance(ai_response.get('missing_fields', []), list) else []
    for mf in missing_fields:
        # Si la IA listó un campo faltante que sí existe en olap_data, marcar inconsistencia
        for table, df in df_map.items():
            if isinstance(df, pd.DataFrame) and mf.lower() in (', '.join(map(str, df.columns))).lower():
                issues.append(f"IA dijo falta '{mf}' pero la tabla '{table}' contiene esa columna")

    # Función auxiliar para verificar una frase (trend/recommendation)
    def _verify_phrase(phrase: str, kind: str):
        nums = _extract_numbers(phrase)
        found_grounding = False
        # Buscar menciones explícitas de tablas
        for table, df in df_map.items():
            if table.lower() in phrase.lower():
                evidence.append(f"{kind} menciona tabla existente: {table}")
                found_grounding = True
        # Buscar valores como nombres de producto/categoría dentro de datos
        # Extraer palabras clave (n-grams simples)
        tokens = re.findall(r"[A-Za-zÀ-ÿ0-9_]{3,}", phrase)
        for t in tokens[:6]:
            for table, df in df_map.items():
                try:
                    if _search_value_in_df(df, t):
                        evidence.append(f"{kind} contiene término encontrado en '{table}': {t}")
                        found_grounding = True
                        raise StopIteration
                except StopIteration:
                    break
        if nums and not found_grounding:
            issues.append(f"{kind} contiene cifras {nums} pero no se encontró grounding en tablas o valores")
        if not nums and not found_grounding:
            # No cifra y tampoco grounding; marcar como posible invento si es afirmación concreta
            if len(phrase.split()) > 6:
                issues.append(f"{kind} posiblemente no verificada: '{phrase[:80]}'")

    for t in ai_response.get('tendencias', []) or []:
        _verify_phrase(t, 'tendencia')
    for r in ai_response.get('recomendaciones', []) or []:
        _verify_phrase(r, 'recomendación')

    verified = len(issues) == 0
    return {"verified": verified, "issues": issues, "evidence": evidence}
