import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle("Sistema Automatizado para la Gestión de Datos Clínicos y Neuropsicológicos")
        self.setGeometry(100, 100, 800, 600)  # Tamaño inicial de la ventana

        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Crear un layout horizontal para la imagen
        image_layout = QHBoxLayout()
        
        # Cargar la imagen correctamente escalada
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')  # Asegúrate de que la imagen esté en la carpeta correcta
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Escalar imagen manteniendo proporción
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
        titulo.setFont(QFont('Arial', 16))
        titulo.setStyleSheet("color: white;")
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
        self.input_usuario.setFixedHeight(40)  # Tamaño del recuadro
        self.input_usuario.setFixedWidth(300)   # Ancho ajustado

        self.input_contrasena = QLineEdit()
        self.input_contrasena.setPlaceholderText("CONTRASEÑA")
        self.input_contrasena.setEchoMode(QLineEdit.Password)
        self.input_contrasena.setFixedHeight(40)  # Tamaño del recuadro
        self.input_contrasena.setFixedWidth(300)   # Ancho ajustado

        form_layout.addWidget(self.input_usuario, alignment=Qt.AlignCenter)
        form_layout.addWidget(self.input_contrasena, alignment=Qt.AlignCenter)

        # Crear el botón de inicio de sesión
        self.boton_login = QPushButton("ENTRAR")
        self.boton_login.setFixedHeight(40)
        self.boton_login.setFixedWidth(150)
        form_layout.addWidget(self.boton_login, alignment=Qt.AlignCenter)

        # Crear el botón de "¿Olvidaste tu contraseña?"
        self.boton_olvido_contrasena = QPushButton("¿Olvidaste la contraseña?")
        self.boton_olvido_contrasena.setStyleSheet("background-color: none; border: none; color: white; text-decoration: underline;")
        form_layout.addWidget(self.boton_olvido_contrasena, alignment=Qt.AlignCenter)

        # Añadir el formulario al layout principal
        main_layout.addLayout(form_layout)

        # Crear un widget central para contener los elementos
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Aplicar estilos
        self.setStyleSheet("""
            QMainWindow {
                background-color: #005BBB;
            }
            QLineEdit {
                background-color: white;
                border-radius: 10px;
                padding-left: 10px;
                font-size: 16px;
            }
            QPushButton {
                background-color: #FFFFFF;
                border-radius: 10px;
                font-size: 16px;
            }
        """)

# Ejecutar la aplicación
if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Crear una instancia de la ventana y mostrarla
    ventana = LoginWindow()
    ventana.show()

    sys.exit(app.exec_())
