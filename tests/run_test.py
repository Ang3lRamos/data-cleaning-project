"""
run_tests.py
============
Script para ejecutar todos los tests del proyecto

Uso: python run_tests.py
"""

import subprocess
import sys

def ejecutar_tests():
    """
    Ejecuta todos los tests con pytest
    """
    
    print("="*60)
    print("EJECUTANDO TESTS DEL PROYECTO")
    print("="*60)
    
    # Comandos de pytest
    comandos = [
        # Tests con coverage
        ["pytest", "tests/", "-v", "--tb=short"],
        
        # Tests con reporte detallado
        # ["pytest", "tests/", "-v", "--tb=long", "--showlocals"],
        
        # Tests con coverage (si tienes pytest-cov instalado)
        # ["pytest", "tests/", "--cov=src", "--cov-report=html"]
    ]
    
    for i, comando in enumerate(comandos, 1):
        print(f"\nEjecutando comando {i}/{len(comandos)}:")
        print(f"  {' '.join(comando)}")
        print("-"*60)
        
        try:
            resultado = subprocess.run(comando, check=True)
            
            if resultado.returncode == 0:
                print("\nTests completados exitosamente")
            else:
                print(f"\nAlgunos tests fallaron (codigo: {resultado.returncode})")
                
        except subprocess.CalledProcessError as e:
            print(f"\nError al ejecutar tests: {e}")
            sys.exit(1)
        except FileNotFoundError:
            print("\nError: pytest no esta instalado")
            print("Instala con: pip install pytest")
            sys.exit(1)
    
    print("\n" + "="*60)
    print("RESUMEN DE TESTS COMPLETADO")
    print("="*60)

if __name__ == "__main__":
    ejecutar_tests()