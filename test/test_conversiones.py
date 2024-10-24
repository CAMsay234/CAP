import unittest
import json
from app import create_app, db
from app.models.conversion import Conversion

app = create_app()

class TestConversiones(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        self.client = app.test_client()
        self.client.testing = True

        db.create_all()

        # Crear una conversión de ejemplo para las pruebas
        conversion = Conversion(
            codigo_hc=1,
            id_prueba=101,
            id_subprueba=201,
            suma_puntacion=80.0,
            puntacion_compuesta=90.0,
            memoria_trabajo=85.0,
            rango_percentil=75.0,
            intervalo_confianza=70.5 
        )
        db.session.add(conversion)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_conversion(self):
        response = self.client.post('/conversiones', json={
            'codigo_hc': 2,
            'id_prueba': 102,
            'id_subprueba': 202,
            'suma_puntacion': 85.0,
            'puntacion_compuesta': 95.0,
            'memoria_trabajo': 88.0,
            'rango_percentil': 80.0,
            'intervalo_confianza': 75.5  # Usando un float válido
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Conversion created successfully', data['message'])

    def test_get_conversion(self):
        response = self.client.get('/conversiones/1/101/201')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['suma_puntacion'], 80.0)

    def test_update_conversion(self):
        response = self.client.put('/conversiones/1/101/201', json={
            'suma_puntacion': 90.0,
            'puntacion_compuesta': 95.0
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Conversion updated successfully', data['message'])

        # Verificar si se actualizaron los datos
        response = self.client.get('/conversiones/1/101/201')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['suma_puntacion'], 90.0)
        self.assertEqual(data['puntacion_compuesta'], 95.0)

    def test_delete_conversion(self):
        response = self.client.delete('/conversiones/1/101/201')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Conversion deleted successfully', data['message'])

        # Verificar que se eliminó
        response = self.client.get('/conversiones/1/101/201')
        self.assertEqual(response.status_code, 404)

    def test_get_nonexistent_conversion(self):
        response = self.client.get('/conversiones/99/999/999')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Conversion not found', data['message'])

if __name__ == '__main__':
    unittest.main()
