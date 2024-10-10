import sys
import os
import requests
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QWidget, QScrollArea, QFormLayout, QSpacerItem, QSizePolicy, QDialog, QApplication
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from areas import AreasWindow
from estado_mental import EstadoMentalWindow

class HistoriaClinicaWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()

        self.paciente_seleccionado = paciente_seleccionado  # Datos del paciente seleccionado

        # Configurar la ventana
        self.setWindowTitle(f"Historia Clínica de {self.paciente_seleccionado['nombre']}")
        self.showMaximized()
        self.setStyleSheet("background-color: white;")

        # Layout principal
        main_layout = QVBoxLayout()

        # Crear la barra azul con el logo y el botón de "Volver"
        header_layout = QHBoxLayout()

        # Crear un widget que actúe como barra azul
        header_background = QWidget()
        header_background.setStyleSheet("background-color: #005BBB;")
        header_background_layout = QHBoxLayout(header_background)
        header_background_layout.setContentsMargins(0, 0, 0, 0)

        # Logo de UPB
        logo_label = QLabel()
        logo_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'src', 'upb.png')).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        header_background_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        # Título
        titulo = QLabel("HISTORIA CLÍNICA")
        titulo.setFont(QFont('Arial', 24))
        titulo.setStyleSheet("color: white;")
        header_background_layout.addWidget(titulo, alignment=Qt.AlignCenter)

        # Botón "Volver" en la esquina superior derecha
        self.boton_volver = QPushButton("Volver")
        self.boton_volver.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #005BBB;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 14px;
                min-width: 80px;
                border: 1px solid #005BBB;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.boton_volver.clicked.connect(self.volver_a_seleccionar_registrar)
        header_background_layout.addWidget(self.boton_volver, alignment=Qt.AlignRight)

        # Añadir el layout del fondo azul al header
        header_layout.addWidget(header_background)
        main_layout.addLayout(header_layout)

        # Añadir los campos de "Código" y "Nombre" debajo del banner
        paciente_info_layout = QHBoxLayout()

        codigo_label = QLabel(f"Código: {self.paciente_seleccionado['codigo_hc']}")
        codigo_label.setProperty("subtitulo", True)
        paciente_info_layout.addWidget(codigo_label, alignment=Qt.AlignLeft)

        nombre_label = QLabel(f"Nombre: {self.paciente_seleccionado['nombre']}")
        nombre_label.setProperty("subtitulo", True)
        paciente_info_layout.addWidget(nombre_label, alignment=Qt.AlignLeft)

        main_layout.addLayout(paciente_info_layout)

        # Crear un espaciador debajo de los datos del paciente
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Scroll area para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        # Crear un widget central para la parte de formulario
        scroll_content = QWidget()
        scroll_layout = QFormLayout(scroll_content)

        # Campos del formulario con borde y en QTextEdit
        campos = [
            ("Motivo de consulta", "Ingrese el motivo de consulta del paciente"),
            ("Estado actual", "Describa el estado actual del paciente"),
            ("Historia médica y psiquiátrica anterior", "Ingrese la historia médica y psiquiátrica anterior"),
            ("Antecedentes psiquiátricos familiares", "Ingrese antecedentes psiquiátricos familiares"),
            ("Historia personal", "Ingrese la historia personal del paciente"),
            ("Historia de la dinámica familiar", "Ingrese la historia de la dinámica familiar")
        ]

        for label, placeholder in campos:
            label_widget = QLabel(f"{label}:")
            label_widget.setFont(QFont('Arial', 18))
            label_widget.setStyleSheet("color:black;")
            input_widget = QTextEdit()  # Cambiado a QTextEdit
            input_widget.setPlaceholderText(placeholder)
            input_widget.setFont(QFont('Arial', 12))
            input_widget.setStyleSheet("""
                QTextEdit {
                    border: 1px solid #005BBB;
                    padding: 5px;
                    height: 100px;  /* Aumenta la altura para permitir múltiples líneas */
                }
            """)
            scroll_layout.addRow(label_widget, input_widget)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

        # Crear los botones en la parte inferior
        button_layout = QVBoxLayout()

        # Crear los botones para subpestañas
        sub_buttons_layout = QHBoxLayout()

        estado_mental_button = QPushButton("Estado Mental")
        estado_mental_button.setFont(QFont('Arial', 16))
        estado_mental_button.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                padding: 10px;
                border-radius: 5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #003F73;
            }
        """)
        estado_mental_button.clicked.connect(self.abrir_estado_mental)
        sub_buttons_layout.addWidget(estado_mental_button)

        areas_button = QPushButton("Áreas")
        areas_button.setFont(QFont('Arial', 16))
        areas_button.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                padding: 10px;
                border-radius: 5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #003F73;
            }
        """)
        areas_button.clicked.connect(self.abrir_areas)
        sub_buttons_layout.addWidget(areas_button)

        button_layout.addLayout(sub_buttons_layout)

        # Botón para guardar historia clínica
        boton_guardar = QPushButton("Guardar historia clínica")
        boton_guardar.setFont(QFont('Arial', 16))
        boton_guardar.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                padding: 10px;
                border-radius: 5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #003F73;
            }
        """)
        button_layout.addWidget(boton_guardar, alignment=Qt.AlignCenter)

        # Añadir el layout de botones al layout principal
        main_layout.addLayout(button_layout)

        # Crear el widget principal
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)



    def volver_a_seleccionar_registrar(self):
        # Ir a la ventana de seleccionar_registrar_paciente.py
        from seleccionar_registrar_paciente import SeleccionarRegistrarPacienteWindow
        self.seleccionar_registrar_window = SeleccionarRegistrarPacienteWindow()
        self.seleccionar_registrar_window.show()
        self.close()  # Cerrar la ventana actual

    def abrir_estado_mental(self):
        if hasattr(self, 'paciente_seleccionado'):
            self.estado_mental = EstadoMentalWindow(self.paciente_seleccionado)
            self.estado_mental.show()


    def abrir_areas(self):
        if hasattr(self, 'paciente_seleccionado'):
            self.areas = AreasWindow(self.paciente_seleccionado)
            self.areas.show()
    
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    paciente = {'codigo_hc': 1, 'nombre': 'Camilo Velasquez'}
    window = HistoriaClinicaWindow(paciente)
    window.show()
    sys.exit(app.exec_())
