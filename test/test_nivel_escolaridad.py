import unittest
import json
from app import create_app, db
from app.models.nivel_escolaridad import NivelEscolaridad

app = create_app()

class TestNivelEscolaridad(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        self.client = app.test_client()
        self.client.testing = True

        db.create_all()

        # Crear un nivel de escolaridad de ejemplo
        nivel = NivelEscolaridad(descripcion="Primaria")
        db.session.add(nivel)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear_nivel_escolaridad(self):
        response = self.client.post('/niveles_escolaridad', json={
            'descripcion': 'Secundaria'
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Nivel de escolaridad creado exitosamente', data['message'])

    def test_obtener_niveles_escolaridad(self):
        response = self.client.get('/niveles_escolaridad')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data) > 0)

    def test_obtener_nivel_escolaridad(self):
        response = self.client.get('/niveles_escolaridad/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['descripcion'], 'Primaria')

    def test_obtener_nivel_escolaridad_no_existente(self):
        response = self.client.get('/niveles_escolaridad/99')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Nivel de escolaridad no encontrado', data['error'])

    def test_actualizar_nivel_escolaridad(self):
        response = self.client.put('/niveles_escolaridad/1', json={
            'descripcion': 'Primaria Actualizada'
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Nivel de escolaridad actualizado exitosamente', data['message'])

        # Verificar la actualización
        response = self.client.get('/niveles_escolaridad/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['descripcion'], 'Primaria Actualizada')

    def test_eliminar_nivel_escolaridad(self):
        response = self.client.delete('/niveles_escolaridad/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Nivel de escolaridad eliminado exitosamente', data['message'])

        # Verificar que se eliminó
        response = self.client.get('/niveles_escolaridad/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
