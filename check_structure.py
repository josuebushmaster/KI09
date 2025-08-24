# check_structure.py
import os

def check_structure():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    required_dirs = [
        'domain',
        'domain/entities',
        'domain/repositories',
        'application',
        'application/use_cases',
        'infrastructure',
        'infrastructure/database',
        'infrastructure/repositories',
        'interfaces',
        'interfaces/api',
        'interfaces/api/controllers',
        'interfaces/api/dtos'
    ]
    
    required_files = [
        'domain/__init__.py',
        'domain/entities/__init__.py',
        'domain/repositories/__init__.py',
        'application/__init__.py',
        'application/use_cases/__init__.py',
        'infrastructure/__init__.py',
        'infrastructure/database/__init__.py',
        'infrastructure/repositories/__init__.py',
        'interfaces/__init__.py',
        'interfaces/api/__init__.py',
        'interfaces/api/controllers/__init__.py',
        'interfaces/api/dtos/__init__.py',
        'interfaces/api/main.py',
        'interfaces/api/controllers/categoria_controller.py',
        'interfaces/api/dtos/categoria_dto.py'
    ]
    
    print("Verificando estructura de carpetas...")
    
    for dir_path in required_dirs:
        full_path = os.path.join(base_dir, dir_path)
        if os.path.exists(full_path):
            print(f"✓ Carpeta {dir_path} existe")
        else:
            print(f"✗ Falta carpeta: {dir_path}")
    
    print("\nVerificando archivos __init__.py...")
    
    for file_path in required_files:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            print(f"✓ Archivo {file_path} existe")
        else:
            print(f"✗ Falta archivo: {file_path}")

if __name__ == "__main__":
    check_structure()