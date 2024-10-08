import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QScrollArea, QTextEdit, QPushButton
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class PruebaAtencionConcentracionWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle("Prueba atención y concentración")
        self.showMaximized()  # Abrir la ventana maximizada
        self.setStyleSheet("background-color: white;")  # Fondo blanco

        # Crear el scroll
        scroll = QScrollArea(self)
        scroll_widget = QWidget()
        scroll.setWidgetResizable(True)
        main_layout = QVBoxLayout(scroll_widget)

        # Crear la barra azul con el logo, título y el campo de código
        header_layout = QHBoxLayout()
        header_background = QWidget()
        header_background.setStyleSheet("background-color: #005BBB;")
        header_background_layout = QHBoxLayout(header_background)

        # Logo UPB
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        header_background_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Title
        self.title = QLabel("ATENCIÓN Y CONCENTRACIÓN")
        self.title.setFont(QFont('Arial', 18, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        header_background_layout.addWidget(self.title, alignment=Qt.AlignCenter)

        # Field for Código
        self.codigo_label = QLabel("Código:")
        self.codigo_label.setFont(QFont('Arial', 12))
        self.codigo_label.setStyleSheet("color: white;")
        self.codigo_input = QLineEdit()
        self.codigo_input.setFixedWidth(100)
        header_background_layout.addWidget(self.codigo_label, alignment=Qt.AlignRight)
        header_background_layout.addWidget(self.codigo_input, alignment=Qt.AlignRight)

        header_layout.addWidget(header_background)
        main_layout.addLayout(header_layout)
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
        self.boton_volver.clicked.connect(self.abrir_evaluacion_neuropsicologica)  # Conectar el botón para volver
        header_background_layout.addWidget(self.boton_volver, alignment=Qt.AlignRight)
 
        # Botón "Guardar" en la esquina derecha
        self.boton_guardar = QPushButton("GUARDAR")
        self.boton_guardar.setStyleSheet("""
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
        self.boton_guardar.clicked.connect(self.abrir_guardar)  # Conectar el botón para guardar
        header_background_layout.addWidget(self.boton_guardar, alignment=Qt.AlignRight)

        # Tabla de pruebas
        table_layout = QGridLayout()
        headers = ["PRUEBAS", "PUNTAJE", "MEDIA", "DS", "INTERPRETACIÓN"]
        tests = [
            "Dígitos", "CPT Auditivo Aciertos", "CPT Auditivo Omisiones", "CPT Visuales Aciertos",
            "CPT Visuales Omisiones", "Control Mental", "Claves (WISC-III)", "Otra Prueba"
        ]
        
        # Agregar encabezados a la tabla
        for col, header in enumerate(headers):
            header_label = QLabel(header)
            header_label.setFont(QFont('Arial', 14, QFont.Bold))
            header_label.setStyleSheet("color: white; background-color: #4A90E2; padding: 10px;")
            header_label.setAlignment(Qt.AlignCenter)
            table_layout.addWidget(header_label, 0, col)
        
        # Agregar filas de pruebas
        for row, test in enumerate(tests, start=1):
            # Nombre de la prueba
            test_label = QLabel(test)
            test_label.setAlignment(Qt.AlignCenter)
            test_label.setProperty("pruebas", True)
            test_label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")
            test_label.setMinimumWidth(500)
            table_layout.addWidget(test_label, row, 0)
        
            # Campos de entrada para Puntaje, Media, DS, Interpretación
            for col in range(1, 5):
                input_field = QLineEdit()
                input_field.setStyleSheet("border: 1px solid black;")
                input_field.setFixedHeight(35)
                table_layout.addWidget(input_field, row, col)
        
        main_layout.addLayout(table_layout)
        
        # Sección de "Tachado de Cuadros"
        self.add_section("TACHADO DE CUADROS", ["Aciertos 48/", "Errores", "Tiempo"], main_layout)
        
        # Sección de "Test de Rastreo de Caminos A."
        self.add_section("TEST DE RASTREOS DE CAMINOS A.", ["Tiempo", "Curva de Memoria. Span"], main_layout)
        
        # Sección de comentarios clínicos
        comentarios_clinicos = [
            "Focalizada: Capacidad para dar respuesta de un modo diferenciado a estímulos sensoriales específicos",
            "Sostenida: Capacidad para mantener una determinada respuesta conductual...",
            "Alternante: Capacidad para cambiar el foco de atención desde un estímulo a otro...",
            "Selectiva: Permite prestar atención a las características del ambiente...",
            "Dividida: Capacidad para responder simultáneamente a diferentes estímulos..."
        ]

        self.add_comment_section("COMENTARIO CLÍNICO: MODALIDADES DE ATENCIÓN EVALUADAS", comentarios_clinicos, main_layout)

        # Sección de "Conclusiones Generales"
        self.add_section("CONCLUSIONES GENERALES", [], main_layout, multiline=True)

        # Configurar el scroll y añadir el widget principal
        scroll.setWidget(scroll_widget)
        self.setCentralWidget(scroll)

    def add_section(self, title, fields, layout, multiline=False):
        """Añadir secciones con campos de entrada de texto"""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        title_label.setStyleSheet("background-color: #4A90E2; color: white; padding: 5px; border-radius: 5px;")
        layout.addWidget(title_label)
    
        section_layout = QGridLayout()
        for i, field in enumerate(fields):
            label = QLabel(field)
            label.setFont(QFont('Arial', 12))
            label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")  # Letra negra y fondo gris
            label.setProperty("pruebas", True)  # Marcar como campo de entrada
            label.setMinimumWidth(500)  # Ajustar altura mínima
            section_layout.addWidget(label, i, 0)
    
            # Añadir campos de entrada para Puntaje, Media, DS, Interpretación
            for col in range(1, 5):
                input_field = QLineEdit()
                input_field.setStyleSheet("border: 1px solid black;")
                input_field.setFixedHeight(35)  # Ajustar altura fija
                section_layout.addWidget(input_field, i, col)
    
        # Añadir un QTextEdit si multiline es True
        if multiline:
            text_edit = QTextEdit()
            text_edit.setFont(QFont('Arial', 12))
            text_edit.setStyleSheet("border: 1px solid black;")
            text_edit.setFixedHeight(150)  # Ajustar altura fija
            layout.addWidget(text_edit)
    
        layout.addLayout(section_layout)

    def add_comment_section(self, title, comments, layout):
        """Añadir sección de comentarios clínicos con múltiples líneas"""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 14, QFont.Bold))  # Letra más pequeña
        title_label.setStyleSheet("background-color: #4A90E2; color: white; padding: 5px; border-radius: 5px;")  # Fondo azul claro y letra blanca
        layout.addWidget(title_label)
    
        comment_layout = QGridLayout()
        for i, comment in enumerate(comments):
            label = QLabel(comment)
            label.setFont(QFont('Arial', 14)) 
            label.setProperty("comentarios", True) # Letra más pequeña
            label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")  # Letra negra y fondo gris
            label.setWordWrap(True)  # Asegurar que el texto se envuelva
            comment_layout.addWidget(label, i, 0)
        
            # Añadir campo de texto asociado al comentario
            input_field = QTextEdit()
            input_field.setFont(QFont('Arial', 12))
            input_field.setStyleSheet("border: 1px solid black;")  # Añadir borde a las casillas de comentarios
            input_field.setFixedHeight(150)  # Ajustar altura fija
            comment_layout.addWidget(input_field, i, 1)
    
        layout.addLayout(comment_layout)

    def abrir_evaluacion_neuropsicologica(self):
            """Función para abrir la ventana de Evaluación Neuropsicológica."""
            from evaluacion_neuropsicologica import EvaluacionNeuropsicologicaWindow  # Importar la nueva ventana de registro de pacientes
            self.evaluacion_neuropsicologica_window = EvaluacionNeuropsicologicaWindow()  # Crear la ventana de registrar paciente
            self.evaluacion_neuropsicologica_window.show()  # Mostrar la ventana de registrar paciente
            self.close()  # Cerrar la ventana actual # Importar la nueva ventana de registro de pacientes

    def abrir_guardar(self):
        """Función para guardar los datos de la prueba en la base de datos."""
    pass

# Función para ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PruebaAtencionConcentracionWindow()
    window.show()
    sys.exit(app.exec_())