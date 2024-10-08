import unittest
from app import app, db
from app.models.evaluacion_neuropsicologica import EvaluacionNeuropsicologica

class TestEvaluacionesNeuropsicologicas(unittest.TestCase):

    def setUp(self):
        # Configurar el cliente de pruebas de Flask y la base de datos
        self.app = app.test_client()
        self.app.testing = True

        # Crear tablas en la base de datos (si no existen)
        db.create_all()

        # Insertar una evaluación de ejemplo para las pruebas
        evaluacion = EvaluacionNeuropsicologica(
            codigo_hc=1,
            id_prueba=1,
            id_subprueba=1,
            puntaje=90,
            media=100,
            desviacion_estandar=15,
            interpretacion="Normal"
        )
        db.session.add(evaluacion)
        db.session.commit()

    def tearDown(self):
        # Eliminar todo después de las pruebas
        db.session.remove()
        db.drop_all()

    # Prueba para la creación de una evaluación (POST)
    def test_crear_evaluacion(self):
        response = self.app.post('/evaluaciones', json={
            'codigo_hc': 2,
            'id_prueba': 2,
            'id_subprueba': 2,
            'puntaje': 85,
            'media': 100,
            'desviacion_estandar': 15,
            'interpretacion': 'Levemente bajo'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn("Evaluación neuropsicológica creada exitosamente", response.get_data(as_text=True))

    # Prueba para obtener todas las evaluaciones (GET)
    def test_obtener_evaluaciones(self):
        response = self.app.get('/evaluaciones')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Normal", response.data)

    # Prueba para obtener una evaluación por clave primaria (GET)
    def test_obtener_evaluacion(self):
        response = self.app.get('/evaluaciones/1/1/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Normal", response.data)

    # Prueba para actualizar una evaluación (PUT)
    def test_actualizar_evaluacion(self):
        response = self.app.put('/evaluaciones/1/1/1', json={
            'puntaje': 95,
            'media': 100,
            'desviacion_estandar': 15,
            'interpretacion': 'Levemente alto'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Evaluación neuropsicológica actualizada exitosamente", response.get_data(as_text=True))

    # Prueba para eliminar una evaluación (DELETE)
    def test_eliminar_evaluacion(self):
        response = self.app.delete('/evaluaciones/1/1/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Evaluación neuropsicológica eliminada exitosamente", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
