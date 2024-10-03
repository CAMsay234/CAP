import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QFont
import requests

class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle("Registro de Usuario")
        self.setGeometry(100, 100, 400, 300)

        # Layout principal
        layout = QVBoxLayout()

        # Campo de nombre de usuario
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Nombre de Usuario")
        self.username_input.setFont(QFont("Arial", 12))
        layout.addWidget(self.username_input)

        # Campo de correo electrónico
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Correo Electrónico")
        self.email_input.setFont(QFont("Arial", 12))
        layout.addWidget(self.email_input)

        # Campo de contraseña
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Arial", 12))
        layout.addWidget(self.password_input)

        # Botón de registro
        self.register_button = QPushButton("Registrar", self)
        self.register_button.setFont(QFont("Arial", 12))
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button)

        # Establecer el layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def register_user(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return

        # Enviar los datos de registro a la API de Flask
        url = "http://127.0.0.1:5000/register"
        data = {"username": username, "email": email, "password": password}

        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                QMessageBox.information(self, "Éxito", "Usuario registrado exitosamente")
            else:
                QMessageBox.warning(self, "Error", f"Hubo un error: {response.json().get('error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar con el servidor: {str(e)}")

# Función para cargar el archivo de estilos
def load_stylesheet(app):
    with open("styles.qss", "r") as file:
        app.setStyleSheet(file.read())

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Cargar el stylesheet general
    load_stylesheet(app)

    ventana = RegisterWindow()
    ventana.show()
    sys.exit(app.exec_())

