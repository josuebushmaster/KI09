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
    # Directorio raíz del proyecto (donde está este script)
    current_dir = Path(__file__).parent
    pycache_count = 0
    pyc_count = 0
    
    if verbose:
        print("🔍 Buscando archivos __pycache__ y .pyc...")
        print(f"Directorio de búsqueda: {current_dir}")
        print("-" * 50)
    
    # Eliminar carpetas __pycache__
    for pycache_dir in current_dir.rglob('__pycache__'):
        if pycache_dir.is_dir():
            try:
                shutil.rmtree(pycache_dir)
                pycache_count += 1
                if verbose:
                    print(f"✓ Eliminada: {pycache_dir.relative_to(current_dir)}")
            except Exception as e:
                if verbose:
                    print(f"✗ Error eliminando {pycache_dir.relative_to(current_dir)}: {e}")
    
    # Eliminar archivos .pyc
    for pyc_file in current_dir.rglob('*.pyc'):
        if pyc_file.is_file():
            try:
                pyc_file.unlink()
                pyc_count += 1
                if verbose:
                    print(f"✓ Eliminado: {pyc_file.relative_to(current_dir)}")
            except Exception as e:
                if verbose:
                    print(f"✗ Error eliminando {pyc_file.relative_to(current_dir)}: {e}")
    
    # Eliminar archivos .pyo (opcionales)
    pyo_count = 0
    for pyo_file in current_dir.rglob('*.pyo'):
        if pyo_file.is_file():
            try:
                pyo_file.unlink()
                pyo_count += 1
                if verbose:
                    print(f"✓ Eliminado: {pyo_file.relative_to(current_dir)}")
            except Exception as e:
                if verbose:
                    print(f"✗ Error eliminando {pyo_file.relative_to(current_dir)}: {e}")
    
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
        
        current_dir = Path(__file__).parent
        for pycache_dir in current_dir.rglob('__pycache__'):
            if pycache_dir.is_dir():
                print(f"📁 {pycache_dir.relative_to(current_dir)}")
        
        for pyc_file in current_dir.rglob('*.pyc'):
            if pyc_file.is_file():
                print(f"📄 {pyc_file.relative_to(current_dir)}")
        
        for pyo_file in current_dir.rglob('*.pyo'):
            if pyo_file.is_file():
                print(f"📄 {pyo_file.relative_to(current_dir)}")
        
        print("-" * 50)
        print("💡 Ejecuta sin --dry-run para eliminar realmente")
        return
    
    # Ejecutar limpieza
    limpiar_pycache(verbose=not args.silent)

if __name__ == "__main__":
    main()