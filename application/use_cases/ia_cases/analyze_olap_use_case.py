from infrastructure.repositories.olap_data_repository import OlapDataRepository
from application.use_cases.ia_cases.olap_context_formatter import format_olap_context, compact_olap_context
import re


class AnalyzeOlapUseCase:
	def __init__(self):
		self.repo = OlapDataRepository()

	def _extract_month_year(self, prompt: str):
		# Buscar patrones como "enero 2024" o "enero de 2024"
		m = re.search(r"(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+(de\s+)?(20\d{2})", prompt, re.IGNORECASE)
		if not m:
			return None, None
		month_name = m.group(1).lower()
		year = int(m.group(3))
		month_map = {
			'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
			'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
		}
		return month_map.get(month_name), year

	def run(self, prompt: str) -> dict:
		"""
		Extrae datos OLAP, construye contexto y si el prompt solicita un mes específico,
		filtra las ventas para ese mes y devuelve contexto específico. Si faltan datos,
		retorna información sobre qué falta en el campo `missing`.
		"""
		olap_data = self.repo.get_all_olap_data()

		# Intentar extraer mes y año del prompt
		month, year = self._extract_month_year(prompt)

		missing = []
		filtered_ctx = ''

		# Si se solicitó un mes, tratar de filtrar usando tablas comunes
		if month and year:
			# Verificar que exista la tabla de hechos y la dimensión tiempo
			hecho = olap_data.get('hecho_ventas')
			dim_t = olap_data.get('dim_tiempo')
			if hecho is None:
				missing.append('hecho_ventas')
			if dim_t is None:
				missing.append('dim_tiempo')

			if not missing:
				try:
					# Suponer que dim_tiempo tiene columnas 'id_tiempo', 'anio', 'mes'
					# y que hecho_ventas tiene 'id_tiempo' como FK
					# Filtrar dim_tiempo para obtener ids del mes/año
					tiempo_ids = dim_t[(dim_t['anio'] == year) & (dim_t['mes'] == month)]['id_tiempo'].unique()
					ventas_mes = hecho[hecho['id_tiempo'].isin(tiempo_ids)]
					# Construir contexto compacto de ventas de ese mes
					filtered_ctx = f"--- Ventas filtradas para {month}/{year} ---\n"
					filtered_ctx += f"Filas: {len(ventas_mes)}\n"
					filtered_ctx += ventas_mes.head(10).to_string(index=False)
				except Exception as e:
					missing.append(f'error_filtrado:{e}')

		# Generar contexto completo o compacto según tamaño
		full_ctx = format_olap_context(olap_data)
		if len(full_ctx) > 10000:
			context_text = compact_olap_context(olap_data)
		else:
			context_text = full_ctx

		# Si tenemos filtered_ctx, prefijarlo al context_text para priorizarlo
		if filtered_ctx:
			context_text = filtered_ctx + '\n' + context_text

		result = {
			'context_text': context_text,
			'olap_data': olap_data,
			'prompt': prompt,
			'missing': missing
		}
		return result
