import os
import sys
import unittest

# Añadir el directorio raíz de CAP
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Imprimir sys.path para verificar que contiene la ruta correcta
print(sys.path)

# Importa las pruebas
from test_evaluaciones import TestEvaluacionesNeuropsicologicas

# Ejecuta las pruebas
if __name__ == '__main__':
    unittest.main()


# Ejecutar el script con el siguiente comando
# python test/run_tests.py