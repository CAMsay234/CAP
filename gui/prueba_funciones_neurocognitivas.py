import os
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QWidget, QSpacerItem, QSizePolicy, QGridLayout, QScrollArea
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class PruebaFuncionesNeurocognitivasWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle("Prueba funciones neurocognitivas")
        self.showMaximized()  # Abrir la ventana maximizada
        self.setStyleSheet("background-color: white;")  # Fondo blanco

        # Scroll Area para contener todo el contenido largo
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()  # El widget que contendrá todo el layout
        scroll_layout = QVBoxLayout(scroll_content)

        # Crear la barra azul con el logo y el campo de código
        header_layout = QHBoxLayout()
        header_background = QWidget()
        header_background.setStyleSheet("background-color: #005BBB;")
        header_background_layout = QHBoxLayout(header_background)
        header_background_layout.setContentsMargins(0, 0, 0, 0)

        # Logo de UPB
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        header_background_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Título de la sección
        titulo = QLabel("FUNCIONES NEUROCOGNITIVAS (GNOSIAS Y PRAXIAS)")
        titulo.setFont(QFont('Arial', 24))  # Tamaño más grande para el título principal
        titulo.setStyleSheet("color: white;")
        header_background_layout.addWidget(titulo, alignment=Qt.AlignCenter)

        # Campo de código
        codigo_layout = QVBoxLayout()
        codigo_label = QLabel("Código:")
        codigo_label.setFont(QFont('Arial', 10))
        codigo_label.setStyleSheet("color: white;")
        codigo_layout.addWidget(codigo_label)

        # Crear el campo de texto de código
        self.codigo_input = QLineEdit()
        self.codigo_input.setFixedWidth(100)
        codigo_layout.addWidget(self.codigo_input, alignment=Qt.AlignRight)
        header_background_layout.addLayout(codigo_layout)

        header_layout.addWidget(header_background)
        scroll_layout.addLayout(header_layout)

        # Crear un espaciador debajo de la barra azul
        scroll_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Sección de la tabla: DIMENSIÓN NEUROCOGNITIVA - PUNTAJE - INTERPRETACIÓN
        section_titles = ["DIMENSIÓN NEUROCOGNITIVA", "PUNTAJE", "INTERPRETACIÓN"]
        neurocognitive_functions = [
            "ESTEROGNOSIA NÚMEROS", "ESTEROGNOSIA LETRAS", "ESTEROGNOSIA FORMAS",
            "GRAFESTESIA NÚMEROS", "GRAFESTESIA FORMAS", "DISCRIMINACIÓN AUDITIVA",
            "PRAXIAS IDEACIONALES", "PRAXIAS IDEOMOTORAS", "PRAXIAS CONSTRUC BIDIMEN.",
            "PRAXIAS CONSTRUC TRIDIMEN.", "OTRA PRUEBA"
        ]

        grid_functions = QGridLayout()
        for i, title in enumerate(section_titles):
            label = QLabel(title)
            label.setFont(QFont('Arial', 12, QFont.Bold))
            grid_functions.addWidget(label, 0, i)

        for row, function in enumerate(neurocognitive_functions, start=1):
            function_label = QLabel(function)
            function_label.setFont(QFont('Arial', 10))
            grid_functions.addWidget(function_label, row, 0)

            # Crear campos de texto para "PUNTAJE" y "INTERPRETACIÓN"
            for col in range(1, 3):
                input_field = QLineEdit()
                input_field.setFixedHeight(30)
                grid_functions.addWidget(input_field, row, col)

        scroll_layout.addLayout(grid_functions)

        # Sección "Comentario Clínico"
        self.add_title("COMENTARIO CLÍNICO", scroll_layout)
        clinical_comments = [
            "PROCESOS VISO-PERCEPTUALES", "PROCESOS VISO-ESPACIALES", "PROCESOS VISO-MOTORES"
        ]
        self.add_comment_section(clinical_comments, scroll_layout)

        # Sección "Conclusiones Generales"
        self.add_title("CONCLUSIONES GENERALES", scroll_layout)
        conclusions_input = QLineEdit()
        conclusions_input.setFixedHeight(40)
        scroll_layout.addWidget(conclusions_input)

        # Configurar el widget principal para el scroll y añadir todo el layout
        scroll_area.setWidget(scroll_content)
        self.setCentralWidget(scroll_area)

    def add_title(self, title, layout):
        """Función para añadir títulos a cada sección."""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        title_label.setStyleSheet("background-color: #B0C4DE; padding: 10px;")
        layout.addWidget(title_label)

    def add_comment_section(self, comments, layout):
        """Añadir comentarios clínicos en la sección de comentarios."""
        grid = QGridLayout()
        for i, comment in enumerate(comments):
            label = QLabel(comment)
            grid.addWidget(label, i, 0)

            # Campo de texto al lado de cada comentario
            input_field = QLineEdit()
            input_field.setFixedHeight(30)
            grid.addWidget(input_field, i, 1)

        layout.addLayout(grid)


# Ejecutar la aplicación
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ventana = PruebaFuncionesNeurocognitivasWindow()
    ventana.show()
    sys.exit(app.exec_())


