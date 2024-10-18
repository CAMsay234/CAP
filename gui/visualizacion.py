from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class VisualizacionWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Visualización Capacidad Intelectual")
        self.setGeometry(0, 0, 1800, 697) # Tamaño manejable y seguro

        # Crear widget principal y layout
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Mostrar logo y título
        self.add_header(main_layout)

        # Añadir la gráfica directamente
        self.add_graph(main_layout)

    def add_header(self, layout):
        """Agregar encabezado con logo y título."""
        title = QLabel("Visualización Capacidad Intelectual")
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

    def add_graph(self, layout):
        """Generar y agregar la gráfica."""
        puntuaciones = self.obtener_puntuaciones()
        if not puntuaciones:
            print("No se encontraron puntuaciones.")
            return

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.set_ylim(1, 19)
        ax.set_yticks(range(1, 20))

        for categoria, subpruebas in puntuaciones.items():
            labels = list(subpruebas.keys())
            scores = list(subpruebas.values())
            ax.plot(labels, scores, marker='o', label=categoria)

        ax.set_title("Perfil de Puntuaciones", fontsize=14)
        ax.set_xlabel("Subpruebas")
        ax.set_ylabel("Puntuación")
        ax.legend(loc='upper right')
        ax.grid(True, linestyle='--', alpha=0.7)

        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

    def obtener_puntuaciones(self):
        """Obtener puntuaciones desde la API."""
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
