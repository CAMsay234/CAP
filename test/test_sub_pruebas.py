import unittest
import json
from app import create_app, db
from app.models.sub_prueba import SubPrueba

app = create_app()

class TestSubPruebas(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        self.client = app.test_client()
        self.client.testing = True

        db.create_all()

        # Crear una sub_prueba inicial para las pruebas
        sub_prueba = SubPrueba(nombre='SubPrueba Inicial', id_prueba=1)
        db.session.add(sub_prueba)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear_subprueba(self):
        response = self.client.post('/subpruebas', json={
            'nombre': 'Nueva SubPrueba',
            'id_prueba': 2
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('SubPrueba creada exitosamente', data['message'])

    def test_obtener_subpruebas(self):
        response = self.client.get('/subpruebas')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertGreater(len(data), 0)

    def test_obtener_subprueba(self):
        response = self.client.get('/subpruebas/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['nombre'], 'SubPrueba Inicial')

    def test_obtener_subprueba_no_existente(self):
        response = self.client.get('/subpruebas/99')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('SubPrueba no encontrada', data['error'])

    def test_actualizar_subprueba(self):
        response = self.client.put('/subpruebas/1', json={
            'nombre': 'SubPrueba Actualizada',
            'id_prueba': 2
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('SubPrueba actualizada exitosamente', data['message'])

        # Verificar que se haya actualizado correctamente
        response = self.client.get('/subpruebas/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['nombre'], 'SubPrueba Actualizada')

    def test_eliminar_subprueba(self):
        response = self.client.delete('/subpruebas/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('SubPrueba eliminada exitosamente', data['message'])

        # Verificar que se haya eliminado
        response = self.client.get('/subpruebas/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
