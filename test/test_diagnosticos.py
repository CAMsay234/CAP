import unittest
import json
from datetime import datetime
from app import create_app, db
from app.models.diagnostico import Diagnostico
from app.models.hipotesis import Hipotesis

app = create_app()

class TestDiagnosticos(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        self.client = app.test_client()
        self.client.testing = True

        db.create_all()

        # Crear una hipótesis de ejemplo para asociar con el diagnóstico
        hipotesis = Hipotesis(id=1, descripcion='Hipótesis Inicial')
        db.session.add(hipotesis)

        # Crear un diagnóstico de ejemplo
        diagnostico = Diagnostico(
            codigo_hc=1,
            plan_Tratamiento='Plan inicial',
            fecha=datetime(2023, 5, 15).date(),
            conclusion='Conclusión inicial'
        )
        diagnostico.hipotesis.append(hipotesis)

        db.session.add(diagnostico)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear_diagnostico(self):
        response = self.client.post('/diagnosticos', json={
            'codigo_hc': 2,
            'plan_Tratamiento': 'Nuevo Plan',
            'fecha': '2023-10-10',
            'conclusion': 'Nueva Conclusión',
            'hipotesis_ids': [1]
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Diagnóstico creado exitosamente', data['message'])

    def test_obtener_diagnostico(self):
        response = self.client.get('/diagnosticos/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['plan_tratamiento'], 'Plan inicial')
        self.assertEqual(len(data['hipotesis']), 1)

    def test_actualizar_diagnostico(self):
        response = self.client.put('/diagnosticos/1', json={
            'plan_Tratamiento': 'Plan Actualizado',
            'fecha': '2024-01-01',
            'conclusion': 'Conclusión Actualizada',
            'hipotesis_ids': [1]
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Diagnóstico actualizado exitosamente', data['message'])

        # Verificar que los cambios se realizaron correctamente
        response = self.client.get('/diagnosticos/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['plan_tratamiento'], 'Plan Actualizado')
        self.assertEqual(data['fecha'], '2024-01-01')

    def test_eliminar_diagnostico(self):
        response = self.client.delete('/diagnosticos/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Diagnóstico eliminado exitosamente', data['message'])

        # Verificar que se eliminó
        response = self.client.get('/diagnosticos/1')
        self.assertEqual(response.status_code, 404)

    def test_obtener_diagnosticos(self):
        response = self.client.get('/diagnosticos')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data) > 0)

    def test_obtener_diagnostico_no_existente(self):
        response = self.client.get('/diagnosticos/99')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Diagnóstico no encontrado', data['error'])

if __name__ == '__main__':
    unittest.main()
