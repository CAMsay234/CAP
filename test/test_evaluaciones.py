import unittest
import json
from app import create_app, db
from app.models.evaluacion_neuropsicologica import EvaluacionNeuropsicologica

app = create_app()

class TestEvaluacionesNeuropsicologicas(unittest.TestCase):

    def setUp(self):
        # Crea y activa un contexto de aplicación
        self.app_context = app.app_context()
        self.app_context.push()

        # Configurar el cliente de pruebas de Flask con el contexto de aplicación activo
        self.client = app.test_client()
        self.client.testing = True
        
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

        # Desactivar el contexto de la aplicación
        self.app_context.pop()

    def test_crear_evaluacion(self):
        response = self.client.post('/evaluaciones', json={
            'codigo_hc': 2,
            'id_prueba': 2,
            'id_subprueba': 2,
            'puntaje': 85,
            'media': 100,
            'desviacion_estandar': 15,
            'interpretacion': 'Levemente bajo'
        })
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 201)
        self.assertIn("Evaluación neuropsicológica creada exitosamente", data['message'])

    def test_obtener_evaluaciones(self):
        response = self.client.get('/evaluaciones')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        # Verifica que la respuesta contiene la palabra "Normal" en algún punto
        self.assertTrue(any("Normal" in evaluacion['interpretacion'] for evaluacion in data if isinstance(evaluacion, dict)))

    def test_obtener_evaluacion(self):
        response = self.client.get('/evaluaciones/1/1/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        # Verifica que la respuesta contiene "Normal" como parte de la interpretación
        self.assertIn("Normal", data['interpretacion'])

    def test_actualizar_evaluacion(self):
        response = self.client.put('/evaluaciones/1/1/1', json={
            'puntaje': 95,
            'media': 100,
            'desviacion_estandar': 15,
            'interpretacion': 'Levemente alto'
        })
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Evaluación neuropsicológica actualizada exitosamente", data['message'])

    def test_eliminar_evaluacion(self):
        response = self.client.delete('/evaluaciones/1/1/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)
        self.assertIn("Evaluación neuropsicológica eliminada exitosamente", data['message'])

if __name__ == '__main__':
    unittest.main()
