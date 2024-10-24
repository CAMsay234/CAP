import unittest
import json
from app import create_app, db
from app.models.comentarios_clinicos import Comentarios

app = create_app()

class TestComentarios(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        self.client = app.test_client()
        self.client.testing = True

        db.create_all()

        # Crear un comentario de ejemplo para pruebas
        comentario = Comentarios(
            codigo_hc=1,
            id_prueba=101,
            tipo_comentario="inicial",
            comentario="Comentario de prueba"
        )
        db.session.add(comentario)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear_comentario(self):
        response = self.client.post('/comentarios', json={
            "codigo_hc": 2,
            "id_prueba": 102,
            "tipo_comentario": "seguimiento",
            "comentario": "Nuevo comentario"
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Comentario creado exitosamente", data['message'])

    def test_obtener_comentarios(self):
        response = self.client.get('/comentarios')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertTrue(len(data) > 0)

    def test_obtener_comentario(self):
        response = self.client.get('/comentarios/1/101/inicial')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['comentario'], "Comentario de prueba")

    def test_actualizar_comentario(self):
        response = self.client.put('/comentarios/1/101/inicial', json={
            "comentario": "Comentario actualizado"
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Comentario actualizado exitosamente", data['message'])

    def test_eliminar_comentario(self):
        response = self.client.delete('/comentarios/1/101/inicial')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Comentario eliminado exitosamente", data['message'])

    def test_crear_comentario_faltante(self):
        response = self.client.post('/comentarios', json={
            "codigo_hc": 3,
            "id_prueba": 103
        })  # Falta "tipo_comentario"
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Los campos codigo_hc, id_prueba, y tipo_comentario son obligatorios", data['error'])

    def test_obtener_comentario_no_existente(self):
        response = self.client.get('/comentarios/99/999/inexistente')
        self.assertEqual(response.status_code, 404)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Comentario no encontrado", data['error'])

if __name__ == '__main__':
    unittest.main()
