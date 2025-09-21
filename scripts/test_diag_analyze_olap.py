import sys
from pathlib import Path

# Asegurar que la raíz del proyecto está en sys.path para poder importar las capas locales
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from application.use_cases.ia_cases.analyze_olap_use_case import AnalyzeOlapUseCase


if __name__ == '__main__':
    use_case = AnalyzeOlapUseCase()
    try:
        result = use_case.run('diagnostico: generar contexto')
        olap = result.get('olap_data', {})
        ctx = result.get('context_text', '')
        print('--- DIAGNOSTICO OLAP ---')
        for table, val in olap.items():
            if hasattr(val, 'shape'):
                print(f'{table}: DataFrame filas={val.shape[0]} cols={val.shape[1]}')
            else:
                print(f'{table}: ERROR -> {val}')
        print('--- CONTEXT SIZE ---')
        print(f'context_text length: {len(ctx)} chars')
    except Exception as e:
        print('Error ejecutando el caso de uso:', e)
