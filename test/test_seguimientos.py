import unittest
import json
from app import create_app, db
from app.models.seguimiento import Seguimiento, get_next_num_seccion
from datetime import datetime

app = create_app()

class TestSeguimientos(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        self.client = app.test_client()
        self.client.testing = True

        db.create_all()

        # Crear un seguimiento inicial para las pruebas
        seguimiento = Seguimiento(
            codigo_hc=1,
            num_seccion=get_next_num_seccion(1),
            fecha=datetime(2024, 10, 1).date(),  # Usar objeto date
            descripcion='Seguimiento inicial'
        )
        db.session.add(seguimiento)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear_seguimiento(self):
        # Convertir fecha a string para enviar en JSON
        fecha_str = datetime(2024, 10, 10).strftime('%Y-%m-%d')

        response = self.client.post('/seguimientos', json={
            'codigo_hc': 2,
            'fecha': fecha_str,  # Enviar la fecha como string
            'descripcion': 'Nuevo seguimiento'
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Seguimiento creado exitosamente', data['message'])
        self.assertEqual(data['num_seccion'], 1)

    def test_obtener_seguimientos(self):
        response = self.client.get('/seguimientos')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertGreater(len(data), 0)

    def test_obtener_seguimiento(self):
        response = self.client.get('/seguimientos/1/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['descripcion'], 'Seguimiento inicial')

    def test_obtener_seguimiento_no_existente(self):
        response = self.client.get('/seguimientos/99/99')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Seguimiento no encontrado', data['error'])

    def test_actualizar_seguimiento(self):
        # Convertir fecha a string para enviar en JSON
        fecha_str = datetime(2024, 10, 5).strftime('%Y-%m-%d')

        response = self.client.put('/seguimientos/1/1', json={
            'fecha': fecha_str,  # Enviar la fecha como string
            'descripcion': 'Seguimiento actualizado'
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Seguimiento actualizado exitosamente', data['message'])

        # Verificar actualización
        response = self.client.get('/seguimientos/1/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['descripcion'], 'Seguimiento actualizado')

    def test_eliminar_seguimiento(self):
        response = self.client.delete('/seguimientos/1/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Seguimiento eliminado exitosamente', data['message'])

        # Verificar que se eliminó
        response = self.client.get('/seguimientos/1/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
