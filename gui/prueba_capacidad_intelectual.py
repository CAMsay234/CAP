import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QSpacerItem, QSizePolicy, QGridLayout, QComboBox, QDateEdit
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QDate
import requests  # Para realizar las solicitudes al backend
from datetime import datetime
from evaluacion_neuropsicologica import EvaluacionNeuropsicologicaWindow  # Importar la clase de la ventana de evaluación neuropsicológica

class PruebaCapacidadIntelectualWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle("Prueba capacidad intelectual")
        self.showMaximized()  # Abrir la ventana maximizada
        self.setStyleSheet("background-color: white;")  # Fondo blanco

        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Crear la barra azul con el logo y el campo de código
        header_layout = QHBoxLayout()

        # Crear un widget que actúe como barra azul
        header_background = QWidget()
        header_background.setStyleSheet("background-color: #005BBB;")
        header_background_layout = QHBoxLayout(header_background)
        header_background_layout.setContentsMargins(0, 0, 0, 0)

        # Logo de UPB
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        header_background_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Título
        titulo = QLabel("DATOS PERSONALES")
        titulo.setFont(QFont('Arial', 40))  # Tamaño más grande para el título principal
        titulo.setStyleSheet("color: white;")
        header_background_layout.addWidget(titulo, alignment=Qt.AlignCenter)

        # Campo de código
        codigo_layout = QVBoxLayout()
        codigo_label = QLabel("Código:")
        codigo_label.setFont(QFont('Arial', 10))
        codigo_label.setStyleSheet("color: white;")
        codigo_label.setProperty('subtitulo', True)
        codigo_layout.addWidget(codigo_label)

        # Crear el campo de texto de código
        self.codigo_input = QLineEdit()
        self.codigo_input.setText(f"{self.obtener_siguiente_codigo()}")
        self.codigo_input.setFixedWidth(100)
        codigo_layout.addWidget(self.codigo_input, alignment=Qt.AlignRight)
        header_background_layout.addLayout(codigo_layout)

        # Añadir el layout del fondo azul al header
        header_layout.addWidget(header_background)
        main_layout.addLayout(header_layout)

        # Crear un espaciador debajo de la barra azul
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))