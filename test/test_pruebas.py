import unittest
import json
from app import create_app, db
from app.models.prueba import Prueba

app = create_app()

class TestPruebas(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        self.client = app.test_client()
        self.client.testing = True

        db.create_all()

        # Crear una prueba de ejemplo
        prueba = Prueba(nombre="Prueba Inicial")
        db.session.add(prueba)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear_prueba(self):
        response = self.client.post('/pruebas', json={
            'nombre': 'Prueba Nueva'
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Prueba creada exitosamente', data['message'])

    def test_obtener_pruebas(self):
        response = self.client.get('/pruebas')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data) > 0)

    def test_obtener_prueba(self):
        response = self.client.get('/pruebas/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['nombre'], 'Prueba Inicial')

    def test_obtener_prueba_no_existente(self):
        response = self.client.get('/pruebas/99')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Prueba no encontrada', data['error'])

    def test_actualizar_prueba(self):
        response = self.client.put('/pruebas/1', json={
            'nombre': 'Prueba Actualizada'
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Prueba actualizada exitosamente', data['message'])

        # Verificar actualización
        response = self.client.get('/pruebas/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['nombre'], 'Prueba Actualizada')

    def test_eliminar_prueba(self):
        response = self.client.delete('/pruebas/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Prueba eliminada exitosamente', data['message'])

        # Verificar que se eliminó
        response = self.client.get('/pruebas/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
