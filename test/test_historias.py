import unittest
import json
from app import create_app, db
from app.models.historia_clinica import Historia_Clinica

app = create_app()

class TestHistoriasClinicas(unittest.TestCase):

    def setUp(self):
        # Crear y activar un contexto de aplicación
        self.app_context = app.app_context()
        self.app_context.push()

        # Configurar el cliente de pruebas de Flask
        self.client = app.test_client()
        self.client.testing = True

        # Crear tablas en la base de datos
        db.create_all()

        # Insertar una evaluación de ejemplo
        evaluacion = Historia_Clinica(
            codigo_hc=1,
            documento_paciente='123456789',
            motivo_consulta='Evaluación de atención',
            estado_actual='Normal',
            antecedentes='Sin antecedentes relevantes',
            historial_personal='Sin problemas neurológicos',
            historial_familiar='Abuelos con Alzheimer'
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
        response = self.client.post('/historias', json={
            'codigo_hc': 2,
            'documento_paciente': '987654321',
            'motivo_consulta': 'Evaluación de memoria',
            'estado_actual': 'Leve deterioro',
            'antecedentes': 'Traumatismo craneal',
            'historial_personal': 'Dificultades para recordar nombres',
            'historial_familiar': 'Padre con demencia'
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Historia Clínica creada exitosamente", data['message'])

    def test_obtener_evaluaciones(self):
        response = self.client.get('/historias')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data) > 0)

    def test_obtener_evaluacion(self):
        response = self.client.get('/historias/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['motivo_consulta'], 'Evaluación de atención')

    def test_actualizar_evaluacion(self):
        response = self.client.put('/historias/1', json={
            'motivo_consulta': 'Evaluación de atención y concentración',
            'estado_actual': 'Leve mejoría'
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Historia Clínica actualizada exitosamente", data['message'])

    def test_eliminar_evaluacion(self):
        response = self.client.delete('/historias/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Historia Clínica eliminada exitosamente", data['message'])

if __name__ == '__main__':
    unittest.main()
