import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from infrastructure.repositories.postgres_categoria_repository import PostgresCategoriaRepository

repo = PostgresCategoriaRepository()
try:
    cats = repo.listar_todas()
    print('Encontradas', len(cats))
    print(cats[:5])
except Exception as e:
    import traceback
    traceback.print_exc()
    print('ERROR:', e)
