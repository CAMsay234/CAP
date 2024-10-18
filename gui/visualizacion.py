import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QLabel, QFrame
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class VisualizacionWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()
        self.paciente_seleccionado = paciente_seleccionado

        # Configurar ventana
        self.setWindowTitle("Visualización Capacidad Intelectual")
        self.setGeometry(100, 100, 1000, 700)  # Tamaño controlado

        # Crear widget principal y layout
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Encabezado con logo y título
        header_layout = self.create_header()
        main_layout.addLayout(header_layout)

        # Recuadro para la gráfica
        graph_frame = QFrame()
        graph_frame.setStyleSheet("border: 2px solid #005BBB; background-color: #F0F0F0;")
        graph_layout = QVBoxLayout(graph_frame)
        
        # Añadir gráfica
        self.add_graph(graph_layout)

        # Añadir recuadro al layout principal
        main_layout.addWidget(graph_frame)

    def create_header(self):
        """Crea el encabezado con logo y título."""
        header_layout = QHBoxLayout()

        # Logo
        logo_label = QLabel()
        logo_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')
        pixmap = QPixmap(logo_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        header_layout.addWidget(logo_label)

        # Título
        title = QLabel("VISUALIZACIÓN CAPACIDAD INTELECTUAL")
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setStyleSheet("color: #005BBB;")
        header_layout.addWidget(title, alignment=Qt.AlignCenter)

        return header_layout

    def add_graph(self, layout):
        """Genera y agrega la gráfica."""
        puntuaciones = self.obtener_puntuaciones()
        if not puntuaciones:
            print("No se encontraron puntuaciones.")
            return

        # Crear figura y gráfica
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_ylim(1, 19)
        ax.set_yticks(range(1, 20))

        for categoria, subpruebas in puntuaciones.items():
            labels = list(subpruebas.keys())
            scores = list(subpruebas.values())
            ax.plot(labels, scores, marker='o', label=categoria)

        ax.set_title("Perfil de Puntuaciones", fontsize=14)
        ax.set_xlabel("Subpruebas", fontsize=12)
        ax.set_ylabel("Puntuación", fontsize=12)
        ax.legend(loc='upper right')
        ax.grid(True, linestyle='--', alpha=0.7)

        # Integrar gráfica en el layout de PyQt
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

    def obtener_puntuaciones(self):
        """Obtiene las puntuaciones desde la API."""
        url = f'http://localhost:5000/evaluaciones/{self.paciente_seleccionado["codigo_hc"]}/6'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                categorias = {
                    "Comprensión Verbal": ["SEMEJANZAS", "VOCABULARIO", "INFORMACIÓN", "COMPRENSIÓN"],
                    "Razonamiento Perceptual": ["DISEÑO CON CUBOS", "MATRICES", "ROMPECABEZAS VISUAL",
                                                "PESO FIGURADO", "FIGURAS INCOMPLETAS"],
                    "Memoria de Trabajo": ["RETENCIÓN DE DÍGITOS", "ARITMÉTICA", "SUCESIÓN DE NÚMEROS Y LETRAS"],
                    "Velocidad de Procesamiento": ["BÚSQUEDA DE SÍMBOLOS", "CLAVES", "CANCELACIÓN"]
                }

                subpruebas_map = {
                    1: "SEMEJANZAS", 2: "VOCABULARIO", 3: "INFORMACIÓN", 4: "COMPRENSIÓN",
                    5: "DISEÑO CON CUBOS", 6: "MATRICES", 7: "ROMPECABEZAS VISUAL",
                    8: "PESO FIGURADO", 9: "FIGURAS INCOMPLETAS", 10: "RETENCIÓN DE DÍGITOS",
                    11: "ARITMÉTICA", 12: "SUCESIÓN DE NÚMEROS Y LETRAS", 13: "BÚSQUEDA DE SÍMBOLOS",
                    14: "CLAVES", 15: "CANCELACIÓN"
                }

                puntuaciones = {cat: {} for cat in categorias}
                for evaluacion in data:
                    subprueba = subpruebas_map.get(evaluacion['id_subprueba'], "Desconocido")
                    escalar = int(evaluacion['escalar'])

                    for categoria, subpruebas in categorias.items():
                        if subprueba in subpruebas:
                            puntuaciones[categoria][subprueba] = escalar

                return puntuaciones
            else:
                print(f"Error {response.status_code}: {response.text}")
                return {}
        except requests.exceptions.RequestException as e:
            print(f"Error al conectar con la API: {e}")
            return {}

# Ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    paciente = {"codigo_hc": 1, "nombre": "Luisa Flórez"}
    window = VisualizacionWindow(paciente)
    window.show()
    sys.exit(app.exec_())
