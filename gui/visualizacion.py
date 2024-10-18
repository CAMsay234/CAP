import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QScrollArea, QPushButton, QGridLayout
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt


class VisualizacionWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()
        self.paciente_seleccionado = paciente_seleccionado
        # Configurar la ventana
        self.setWindowTitle("Visualizaciones")
        self.showMaximized()  # Abrir la ventana maximizada
        self.setStyleSheet("background-color: white;")  # Fondo blanco

        # Crear el widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # ---- LATERAL IZQUIERDO CON NÚMEROS ----
        self.crear_lateral_izquierdo(main_layout)

        # Crear el scroll
        scroll = QScrollArea(self)
        scroll_widget = QWidget()
        scroll.setWidgetResizable(True)
        scroll.setWidget(scroll_widget)
        scroll_layout = QVBoxLayout(scroll_widget)

        # ---- BARRA AZUL SUPERIOR ----
        header_background = QWidget()
        header_background.setFixedHeight(100)  # Fijamos altura de la barra azul
        header_background.setStyleSheet("background-color: #005BBB;")
        header_layout = QHBoxLayout(header_background)
        header_layout.setContentsMargins(10, 0, 10, 0)
        header_layout.setSpacing(20)

        # Logo UPB
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Tamaño ajustado
        self.logo.setPixmap(pixmap)
        header_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Título de la ventana
        self.title = QLabel("VISUALIZACIONES")
        self.title.setFont(QFont('Arial', 24, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        header_layout.addWidget(self.title, alignment=Qt.AlignCenter)

        # Campo de código del paciente
        self.codigo_label = QLabel(f"Código: {self.paciente_seleccionado['codigo_hc']}")
        self.codigo_label.setFont(QFont('Arial', 14))
        self.codigo_label.setStyleSheet("color: white;")
        header_layout.addWidget(self.codigo_label, alignment=Qt.AlignRight)

        # Botón Volver
        self.boton_volver = QPushButton("VOLVER")
        self.boton_volver.setFixedSize(80, 30)
        self.boton_volver.setStyleSheet(self.boton_style())
        self.boton_volver.clicked.connect(self.abrir_evaluacion_neuropsicologica)
        header_layout.addWidget(self.boton_volver, alignment=Qt.AlignRight)

        # Botón Guardar
        self.boton_guardar = QPushButton("GUARDAR")
        self.boton_guardar.setFixedSize(80, 30)
        self.boton_guardar.setStyleSheet(self.boton_style())
        header_layout.addWidget(self.boton_guardar, alignment=Qt.AlignRight)

        # Agregar la barra azul al layout principal
        scroll_layout.addWidget(header_background)

        # ---- TÍTULO DE LA GRÁFICA ----
        grafica_title = QLabel("PERFIL DE PUNTUACIONES ESCALARES DE LAS SUBPRUEBAS")
        grafica_title.setFont(QFont('Arial', 16, QFont.Bold))
        grafica_title.setStyleSheet("background-color: #B0C4DE; padding: 10px; border-radius: 5px;")
        grafica_title.setAlignment(Qt.AlignCenter)
        grafica_title.setFixedHeight(50)  # Fijamos la altura del título
        scroll_layout.addWidget(grafica_title)

        # ---- SEPARACIÓN DE LAS SECCIONES SUPERIORES ----
        self.crear_secciones_superiores(scroll_layout)

        main_layout.addWidget(scroll)

    def boton_style(self):
        """Estilo para los botones."""
        return """
            QPushButton {
                background-color: white;
                border: 1px solid #005BBB;
                border-radius: 5px;
                color: #005BBB;
                font-size: 12px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """

    def abrir_evaluacion_neuropsicologica(self):
        """Abrir la ventana de evaluación neuropsicológica."""
        print("Volviendo a la evaluación neuropsicológica...")
        self.close()

    def crear_secciones_superiores(self, layout):
        """Crear las secciones superiores con recuadros."""
        secciones = ["Comprensión Verbal", "Razonamiento Perceptual", "Memoria de Trabajo", "Velocidad de Procesamiento"]
        secciones_layout = QHBoxLayout()
        secciones_layout.setSpacing(10)

        for seccion in secciones:
            label = QLabel(seccion)
            label.setFont(QFont('Arial', 10, QFont.Bold))
            label.setStyleSheet("background-color: #E0E0E0; padding: 5px; border-radius: 5px;")
            label.setAlignment(Qt.AlignCenter)
            secciones_layout.addWidget(label)

        layout.addLayout(secciones_layout)

    def crear_lateral_izquierdo(self, layout):
        """Crear los recuadros de la parte lateral izquierda con los números correspondientes."""
        lateral_widget = QWidget()
        lateral_layout = QVBoxLayout(lateral_widget)
        lateral_layout.setSpacing(5)

        # Añadir los números en el lateral izquierdo (de 19 a 1)
        for i in range(19, 0, -1):
            label = QLabel(str(i))
            label.setFont(QFont('Arial', 10))
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("background-color: #F0F0F0; padding: 3px; border: 1px solid #C0C0C0; border-radius: 3px;")
            lateral_layout.addWidget(label)

        layout.addWidget(lateral_widget, alignment=Qt.AlignLeft)


# Función para ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    paciente = {'codigo_hc': '12345'}  # Ejemplo de datos del paciente
    window = VisualizacionWindow(paciente)
    window.show()
    sys.exit(app.exec_())
