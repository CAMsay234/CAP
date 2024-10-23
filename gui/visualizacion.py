from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import requests
import unicodedata

class VisualizacionWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()

        # Asignar paciente_seleccionado como un atributo de la instancia
        self.paciente_seleccionado = paciente_seleccionado

        # Configuración de la ventana principal
        self.setWindowTitle("Visualización Capacidad Intelectual")
        self.setGeometry(0, 0, 1800, 697)  # Tamaño manejable y seguro

        # Crear widget principal y layout
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Mostrar logo y título
        self.add_header(main_layout)

        # Añadir gráfico
        self.add_graph(main_layout)

    def add_header(self, layout):
        # Añadir logo y título
        logo_label = QLabel(self)
        logo_pixmap = QPixmap('gui/src/upb.png').scaled(100, 100, Qt.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        title_label = QLabel("Capacidad Intelectual", self)
        title_label.setFont(QFont('Arial', 24))
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

    def add_graph(self, layout):
        # Cambiar el tamaño de la figura
        fig, ax = plt.subplots(figsize=(14, 7))  # Tamaño ajustado
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        # Obtener subpruebas y escalares
        categorias = self.obtener_puntuaciones()

        # Definir colores para cada categoría
        colores_categoria = {
            "Comprensión Verbal": "blue",
            "Razonamiento Perceptual": "orange",
            "Memoria de Trabajo": "green",
            "Velocidad de Procesamiento": "red"
        }

        # Depuración: Imprimir categorías obtenidas
        for categoria, (subpruebas, escalares) in categorias.items():
            print(f"{categoria} - Subpruebas obtenidas:", subpruebas)
            print(f"{categoria} - Escalares obtenidos:", escalares)

        # Graficar escalares por categoría con diferentes colores
        all_subpruebas = []
        all_escalares = []
        all_colores = []

        for categoria, (subpruebas, escalares) in categorias.items():
            if subpruebas and escalares:
                indices = list(range(len(all_subpruebas), len(all_subpruebas) + len(subpruebas)))
                ax.plot(indices, escalares, marker='o', linestyle='-', color=colores_categoria[categoria], label=categoria)
                all_subpruebas.extend(subpruebas)
                all_escalares.extend(escalares)
                all_colores.extend([colores_categoria[categoria]] * len(subpruebas))

        # Ajustes de estilo y etiquetas
        ax.set_title('Perfil de Puntuaciones Escalares de las Subpruebas', fontsize=18)  # Fuente ajustada
        ax.set_xlabel('Subpruebas', fontsize=14)  # Fuente ajustada
        ax.set_ylabel('Puntuación Escalar', fontsize=14)  # Fuente ajustada
        ax.set_yticks(range(1, 20))
        ax.set_ylim(1, 19)
        ax.legend(handles=[
            plt.Line2D([0], [0], color=colores_categoria["Comprensión Verbal"], marker='o', label="Comprensión Verbal"),
            plt.Line2D([0], [0], color=colores_categoria["Razonamiento Perceptual"], marker='o', label="Razonamiento Perceptual"),
            plt.Line2D([0], [0], color=colores_categoria["Memoria de Trabajo"], marker='o', label="Memoria de Trabajo"),
            plt.Line2D([0], [0], color=colores_categoria["Velocidad de Procesamiento"], marker='o', label="Velocidad de Procesamiento"),
        ], title='Categorías', loc='upper right')

        # Ajuste de los ticks del eje X para que los puntos estén más cercanos
        ax.set_xticks(range(len(all_subpruebas)))
        ax.set_xticklabels([self.obtener_iniciales(subprueba) for subprueba in all_subpruebas], rotation=45, ha='right', fontsize=10)

        # Ajuste de márgenes
        fig.tight_layout(pad=2.0)

        # Remover bordes innecesarios
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Añadir una cuadrícula
        ax.grid(True, linestyle='--', alpha=0.7)

    def obtener_puntuaciones(self):
        # Obtener el ID de la prueba de capacidad intelectual
        id_prueba = self.obtener_id_prueba("Capacidad Intelectual")
        if not id_prueba:
            return {}

        # Obtener puntuaciones desde el backend
        url = f'http://localhost:5000/evaluaciones/{self.paciente_seleccionado["codigo_hc"]}/{id_prueba}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            subpruebas_ids = [item['id_subprueba'] for item in data]
            escalares = [self.convertir_a_numero(item['escalar']) for item in data]
            subpruebas_nombres = self.obtener_nombres_subpruebas(subpruebas_ids)
            # Depuración: Imprimir subpruebas y escalares obtenidos
            print("Subpruebas IDs obtenidas:", subpruebas_ids)
            print("Subpruebas nombres obtenidos:", subpruebas_nombres)
            print("Escalares obtenidos:", escalares)
            return self.clasificar_por_categoria(subpruebas_nombres, escalares)
        return {}

    def obtener_id_prueba(self, nombre_prueba):
        # Obtener el ID de la prueba desde el backend
        url = 'http://localhost:5000/pruebas'
        response = requests.get(url)
        if response.status_code == 200:
            pruebas = response.json()
            for prueba in pruebas:
                if prueba['nombre'].lower() == nombre_prueba.lower():
                    return prueba['id']
        return None

    def obtener_nombres_subpruebas(self, subpruebas_ids):
        # Obtener los nombres de las subpruebas desde el backend
        url = 'http://localhost:5000/subpruebas'
        response = requests.get(url)
        if response.status_code == 200:
            subpruebas = response.json()
            nombres = []
            for id_subprueba in subpruebas_ids:
                for subprueba in subpruebas:
                    if subprueba['id'] == id_subprueba:
                        nombres.append(subprueba['nombre'])
                        break
            return nombres
        return []

    def clasificar_por_categoria(self, subpruebas, escalares):
        categorias = {
            "Comprensión Verbal": ["SEMEJANZAS", "VOCABULARIO", "INFORMACIÓN", "COMPRENSIÓN"],
            "Razonamiento Perceptual": ["DISEÑO CON CUBOS", "MATRICES", "ROMPECABEZAS VISUAL", "PESO FIGURADO", "FIGURAS INCOMPLETAS"],
            "Memoria de Trabajo": ["RETENCIÓN DE DÍGITOS", "ARITMÉTICA", "SUCESIÓN DE NÚMEROS Y LETRAS"],
            "Velocidad de Procesamiento": ["BÚSQUEDA DE SÍMBOLOS", "CLAVES", "CANCELACIÓN"]
        }

        clasificacion = {
            "Comprensión Verbal": ([], []),
            "Razonamiento Perceptual": ([], []),
            "Memoria de Trabajo": ([], []),
            "Velocidad de Procesamiento": ([], [])
        }

        for subprueba, escalar in zip(subpruebas, escalares):
            subprueba_normalizada = self.normalizar_texto(subprueba)
            print(f"Subprueba normalizada: {subprueba_normalizada}")  # Depuración
            for categoria, subpruebas_categoria in categorias.items():
                if subprueba in subpruebas_categoria:
                    clasificacion[categoria][0].append(subprueba)
                    clasificacion[categoria][1].append(escalar)
                    break

        # Depuración: Imprimir categorías y sus subpruebas
        for categoria, (subpruebas, escalares) in clasificacion.items():
            print(f"Categoría: {categoria}")
            print(f"  Subpruebas: {subpruebas}")
            print(f"  Escalares: {escalares}")

        return clasificacion

    def normalizar_texto(self, texto):
        # Normalizar texto para eliminar acentos y convertir a mayúsculas
        texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')
        return texto.upper()

    def obtener_iniciales(self, texto):
        # Obtener las iniciales de las palabras en el texto
        return ''.join([palabra[0] for palabra in texto.split()]).upper()

    def convertir_a_numero(self, valor):
        try:
            if isinstance(valor, str) and '.' in valor:
                return float(valor)
            else:
                return int(valor)
        except ValueError:
            return 0  # Valor por defecto en caso de error de conversión

if __name__ == "__main__":
    app = QApplication([])
    paciente = {'codigo_hc': 1, 'nombre': 'Camilo Velasquez'}
    window = VisualizacionWindow(paciente)
    window.show()
    app.exec_()