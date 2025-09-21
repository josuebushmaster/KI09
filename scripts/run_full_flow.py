from pathlib import Path
import sys
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from application.use_cases.ia_cases.analyze_olap_use_case import AnalyzeOlapUseCase
from scripts import grok_client

if __name__ == '__main__':
    use_case = AnalyzeOlapUseCase()
    try:
        uc = use_case.run('Genera un resumen de tendencias y problemas en mis ventas')
        ctx = uc.get('context_text', '')
        print('Context size:', len(ctx))
        # llamar al cliente grok
        resp = grok_client.analyze_prompt('Genera un resumen de tendencias y problemas en mis ventas', context_text=ctx)
        print('\n--- RESPUESTA DEL MODELO ---')
        print(resp)
    except Exception as e:
        print('Error ejecutando flujo completo:', e)
