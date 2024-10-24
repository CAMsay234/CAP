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
          # Abrir la ventana en pantalla completa
        self.WindowState = Qt.WindowMaximized  

        main_layout = QVBoxLayout()

        # Crear un layout horizontal para la imagen y el botón de volver
        top_layout = QHBoxLayout()

        # Cargar la imagen correctamente escalada
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        top_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Añadir un espaciador entre el logo y el botón
        top_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        # Añadir el layout del header al layout principal
        main_layout.addLayout(top_layout)

        # Crear un espaciador grande debajo de la imagen
        main_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Fixed))


         # Crear el título centrado
        titulo = QLabel("SISTEMA AUTOMATIZADO PARA LA GESTIÓN DE DATOS CLÍNICOS Y NEUROPSICOLÓGICOS")
        font = QFont('Arial', 24)
        font.setBold(True)  # Poner el texto en negrilla
        titulo.setFont(font)
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titulo)

        # Crear un espaciador debajo del título
        main_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Crear un layout para los campos de usuario y contraseña
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)  # Espacio reducido entre los campos
        
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
        #self.boton_olvido_contrasena = QPushButton("¿Olvidaste la contraseña?")
        #self.boton_olvido_contrasena.setProperty('flat', True)
        #buttons_layout.addWidget(self.boton_olvido_contrasena, alignment=Qt.AlignCenter)

        # Crear el botón de "Registrarse"
        self.boton_registro = QPushButton("Registrarse")
        self.boton_registro.setProperty('flat', True)
        buttons_layout.addWidget(self.boton_registro, alignment=Qt.AlignCenter)

        # Añadir los botones al layout
        form_layout.addLayout(buttons_layout)

        # Añadir el formulario al layout principal
        main_layout.addLayout(form_layout)

        main_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Conectar el botón de registro con la acción para abrir la ventana de registro
        self.boton_registro.clicked.connect(self.abrir_registro)

        # Conectar el botón de login para abrir la nueva ventana de tipo historia
        self.boton_login.clicked.connect(self.abrir_tipo_historia)

        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

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

    # Crear una instancia de la ventana de login
    ventana = LoginWindow()
    ventana.showMaximized()  # Asegura que la ventana se abra maximizada

    # Ejecutar la aplicación
    sys.exit(app.exec_())

