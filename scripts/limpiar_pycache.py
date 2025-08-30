#!/usr/bin/env python3
"""
Script para eliminar archivos __pycache__ y .pyc
Ejecutar: python limpiar_pycache.py
"""

import shutil
from pathlib import Path
import argparse

def limpiar_pycache(verbose=True):
    """
    Elimina todas las carpetas __pycache__ y archivos .pyc en el proyecto
    """
    # Directorio del script y directorio raíz del proyecto (parent de scripts)
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    pycache_count = 0
    pyc_count = 0
    
    if verbose:
        print("🔍 Buscando archivos __pycache__ y .pyc...")
        print(f"Directorio de búsqueda: {project_root}")
        print("-" * 50)
    
    # Eliminar carpetas __pycache__
    for pycache_dir in project_root.rglob('__pycache__'):
        if pycache_dir.is_dir():
            try:
                shutil.rmtree(pycache_dir)
                pycache_count += 1
                if verbose:
                    print(f"✓ Eliminada: {pycache_dir.relative_to(project_root)}")
            except Exception as e:
                if verbose:
                    print(f"✗ Error eliminando {pycache_dir.relative_to(project_root)}: {e}")
    
    # Eliminar archivos .pyc
    for pyc_file in project_root.rglob('*.pyc'):
        if pyc_file.is_file():
            try:
                pyc_file.unlink()
                pyc_count += 1
                if verbose:
                    print(f"✓ Eliminado: {pyc_file.relative_to(project_root)}")
            except Exception as e:
                if verbose:
                    print(f"✗ Error eliminando {pyc_file.relative_to(project_root)}: {e}")
    
    # Eliminar archivos .pyo (opcionales)
    pyo_count = 0
    for pyo_file in project_root.rglob('*.pyo'):
        if pyo_file.is_file():
            try:
                pyo_file.unlink()
                pyo_count += 1
                if verbose:
                    print(f"✓ Eliminado: {pyo_file.relative_to(project_root)}")
            except Exception as e:
                if verbose:
                    print(f"✗ Error eliminando {pyo_file.relative_to(project_root)}: {e}")
    
    if verbose:
        print("-" * 50)
        print(f"✅ Limpieza completada!")
        print(f"   • Carpetas __pycache__ eliminadas: {pycache_count}")
        print(f"   • Archivos .pyc eliminados: {pyc_count}")
        print(f"   • Archivos .pyo eliminados: {pyo_count}")
    
    return pycache_count, pyc_count, pyo_count

def main():
    """Función principal con argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(description='Limpiar archivos __pycache__ y .pyc')
    parser.add_argument('--silent', '-s', action='store_true', 
                       help='Modo silencioso (sin output)')
    parser.add_argument('--dry-run', '-d', action='store_true',
                       help='Mostrar qué se eliminaría sin hacer cambios')
    
    args = parser.parse_args()
    
    if args.dry_run:
        print("🔍 MODO SIMULACIÓN: Mostrando qué se eliminaría")
        print("Los siguientes archivos serían eliminados:")
        print("-" * 50)

        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        for pycache_dir in project_root.rglob('__pycache__'):
            if pycache_dir.is_dir():
                print(f"📁 {pycache_dir.relative_to(project_root)}")

        for pyc_file in project_root.rglob('*.pyc'):
            if pyc_file.is_file():
                print(f"📄 {pyc_file.relative_to(project_root)}")

        for pyo_file in project_root.rglob('*.pyo'):
            if pyo_file.is_file():
                print(f"📄 {pyo_file.relative_to(project_root)}")

        print("-" * 50)
        print("💡 Ejecuta sin --dry-run para eliminar realmente")
        return
    
    # Ejecutar limpieza
    limpiar_pycache(verbose=not args.silent)

if __name__ == "__main__":
    main()