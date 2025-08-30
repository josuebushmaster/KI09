# check_structure.py
import os

def check_structure():
    # directorio del script y raíz del proyecto (parent de scripts)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)
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
    
    print(f"Verificando estructura de carpetas (base: {base_dir})...")

    for dir_path in required_dirs:
        full_path = os.path.join(base_dir, dir_path)
        rel = os.path.relpath(full_path, base_dir)
        if os.path.exists(full_path):
            print(f"✓ Carpeta {rel} existe")
        else:
            print(f"✗ Falta carpeta: {rel}")
    
    print("\nVerificando archivos __init__.py y archivos requeridos...")

    for file_path in required_files:
        full_path = os.path.join(base_dir, file_path)
        rel = os.path.relpath(full_path, base_dir)
        if os.path.exists(full_path):
            print(f"✓ Archivo {rel} existe")
        else:
            print(f"✗ Falta archivo: {rel}")

if __name__ == "__main__":
    check_structure()