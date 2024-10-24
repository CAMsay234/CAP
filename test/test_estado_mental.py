import unittest
import json
from app import create_app, db
from app.models.estado_mental import EstadoMental

app = create_app()

class TestEstadoMental(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        self.client = app.test_client()
        self.client.testing = True

        db.create_all()

        # Crear un estado mental de ejemplo para las pruebas
        estado_mental = EstadoMental(
            codigo_hc=1,
            atencion="Buena",
            memoria="Adecuada",
            lenguaje="Fluido",
            pensamiento="Lógico",
            introspeccion="Presente"
        )
        db.session.add(estado_mental)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear_estado_mental(self):
        response = self.client.post('/estado_mental', json={
            'codigo_hc': 2,
            'atencion': 'Regular',
            'memoria': 'Media',
            'lenguaje': 'Adecuado',
            'pensamiento': 'Abstracto',
            'introspeccion': 'Parcial'
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Estado mental creado exitosamente', data['message'])

    def test_obtener_estado_mental(self):
        response = self.client.get('/estado_mental/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['atencion'], 'Buena')

    def test_obtener_estado_mental_no_existente(self):
        response = self.client.get('/estado_mental/99')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Estado mental no encontrado', data['error'])

    def test_actualizar_estado_mental(self):
        response = self.client.put('/estado_mental/1', json={
            'atencion': 'Excelente',
            'memoria': 'Mejorada'
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Estado mental actualizado exitosamente', data['message'])

        # Verificar actualización
        response = self.client.get('/estado_mental/1')
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['atencion'], 'Excelente')
        self.assertEqual(data['memoria'], 'Mejorada')

    def test_eliminar_estado_mental(self):
        response = self.client.delete('/estado_mental/1')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn('Estado mental eliminado exitosamente', data['message'])

        # Verificar eliminación
        response = self.client.get('/estado_mental/1')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
