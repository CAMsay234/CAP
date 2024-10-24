import unittest
import json
from app import create_app, db
from app.models.usuario import Usuario

app = create_app()

class TestAuth(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()

        self.client = app.test_client()
        self.client.testing = True

        db.create_all()

        # Crear un usuario de ejemplo
        usuario = Usuario(username='testuser', email='test@example.com')
        usuario.set_password('password123')
        db.session.add(usuario)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_usuario(self):
        response = self.client.post('/register', json={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword123'
        })
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Usuario registrado exitosamente", data['message'])

    def test_register_usuario_existente(self):
        response = self.client.post('/register', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("El nombre de usuario o email ya existe", data['error'])

    def test_login_correcto(self):
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Bienvenido testuser", data['message'])

    def test_login_incorrecto(self):
        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Credenciales incorrectas", data['error'])

    def test_register_campos_faltantes(self):
        response = self.client.post('/register', json={
            'username': '',
            'email': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 400)

        data = json.loads(response.get_data(as_text=True))
        self.assertIn("Todos los campos son obligatorios", data['error'])

if __name__ == '__main__':
    unittest.main()
