import logging
import re
from typing import Dict, List, Optional, Tuple

import pandas as pd

from application.use_cases.ia_cases.olap_context_formatter import compact_olap_context, format_olap_context
from infrastructure.repositories.olap_data_repository import OlapDataRepository


logger = logging.getLogger(__name__)


class AnalyzeOlapUseCase:
	REQUIRED_TABLES = ("hecho_ventas", "dim_tiempo")

	def __init__(self) -> None:
		self.repo = OlapDataRepository()

	def _extract_month_year(self, prompt: str) -> Tuple[Optional[int], Optional[int]]:
		pattern = (
			r"(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+"
			r"(de\s+)?(20\d{2})"
		)
		match = re.search(pattern, prompt, re.IGNORECASE)
		if not match:
			return None, None

		month_name = match.group(1).lower()
		year = int(match.group(3))
		month_map = {
			"enero": 1,
			"febrero": 2,
			"marzo": 3,
			"abril": 4,
			"mayo": 5,
			"junio": 6,
			"julio": 7,
			"agosto": 8,
			"septiembre": 9,
			"octubre": 10,
			"noviembre": 11,
			"diciembre": 12,
		}
		return month_map.get(month_name), year

	def run(self, prompt: str) -> Dict[str, object]:
		"""Construye contexto OLAP y responde ante solicitudes temporales específicas."""

		olap_data = self.repo.get_all_olap_data()
		missing = self._detect_missing_tables(olap_data, self.REQUIRED_TABLES)

		month, year = self._extract_month_year(prompt)
		filtered_ctx, extra_missing = self._build_filtered_context(olap_data, month, year)
		missing.extend(extra_missing)

		full_context = format_olap_context(olap_data)
		if len(full_context) > 12000:
			context_text = compact_olap_context(olap_data, max_tables=8, rows_per_table=4)
		else:
			context_text = full_context

		if filtered_ctx:
			context_text = f"{filtered_ctx}\n{context_text}"

		return {
			"context_text": context_text,
			"olap_data": olap_data,
			"prompt": prompt,
			"missing": missing,
		}

	def _detect_missing_tables(self, olap_data: Dict[str, object], required: Tuple[str, ...]) -> List[str]:
		missing: List[str] = []
		for table in required:
			df = olap_data.get(table)
			if not isinstance(df, pd.DataFrame):
				missing.append(table)
		return missing

	def _build_filtered_context(
		self,
		olap_data: Dict[str, object],
		month: Optional[int],
		year: Optional[int],
	) -> Tuple[str, List[str]]:
		if not month or not year:
			return "", []

		hecho = olap_data.get("hecho_ventas")
		dim_tiempo = olap_data.get("dim_tiempo")
		missing: List[str] = []

		if not isinstance(hecho, pd.DataFrame):
			missing.append("hecho_ventas")
		if not isinstance(dim_tiempo, pd.DataFrame):
			missing.append("dim_tiempo")

		if missing:
			return "", missing

		try:
			tiempo_ids = dim_tiempo[
				(dim_tiempo["anio"].astype(int) == year) & (dim_tiempo["mes"].astype(int) == month)
			]["id_tiempo"].unique()

			ventas_mes = hecho[hecho["id_tiempo"].isin(tiempo_ids)]
			if ventas_mes.empty:
				return (
					f"--- Ventas filtradas para {month}/{year} ---\nNo se encontraron registros para ese periodo.",
					[],
				)

			preview = ventas_mes.head(20).to_string(index=False)
			context = (
				f"--- Ventas filtradas para {month}/{year} ---\n"
				f"Filas: {len(ventas_mes)}\n"
				f"Vista previa (hasta 20 filas):\n{preview}"
			)
			return context, []
		except KeyError as exc:
			logger.warning("No se pudieron filtrar ventas por falta de columnas: %s", exc)
			return "", [f"column_missing:{exc}"]
		except Exception as exc:  # pylint: disable=broad-except
			logger.exception("Error filtrando ventas por periodo", exc_info=exc)
			return "", [f"error_filtrado:{exc}"]
