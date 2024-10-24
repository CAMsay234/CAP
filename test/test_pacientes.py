import unittest
import json
from datetime import datetime, date
from app import create_app, db
from app.models.paciente import Paciente

app = create_app()

class TestPacientes(unittest.TestCase):

    def setUp(self):
        # Crear y activar un contexto de aplicación
        self.app_context = app.app_context()
        self.app_context.push()

        # Configurar el cliente de pruebas de Flask
        self.client = app.test_client()
        self.client.testing = True

        # Crear las tablas en la base de datos
        db.create_all()

        # Insertar un paciente de ejemplo para las pruebas
        paciente = Paciente(
            documento='123456789',
            nombre='Juan Pérez',
            edad=30,
            fecha_nacimiento=date(1993, 5, 1),  # Conversión correcta a date
            id_escolaridad=2,
            profesion='Ingeniero',
            telefono='1234567',
            celular='987654321',
            remision='Ninguna'
        )
        db.session.add(paciente)
        db.session.commit()

    def tearDown(self):
        # Eliminar todo después de las pruebas
        db.session.remove()
        db.drop_all()

        # Desactivar el contexto de la aplicación
        self.app_context.pop()

    def test_listar_pacientes(self):
        response = self.client.get('/pacientes/listar')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data) > 0)

    def test_buscar_paciente(self):
        response = self.client.get('/paciente/buscar?documento=123456789')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['nombre'], 'Juan Pérez')

    def test_crear_paciente(self):
        response = self.client.post('/paciente/nuevo', json={
            'documento': '987654321',
            'nombre': 'María López',
            'edad': 28,
            'fecha_nacimiento': '1995-03-15',  # Enviar como string, se convertirá en la ruta
            'id_escolaridad': 3,
            'profesion': 'Abogada',
            'telefono': '7654321',
            'celular': '123456789',
            'remision': 'Consulta externa'
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['nombre'], 'María López')

    def test_obtener_paciente(self):
        response = self.client.get('/paciente/buscar?documento=123456789')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['nombre'], 'Juan Pérez')

    def test_actualizar_paciente(self):
        response = self.client.put('/paciente/1', json={
            'nombre': 'Juan Pérez Actualizado',
            'edad': 31
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Paciente actualizado exitosamente", data['mensaje'])

    def test_eliminar_paciente(self):
        response = self.client.delete('/paciente/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Paciente eliminado exitosamente", data['mensaje'])

    def test_contar_pacientes(self):
        response = self.client.get('/pacientes/count')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(data['count'] > 0)

if __name__ == '__main__':
    unittest.main()