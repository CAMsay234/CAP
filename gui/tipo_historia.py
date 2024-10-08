import os
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QWidget
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from seleccionar_registrar_paciente import SeleccionarRegistrarPacienteWindow  # Importar la nueva ventana

class TipoHistoriaWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana para que se abra en pantalla completa
        self.setWindowTitle("Tipo de Historia Clínica")
        self.showMaximized()  # Abrir la ventana maximizada
        self.setStyleSheet("background-color: #005BBB;")  # Fondo azul

        # Crear el layout principal
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

        # Botón de regreso en la esquina superior derecha
        self.boton_regresar = QPushButton("VOLVER")
        self.boton_regresar.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                border-radius: 5px;
                font-size: 14px;
                height: 40px;
                width: 80px;
                color: white;
                border: 1px solid white;
            }
            QPushButton:hover {
                background-color: #003F7D;
            }
        """)
        self.boton_regresar.clicked.connect(self.regresar_login)  # Conectar el botón de regreso
        top_layout.addWidget(self.boton_regresar, alignment=Qt.AlignRight)

        # Añadir el layout superior al layout principal
        main_layout.addLayout(top_layout)

        # Crear un espaciador grande debajo de la imagen
        main_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Crear el título centrado
        title_layout = QHBoxLayout()
        titulo = QLabel("TIPO DE HISTORIA CLÍNICA")
        titulo.setFont(QFont('Arial', 56))  # Agrandado a 56px
        titulo.setStyleSheet("color: white;")
        titulo.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(titulo, alignment=Qt.AlignCenter)
        main_layout.addLayout(title_layout)

        # Crear un espaciador grande debajo del título
        main_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Crear el layout para los botones, centrado
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(100)  # Espaciado grande entre los botones

        # Botón para Historia Clínica de Niños
        self.boton_ninos = QPushButton("HISTORIA CLÍNICA DE NIÑOS")
        self.boton_ninos.setStyleSheet("""
            QPushButton {
                background-color: #C0C0C0;
                border-radius: 10px;
                font-size: 20px;
                height: 80px;
                width: 300px;
                color: #005BBB;
            }
        """)
        buttons_layout.addWidget(self.boton_ninos, alignment=Qt.AlignCenter)

        # Botón para Historia Clínica de Adultos
        self.boton_adultos = QPushButton("HISTORIA CLÍNICA DE ADULTOS")
        self.boton_adultos.setStyleSheet("""
            QPushButton {
                background-color: #FFFFFF;
                border-radius: 10px;
                font-size: 20px;
                height: 80px;
                width: 300px;
                color: #005BBB;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.boton_adultos.clicked.connect(self.abrir_seleccionar_registrar_paciente)  # Conectar el botón
        buttons_layout.addWidget(self.boton_adultos, alignment=Qt.AlignCenter)

        # Añadir el layout de botones al layout principal
        main_layout.addLayout(buttons_layout)

        # Crear un espaciador grande debajo de los botones
        main_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Crear un widget central para contener los elementos
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def abrir_seleccionar_registrar_paciente(self):
        """Cierra la ventana actual y abre la de Seleccionar o Registrar Paciente."""
        self.seleccionar_registrar_paciente = SeleccionarRegistrarPacienteWindow()  # Crear la nueva ventana
        self.seleccionar_registrar_paciente.show()  # Mostrar la nueva ventana
        self.close()  # Cerrar la ventana actual

    def regresar_login(self):
        """Regresa a la ventana de Login."""
        from main_window import LoginWindow  # Importar aquí para evitar el import circular
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()
