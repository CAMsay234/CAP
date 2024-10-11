import os
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QWidget
from PyQt5.QtGui import QFont, QPixmap  # Asegúrate de importar QPixmap
from PyQt5.QtCore import Qt

class SeleccionarRegistrarPacienteWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle("Seleccionar o Registrar Paciente")
        self.showMaximized()  # Abrir la ventana maximizada
        self.setStyleSheet("background-color: white;")  # Fondo blanco

        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Crear un layout horizontal para la barra azul con el logo
        header_layout = QHBoxLayout()

        # Crear un widget que actúe como barra azul
        header_background = QWidget()
        header_background.setStyleSheet("background-color: #005BBB;")
        header_background_layout = QHBoxLayout(header_background)
        header_background_layout.setContentsMargins(0, 0, 0, 0)

        # Logo de UPB
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Ajustar el tamaño del logo
        self.logo.setPixmap(pixmap)
        header_background_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Botón "Volver" en la esquina derecha
        self.boton_volver = QPushButton("VOLVER")
        self.boton_volver.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #005BBB;
                border-radius: 5px;
                color: #005BBB;
                font-size: 14px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.boton_volver.clicked.connect(self.abrir_tipo_historia)  # Conectar el botón para volver
        header_background_layout.addWidget(self.boton_volver, alignment=Qt.AlignRight)

        # Añadir el layout del fondo azul (con el logo y el botón "Volver") al header
        header_layout.addWidget(header_background)

        # Añadir el layout del header al layout principal
        main_layout.addLayout(header_layout)

        # Crear un espaciador grande debajo de la imagen
        main_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Crear el título centrado
        titulo = QLabel("SELECCIONE LA OPCIÓN QUE DESEA")
        font = QFont('Arial', 24)
        font.setBold(True)  # Poner el texto en negrilla
        titulo.setFont(font)
        titulo.setStyleSheet("color: #005BBB;")
        titulo.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(titulo)

        # Crear un espaciador debajo del título
        main_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Crear el layout para los botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(40)  # Espaciado entre los botones

        # Botón para "Seleccionar Paciente"
        self.boton_registrar = QPushButton("REGISTRAR PACIENTE")
        self.boton_registrar.setStyleSheet("""
            QPushButton {
                background-color: #D8D8D8;
                border: 1px solid #005BBB;
                border-radius: 10px;
                font-size: 18px;
                height: 100px;
                width: 250px;
                color: #005BBB;
            }
            QPushButton:hover {
                background-color: #c0c0c0;
            }
        """)
        self.boton_registrar.clicked.connect(self.abrir_registrar_paciente)  # Conectar el botón "Seleccionar Paciente"
        buttons_layout.addWidget(self.boton_registrar, alignment=Qt.AlignCenter)

        # Botón para "Registrar Paciente"
        self.boton_seleccionar = QPushButton("SELECCIONAR PACIENTE")
        self.boton_seleccionar.setStyleSheet("""
            QPushButton {
                background-color: #D8D8D8;
                border: 1px solid #005BBB;
                border-radius: 10px;
                font-size: 18px;
                height: 100px;
                width: 250px;
                color: #005BBB;
            }
            QPushButton:hover {
                background-color: #c0c0c0;
            }
        """)
        self.boton_seleccionar.clicked.connect(self.abrir_seleccionar_paciente)  # Conectar el botón "Registrar Paciente"
        buttons_layout.addWidget(self.boton_seleccionar, alignment=Qt.AlignCenter)

        # Añadir el layout de botones al layout principal
        main_layout.addLayout(buttons_layout)

        # Crear un espaciador debajo de los botones
        main_layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Crear un widget central para contener los elementos
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def abrir_tipo_historia(self):
        """Cierra la ventana actual y abre la ventana TipoHistoriaWindow."""
        from tipo_historia import TipoHistoriaWindow  # Import retrasado para evitar el ciclo
        self.tipo_historia_window = TipoHistoriaWindow()  # Crear la ventana anterior
        self.tipo_historia_window.show()  # Mostrar la ventana anterior
        self.close()  # Cerrar la ventana actual

    def abrir_registrar_paciente(self):
        """Cierra la ventana actual y abre la ventana RegistrarPacienteWindow."""
        from registrar_paciente import RegistrarPacienteWindow  # Importar la nueva ventana de registro de pacientes
        self.registrar_paciente_window = RegistrarPacienteWindow()  # Crear la ventana de registrar paciente
        self.registrar_paciente_window.show()  # Mostrar la ventana de registrar paciente
        self.close()  # Cerrar la ventana actual

    def abrir_seleccionar_paciente(self):
        """Cierra la ventana actual y abre la ventana SeleccionarPacienteWindow."""
        from seleccionar_paciente import SeleccionarPacienteWindow  # Importar la ventana de selección de paciente
        self.seleccionar_paciente_window = SeleccionarPacienteWindow()  # Crear la ventana de selección de paciente
        self.seleccionar_paciente_window.show()  # Mostrar la ventana de selección de paciente
        self.close()  # Cerrar la ventana actual

