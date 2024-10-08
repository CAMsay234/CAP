import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QScrollArea
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class PruebaProcesosMemoriaWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle("Prueba procesos de memoria")
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

        # Título
        self.title = QLabel("PROCESOS DE MEMORIA")
        self.title.setFont(QFont('Arial', 18, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        header_background_layout.addWidget(self.title, alignment=Qt.AlignCenter)

        # Campo de código
        self.codigo_label = QLabel("Código:")
        self.codigo_label.setFont(QFont('Arial', 12))
        self.codigo_label.setStyleSheet("color: white;")
        self.codigo_input = QLineEdit()
        self.codigo_input.setFixedWidth(100)
        header_background_layout.addWidget(self.codigo_label, alignment=Qt.AlignRight)
        header_background_layout.addWidget(self.codigo_input, alignment=Qt.AlignRight)

        header_layout.addWidget(header_background)
        main_layout.addLayout(header_layout)

        # Tabla de pruebas para "Escala de Memoria de Wechsler"
        self.add_table("ESCALA DE MEMORIA DE WECHSLER", ["INFORMACIÓN", "ORIENTACIÓN", "CONTROL MENTAL", "MEMORIA LÓGICA"], main_layout)

        # Tabla de pruebas para "Curva de Memoria Verbal"
        self.add_table("CURVA DE MEMORIA VERBAL", ["VOLUMEN INICIAL", "PUNTAJE MÁXIMO", "EVOCACIÓN DIFERIDA 20'", "NÚMERO DE ENSAYOS"], main_layout)

        # Tabla de pruebas para "Curva de Memoria Visual"
        self.add_table("CURVA DE MEMORIA VISUAL", ["VOLUMEN INICIAL", "PUNTAJE MÁXIMO", "EVOCACIÓN DIFERIDA 20'", "NÚMERO DE ENSAYOS", "FIGURA REY EVOCACIÓN", "OTRA PRUEBA"], main_layout)

        # Sección de comentarios clínicos con celdas para cada comentario
        comentarios_clinicos = [
            "Curva de aprendizaje de información verbal", "Curva de aprendizaje no verbal", 
            "Proceso de codificación, almacenamiento y evocación", "Memoria de trabajo",
            "Memoria semántica", "Memoria no verbal", "Memoria autobiográfica", 
            "Memoria a corto plazo", "Memoria largo plazo"
        ]
        self.add_comment_section("COMENTARIO CLÍNICO", comentarios_clinicos, main_layout)

        # Sección de "Conclusiones Generales"
        self.add_conclusion_section("CONCLUSIONES GENERALES", main_layout)

        # Configurar el scroll y añadir el widget principal
        scroll.setWidget(scroll_widget)
        self.setCentralWidget(scroll)

    def add_table(self, title, tests, layout):
        """Función para agregar una tabla con los datos de las pruebas."""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setStyleSheet("color: black; background-color: #B0C4DE; padding: 10px;")
        layout.addWidget(title_label)

        table_layout = QGridLayout()
        headers = ["PRUEBAS", "PUNTAJE", "MEDIA", "DS", "INTERPRETACIÓN"]
        
        # Agregar encabezados a la tabla
        for col, header in enumerate(headers):
            header_label = QLabel(header)
            header_label.setFont(QFont('Arial', 14, QFont.Bold))
            header_label.setStyleSheet("color: white; background-color: #4A90E2; padding: 10px; border-radius: 5px;")
            header_label.setAlignment(Qt.AlignCenter)
            table_layout.addWidget(header_label, 0, col)
        
        # Agregar filas de pruebas
        for row, test in enumerate(tests, start=1):
            # Nombre de la prueba
            test_label = QLabel(test)
            test_label.setFont(QFont('Arial', 12))
            test_label.setAlignment(Qt.AlignCenter)
            test_label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")
            table_layout.addWidget(test_label, row, 0)
        
            # Campos de entrada para Puntaje, Media, DS, Interpretación
            for col in range(1, 5):
                input_field = QLineEdit()
                input_field.setFixedHeight(35)
                input_field.setStyleSheet("border: 1px solid black;")  # Añadir borde
                table_layout.addWidget(input_field, row, col)
        
        layout.addLayout(table_layout)

    def add_conclusion_section(self, title, layout):
        """Función para agregar la sección de conclusiones generales con recuadro extra."""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        title_label.setStyleSheet("color: white; background-color: #6A9DE2; padding: 10px;")
        layout.addWidget(title_label)

        section_layout = QHBoxLayout()

        # Recuadro de texto de conclusiones generales
        conclusion_field = QLineEdit()
        conclusion_field.setFixedHeight(40)
        conclusion_field.setStyleSheet("border: 1px solid black;")
        section_layout.addWidget(conclusion_field)

        # Recuadro pequeño al lado
        small_field = QLineEdit()
        small_field.setFixedWidth(150)
        small_field.setFixedHeight(40)
        small_field.setStyleSheet("border: 1px solid black;")
        section_layout.addWidget(small_field)

        layout.addLayout(section_layout)

    def add_comment_section(self, title, comments, layout):
        """Añadir sección de comentarios clínicos con múltiples líneas"""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 12, QFont.Bold))
        title_label.setStyleSheet("background-color: #4A90E2; color: black; padding: 5px; border-radius: 5px;")
        layout.addWidget(title_label)
    
        # Cambiar a QGridLayout para alinear correctamente las etiquetas y las casillas
        comment_layout = QGridLayout()
        for i, comment in enumerate(comments):
            label = QLabel(comment)
            label.setFont(QFont('Arial', 12))
            label.setStyleSheet("color: black;")  # Asegurar que el texto sea negro
            label.setWordWrap(True)  # Asegurar que el texto se envuelva
            comment_layout.addWidget(label, i, 0)
    
            # Añadir campo de texto asociado al comentario
            input_field = QLineEdit()
            input_field.setFixedHeight(35)
            input_field.setStyleSheet("border: 1px solid black;")  # Añadir borde a las casillas de comentarios
            comment_layout.addWidget(input_field, i, 1)
    
        layout.addLayout(comment_layout)

# Función para ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PruebaProcesosMemoriaWindow()
    window.show()
    sys.exit(app.exec_())
