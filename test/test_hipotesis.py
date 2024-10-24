import unittest
import json
from app import create_app, db
from app.models.hipotesis import Hipotesis

app = create_app()

class TestHipotesis(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        self.client = app.test_client()
        self.client.testing = True

        db.create_all()

        # Crear una hipótesis de ejemplo para las pruebas
        hipotesis = Hipotesis(descripcion="Hipótesis inicial")
        db.session.add(hipotesis)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear_hipotesis(self):
        response = self.client.post('/hipotesis', json={
            'descripcion': 'Nueva hipótesis'
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Hipótesis creada exitosamente', data['message'])

    def test_obtener_todas_hipotesis(self):
        response = self.client.get('/hipotesis')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data) > 0)

    def test_obtener_hipotesis_por_id(self):
        response = self.client.get('/hipotesis/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['descripcion'], 'Hipótesis inicial')

    def test_obtener_hipotesis_no_existente(self):
        response = self.client.get('/hipotesis/99')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Hipótesis no encontrada', data['error'])

    def test_actualizar_hipotesis(self):
        response = self.client.put('/hipotesis/1', json={
            'descripcion': 'Hipótesis actualizada'
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Hipótesis actualizada exitosamente', data['message'])

        # Verificar la actualización
        response = self.client.get('/hipotesis/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['descripcion'], 'Hipótesis actualizada')

    def test_eliminar_hipotesis(self):
        response = self.client.delete('/hipotesis/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Hipótesis eliminada exitosamente', data['message'])

        # Verificar que se eliminó
        response = self.client.get('/hipotesis/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
