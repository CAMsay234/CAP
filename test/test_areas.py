import unittest
import json
from app import create_app, db
from app.models.area import Area

app = create_app()

class TestAreas(unittest.TestCase):

    def setUp(self):
        # Crear y activar un contexto de aplicación
        self.app_context = app.app_context()
        self.app_context.push()

        # Configurar el cliente de pruebas de Flask
        self.client = app.test_client()
        self.client.testing = True

        # Crear las tablas necesarias en la base de datos
        db.create_all()

        # Insertar un área de ejemplo para pruebas
        area = Area(
            codigo_hc=1,
            familiar='Buena relación familiar',
            pareja='Estable',
            social='Activo socialmente',
            laboral='Satisfacción laboral alta'
        )
        db.session.add(area)
        db.session.commit()

    def tearDown(self):
        # Limpiar la base de datos después de las pruebas
        db.session.remove()
        db.drop_all()

        # Desactivar el contexto de la aplicación
        self.app_context.pop()

    def test_crear_area(self):
        response = self.client.post('/areas', json={
            'codigo_hc': 2,
            'familiar': 'Relación conflictiva',
            'pareja': 'Inestable',
            'social': 'Aislado',
            'laboral': 'Insatisfacción laboral'
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Área creada exitosamente", data['message'])

    def test_obtener_areas(self):
        response = self.client.get('/areas')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data) > 0)

    def test_obtener_area(self):
        response = self.client.get('/areas/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['familiar'], 'Buena relación familiar')

    def test_actualizar_area(self):
        response = self.client.put('/areas/1', json={
            'familiar': 'Relación mejorada',
            'pareja': 'Estable',
            'social': 'Moderadamente activo',
            'laboral': 'Satisfacción laboral media'
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Área actualizada exitosamente", data['message'])

    def test_eliminar_area(self):
        response = self.client.delete('/areas/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Área eliminada exitosamente", data['message'])

if __name__ == '__main__':
    unittest.main()
