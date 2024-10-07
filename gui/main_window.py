import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from registro import RegisterWindow  # Importar la ventana de registro
from tipo_historia import TipoHistoriaWindow  # Importar la nueva ventana de tipo de historia

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana para que se abra en modo pantalla completa
        self.setWindowTitle("Sistema Automatizado para la Gestión de Datos Clínicos y Neuropsicológicos")
        self.showFullScreen()  # Abrir la ventana en pantalla completa

        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Crear un layout horizontal para la imagen
        image_layout = QHBoxLayout()
        
        # Cargar la imagen correctamente escalada
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')  # Asegúrate de que la imagen esté en la carpeta correcta
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Escalar imagen manteniendo proporción
        self.logo.setPixmap(pixmap)
        image_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Añadir el layout de la imagen al layout principal
        main_layout.addLayout(image_layout)

        # Crear un espaciador adicional debajo de la imagen para ajustar el título
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Crear un layout horizontal para el título
        title_layout = QHBoxLayout()

        # Crear una etiqueta para el título
        titulo = QLabel("SISTEMA AUTOMATIZADO PARA LA GESTIÓN DE DATOS CLÍNICOS Y NEUROPSICOLÓGICOS")
        titulo.setFont(QFont('Arial', 60))
        titulo.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(titulo, alignment=Qt.AlignCenter)

        # Añadir el layout del título al layout principal
        main_layout.addLayout(title_layout)

        # Crear un layout para los campos de usuario y contraseña
        form_layout = QVBoxLayout()
        form_layout.setSpacing(10)  # Espacio reducido entre los campos

        # Crear los campos de usuario y contraseña
        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("USUARIO")

        self.input_contrasena = QLineEdit()
        self.input_contrasena.setPlaceholderText("CONTRASEÑA")
        self.input_contrasena.setEchoMode(QLineEdit.Password)

        form_layout.addWidget(self.input_usuario, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.input_contrasena, alignment=Qt.AlignCenter)

        # Crear el botón de inicio de sesión
        self.boton_login = QPushButton("ENTRAR")
        form_layout.addWidget(self.boton_login, alignment=Qt.AlignCenter)

        # Crear un layout horizontal para "¿Olvidaste tu contraseña?" y "Registrarse"
        buttons_layout = QHBoxLayout()

        # Crear el botón de "¿Olvidaste tu contraseña?"
        self.boton_olvido_contrasena = QPushButton("¿Olvidaste la contraseña?")
        self.boton_olvido_contrasena.setProperty('flat', True)
        buttons_layout.addWidget(self.boton_olvido_contrasena, alignment=Qt.AlignCenter)

        # Crear el botón de "Registrarse"
        self.boton_registro = QPushButton("Registrarse")
        self.boton_registro.setProperty('flat', True)
        buttons_layout.addWidget(self.boton_registro, alignment=Qt.AlignCenter)

        # Añadir los botones al layout
        form_layout.addLayout(buttons_layout)

        # Añadir el formulario al layout principal
        main_layout.addLayout(form_layout)

        # Crear un widget central para contener los elementos
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Conectar el botón de registro con la acción para abrir la ventana de registro
        self.boton_registro.clicked.connect(self.abrir_registro)

        # Conectar el botón de login para abrir la nueva ventana de tipo historia
        self.boton_login.clicked.connect(self.abrir_tipo_historia)

    def abrir_tipo_historia(self):
        # Cerrar la ventana actual y abrir la nueva ventana
        self.tipo_historia_ventana = TipoHistoriaWindow()  # Crear la nueva ventana
        self.tipo_historia_ventana.show()  # Mostrar la nueva ventana
        self.close()  # Cerrar la ventana actual

    def abrir_registro(self):
        # Abrir la ventana de registro
        self.registro_ventana = RegisterWindow()
        self.registro_ventana.show()

# Función para cargar el archivo de estilos
def load_stylesheet(app):
    stylesheet_path = os.path.join(os.path.dirname(__file__), 'styles.qss')  # Ruta asegurada
    with open(stylesheet_path, "r") as file:
        app.setStyleSheet(file.read())

# Ejecutar la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Cargar el stylesheet general
    load_stylesheet(app)

    # Crear una instancia de la ventana de login y mostrarla
    ventana = LoginWindow()
    ventana.show()

    sys.exit(app.exec_())

