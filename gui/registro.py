import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtGui import QFont
import requests
import re
 
class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()
 
        # Configurar la ventana
        self.setWindowTitle("Registro de Usuario")
        self.setGeometry(100, 100, 400, 300)
        #self.setStyleSheet("background-color: #005BBB;")
 
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
    
    def validar_registro(self):
        """Valida los datos ingresados para el registro."""
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        if not username or not email or not password:
            self.mostrar_mensaje("Error", "Todos los campos son obligatorios.")
            return
        if not self.validar_email(email):
            self.mostrar_mensaje("Error", "El correo electrónico debe contener '@' y '.'.")
            return
        if not self.validar_contrasena(password):
            self.mostrar_mensaje("Error", "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.")
            return
        if not self.verificar_unicidad(username, email):
            return
        # Enviar los datos de registro a la API de Flask
        url = "http://127.0.0.1:5000/register"
        data = {"username": username, "email": email, "password": password}
        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                self.mostrar_mensaje("Éxito", "Usuario registrado exitosamente.")
            else:
                try:
                    error_message = response.json().get('error', 'Error desconocido')
                    self.mostrar_mensaje("Error", f"Hubo un error: {error_message}")
                except ValueError:
                    self.mostrar_mensaje("Error", f"Respuesta inesperada del servidor: {response.text}")
        except requests.exceptions.ConnectionError:
            self.mostrar_mensaje("Error", "No se pudo conectar con el servidor. Revisa tu conexión.")

    def validar_email(self, email):
        """Valida que el correo electrónico tenga un formato válido."""
        patron = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(patron, email) is not None
    
    def validar_contrasena(self, password):
        """
        Valida que la contraseña tenga al menos 8 caracteres,
        contenga al menos una letra mayúscula y un número.
        """
        if len(password) < 8:
            print("Error: La contraseña tiene menos de 8 caracteres.")  # Depuración
            return False
        if not re.search(r'[A-Z]', password):
            print("Error: La contraseña no tiene ninguna letra mayúscula.")  # Depuración
            return False
        if not re.search(r'\d', password):
            print("Error: La contraseña no tiene ningún número.")  # Depuración
            return False
        return True
    
    def verificar_unicidad(self, username, email):
        """Verifica que el nombre de usuario y el correo electrónico sean únicos."""
        
        # Verificar nombre de usuario
        url_username = f"http://127.0.0.1:5000/user/{username}"
        try:
            response_username = requests.get(url_username)
            if response_username.status_code == 200:
                self.mostrar_mensaje("Error", "El nombre de usuario ya existe. Por favor, elige otro.")
                return False
            elif response_username.status_code != 404:
                self.mostrar_mensaje("Error", f"Error al verificar el nombre de usuario: {response_username.text}")
                return False
        except requests.exceptions.ConnectionError:
            self.mostrar_mensaje("Error", "No se pudo conectar con el servidor. Revisa tu conexión.")
            return False
        # Verificar correo electrónico
        url_email = f"http://127.0.0.1:5000/user/email/{email}"
        try:
            response_email = requests.get(url_email)
            if response_email.status_code == 200:
                self.mostrar_mensaje("Error", "El correo electrónico ya existe. Por favor, elige otro.")
                return False
            elif response_email.status_code != 404:
                self.mostrar_mensaje("Error", f"Error al verificar el correo electrónico: {response_email.text}")
                return False
        except requests.exceptions.ConnectionError:
            self.mostrar_mensaje("Error", "No se pudo conectar con el servidor. Revisa tu conexión.")
            return False
        return True
    
    def mostrar_mensaje(self, titulo, mensaje):
        """Muestra un cuadro de diálogo con un mensaje."""
        msg_box = QMessageBox(self)  # Asociar con la ventana principal
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje if mensaje else "Error desconocido.")  # Asegurar que haya mensaje
        msg_box.setIcon(QMessageBox.Warning)  # Establecer un icono claro
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #f0f0f0;
                font-size: 14px;
                color: #005BBB;
            }
            QLabel {
                color: #005BBB;
            }
            QPushButton {
                background-color: #005BBB;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #003F73;
            }
        """)
        msg_box.exec_()

    def register_user(self):
        """Maneja el proceso de registro del usuario."""
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        # Verificar que todos los campos estén completos
        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            self.mostrar_mensaje("Error", "Todos los campos son obligatorios.")
            return
        # Validar la contraseña
        if not self.validar_contrasena(password):
            self.mostrar_mensaje("Error", "La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.")
            return
        # Validar el formato del correo electrónico
        if not self.validar_email(email):
            self.mostrar_mensaje("Error", "El correo electrónico no tiene un formato válido.")
            return
        # Verificar que el nombre de usuario y el correo sean únicos
        if not self.verificar_unicidad(username, email):
            return

        # Enviar los datos de registro a la API de Flask
        url = "http://127.0.0.1:5000/register"
        data = {"username": username, "email": email, "password": password}

        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                #QMessageBox.information(self,"Éxito", "Usuario registrado exitosamente.")
                self.mostrar_mensaje("Éxito", "Usuario registrado exitosamente.")
            else:
                QMessageBox.warning(self, "Error", f"Hubo un error: {response.json().get('error')}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar con el servidor: {str(e)}")
            try:
                    error_message = response.json().get('error', 'Error desconocido')
                    self.mostrar_mensaje("Error", f"Hubo un error: {error_message}")
            except ValueError:
                    self.mostrar_mensaje("Error", f"Respuesta inesperada del servidor: {response.text}")
        except requests.exceptions.ConnectionError:
            self.mostrar_mensaje("Error", "No se pudo conectar con el servidor. Revisa tu conexión.")

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
    sys.exit(app.exec_())