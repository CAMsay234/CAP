import sys
import os
import requests
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QScrollArea, QFormLayout, QSpacerItem, QSizePolicy, QApplication
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class HistoriaClinicaWindow(QMainWindow):
    def __init__(self, paciente):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle(f"Historia Clínica de {paciente['nombre']}")
        self.showMaximized()
        self.setStyleSheet("background-color: white;")

        # Layout principal
        main_layout = QVBoxLayout()

        # Crear la barra azul con el logo y el campo de código
        header_layout = QHBoxLayout()

        # Crear un widget que actúe como barra azul
        header_background = QWidget()
        header_background.setStyleSheet("background-color: #005BBB;")
        header_background_layout = QHBoxLayout(header_background)
        header_background_layout.setContentsMargins(0, 0, 0, 0)

        # Logo de UPB
        logo_label = QLabel()
        logo_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'src', 'upb.png')).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        header_background_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        # Título
        titulo = QLabel("HISTORIA CLÍNICA")
        titulo.setFont(QFont('Arial', 24))
        titulo.setStyleSheet("color: white;")
        header_background_layout.addWidget(titulo, alignment=Qt.AlignCenter)

        # Campo de código y nombre
        codigo_layout = QVBoxLayout()
        codigo_label = QLabel("Código:")
        codigo_label.setFont(QFont('Arial', 14))
        codigo_label.setStyleSheet("color: white;")
        codigo_layout.addWidget(codigo_label, alignment=Qt.AlignRight)

        self.codigo_input = QLineEdit()
        self.codigo_input.setText(str(paciente['codigo_hc']))  # Mostrar el código del paciente
        self.codigo_input.setFixedWidth(100)
        codigo_layout.addWidget(self.codigo_input, alignment=Qt.AlignRight)

        nombre_label = QLabel("Nombre paciente:")
        nombre_label.setFont(QFont('Arial', 14))
        nombre_label.setStyleSheet("color: white;")
        codigo_layout.addWidget(nombre_label, alignment=Qt.AlignRight)

        self.nombre_input = QLineEdit()
        self.nombre_input.setText(paciente['nombre'])  # Mostrar el nombre del paciente
        self.nombre_input.setFixedWidth(200)
        codigo_layout.addWidget(self.nombre_input, alignment=Qt.AlignRight)

        header_background_layout.addLayout(codigo_layout)

        # Añadir el layout del fondo azul al header
        header_layout.addWidget(header_background)
        main_layout.addLayout(header_layout)

        # Crear un espaciador debajo de la barra azul
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Scroll area para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # Crear un widget central para la parte de formulario
        scroll_content = QWidget()
        scroll_layout = QFormLayout(scroll_content)

        # Campos del formulario
        campos = [
            ("Motivo de consulta", "Ingrese el motivo de consulta del paciente"),
            ("Estado actual", "Describa el estado actual del paciente"),
            ("Historia médica y psiquiátrica anterior", "Ingrese la historia médica y psiquiátrica anterior"),
            ("Antecedentes psiquiátricos familiares", "Ingrese antecedentes psiquiátricos familiares"),
            ("Historial personal", "Situaciones significativas (comportamentales, emocionales y socioafectivas)"),
            ("Historial de la dinámica familiar relevante", "Describa la dinámica familiar relevante"),
            ("Atención", "Describa la atención del paciente"),
            ("Memoria", "Describa la memoria del paciente"),
            ("Lenguaje", "Describa el lenguaje del paciente"),
            ("Pensamiento", "Describa el pensamiento del paciente"),
            ("Introspección", "Describe la introspección del paciente"),
            ("Familiar", "Describa la información familiar del paciente"),
            ("Pareja", "Describa la información sobre la pareja del paciente"),
            ("Social", "Describa la información social del paciente"),
            ("Laboral", "Describa la información laboral del paciente"),
        ]

        for label, placeholder in campos:
            label_widget = QLabel(f"{label}:")
            label_widget.setFont(QFont('Arial', 14))
            input_widget = QLineEdit()
            input_widget.setPlaceholderText(placeholder)
            input_widget.setFont(QFont('Arial', 12))
            scroll_layout.addRow(label_widget, input_widget)

        # Botón para guardar historia clínica
        boton_guardar = QPushButton("Guardar historia clínica")
        boton_guardar.setFont(QFont('Arial', 16))
        boton_guardar.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #003F73;
            }
        """)
        scroll_layout.addRow(boton_guardar)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Crear el widget principal
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Ejemplo de datos de paciente (aquí podrías pasar los datos reales)
    paciente_ejemplo = {
        'codigo_hc': 1234,
        'nombre': 'Camilo Velasquez',
        'documento': '1025640088',
        'edad': 20,
        'telefono': '3218360814',
        'celular': '3193370656',
        'remision': 'Neuropsiquiatra'
    }

    window = HistoriaClinicaWindow(paciente_ejemplo)
    window.show()
    sys.exit(app.exec_())

