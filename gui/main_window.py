import sys
import os
import requests  # Asegúrate de tener instalado requests: pip install requests
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, 
                             QPushButton, QVBoxLayout, QHBoxLayout, QWidget, 
                             QSpacerItem, QSizePolicy, QMessageBox)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from registro import RegisterWindow
from tipo_historia import TipoHistoriaWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle("Sistema Automatizado para la Gestión de Datos Clínicos y Neuropsicológicos")
        self.showMaximized()  # Abrir la ventana maximizada

        # Layout principal
        main_layout = QVBoxLayout()

        # Layout superior con imagen
        top_layout = QHBoxLayout()
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        top_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Añadir espaciador en el top layout
        top_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        main_layout.addLayout(top_layout)

        # Espaciador grande debajo de la imagen
        main_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Título
        titulo = QLabel("SISTEMA AUTOMATIZADO PARA LA GESTIÓN DE DATOS CLÍNICOS Y NEUROPSICOLÓGICOS")
        font = QFont('Arial', 24, QFont.Bold)  # Negrita
        titulo.setFont(font)
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titulo)

        # Espaciador debajo del título
        main_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Formulario de login
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("USUARIO")

        self.input_contrasena = QLineEdit()
        self.input_contrasena.setPlaceholderText("CONTRASEÑA")
        self.input_contrasena.setEchoMode(QLineEdit.Password)

        form_layout.addWidget(self.input_usuario, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.input_contrasena, alignment=Qt.AlignCenter)

        # Botón de login
        self.boton_login = QPushButton("ENTRAR")
        form_layout.addWidget(self.boton_login, alignment=Qt.AlignCenter)

        # Layout para el botón de registro
        buttons_layout = QHBoxLayout()

        self.boton_registro = QPushButton("Registrarse")
        self.boton_registro.setProperty('flat', True)
        buttons_layout.addWidget(self.boton_registro, alignment=Qt.AlignCenter)

        form_layout.addLayout(buttons_layout)
        main_layout.addLayout(form_layout)

        # Espaciador final
        main_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Conectar botones a funciones
        self.boton_registro.clicked.connect(self.abrir_registro)
        self.boton_login.clicked.connect(self.validar_login)

        # Configurar el widget principal
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def validar_login(self):
        """Valida las credenciales ingresadas."""
        username = self.input_usuario.text()
        password = self.input_contrasena.text()

        if not username or not password:
            self.mostrar_mensaje("Error", "Por favor ingresa tanto el usuario como la contraseña.")
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/login",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                self.mostrar_mensaje("Bienvenido", f"Bienvenido {username}")
                self.abrir_tipo_historia()
            else:
                self.mostrar_mensaje("Error", "Credenciales incorrectas. Por favor, verifica tus datos.")
        except requests.exceptions.ConnectionError:
            self.mostrar_mensaje("Error", "No se pudo conectar con el servidor. Revisa tu conexión.")

    def mostrar_mensaje(self, titulo, mensaje):
        """Muestra un cuadro de diálogo con un mensaje."""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def abrir_tipo_historia(self):
        """Abre la ventana de tipo historia y cierra la ventana actual."""
        self.tipo_historia_ventana = TipoHistoriaWindow()
        self.tipo_historia_ventana.show()
        self.close()

    def abrir_registro(self):
        """Abre la ventana de registro."""
        self.registro_ventana = RegisterWindow()
        self.registro_ventana.show()

# Función para cargar el archivo de estilos
def load_stylesheet(app):
    stylesheet_path = os.path.join(os.path.dirname(__file__), 'styles.qss')
    with open(stylesheet_path, "r") as file:
        app.setStyleSheet(file.read())


# Ejecutar la aplicación


if __name__ == '__main__':
    app = QApplication(sys.argv)
    load_stylesheet(app)

    ventana = LoginWindow()
    ventana.showFullScreen()  # Cambiar a showFullScreen()

    sys.exit(app.exec_())


