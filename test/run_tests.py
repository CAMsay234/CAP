import os
import sys
import unittest

# Añadir el directorio raíz de CAP al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar las clases de prueba manualmente
from test_evaluaciones import TestEvaluacionesNeuropsicologicas
from test_pacientes import TestPacientes
from test_areas import TestAreas
from test_historias import TestHistoriasClinicas
from test_auth import TestAuth
from test_comentarios import TestComentarios
from test_conversiones import TestConversiones
from test_diagnosticos import TestDiagnosticos  # Agregar importación de Diagnósticos
from test_estado_mental import TestEstadoMental  # Nueva importación
from test_hipotesis import TestHipotesis  
from test_nivel_escolaridad import TestNivelEscolaridad
from test_pruebas import TestPruebas  # Nueva importación
from test_seguimientos import TestSeguimientos  # Nueva importación
from test_sub_pruebas import TestSubPruebas  # Nueva importación

def suite():
    suite = unittest.TestSuite()
    suite.addTests([
        unittest.defaultTestLoader.loadTestsFromTestCase(TestEvaluacionesNeuropsicologicas),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestPacientes),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestAreas),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestHistoriasClinicas),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestAuth),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestComentarios),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestConversiones),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestDiagnosticos),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestEstadoMental),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestHipotesis),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestNivelEscolaridad),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestPruebas),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestSeguimientos),
        unittest.defaultTestLoader.loadTestsFromTestCase(TestSubPruebas)
    ])
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    if not result.wasSuccessful():
        sys.exit(1)