from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QMessageBox
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
        self.setStyleSheet("background-color: #005BBB;")  # Fondo azul

        # Crear widget principal y layout
        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        main_widget.setStyleSheet("background-color: #005BBB;")  # Fondo azul
        self.setCentralWidget(main_widget)

        # Mostrar logo y título
        self.add_header(main_layout)

        # Añadir gráficos
        self.add_graph(main_layout)
        self.add_graph_compuesto(main_layout)

        # Establecer un tamaño mínimo para la ventana
        self.setMinimumSize(800, 600)

        # Mostrar la ventana
        self.show()

    def add_header(self, layout):
        # Crear un layout horizontal para el header
        header_layout = QHBoxLayout()

        # Añadir logo
        logo_label = QLabel(self)
        logo_pixmap = QPixmap('gui/src/upb.png').scaled(100, 100, Qt.KeepAspectRatio)
        logo_label.setPixmap(logo_pixmap)
        header_layout.addWidget(logo_label, alignment=Qt.AlignLeft)

        # Añadir título
        title_label = QLabel("Capacidad Intelectual", self)
        title_label.setFont(QFont('Arial', 24))
        title_label.setStyleSheet("color: white;")  # Texto blanco
        header_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Añadir botón "Volver"
        self.boton_volver = QPushButton("VOLVER")
        self.boton_volver.setStyleSheet("""
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
        """)
        self.boton_volver.clicked.connect(self.abrir_ventana_anterior)
        header_layout.addWidget(self.boton_volver, alignment=Qt.AlignRight)

        # Añadir el header layout al layout principal
        layout.addLayout(header_layout)

    def add_graph(self, layout):
        # Cambiar el tamaño de la figura
        fig, ax = plt.subplots(figsize=(10, 5))  # Tamaño ajustado
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        # Obtener subpruebas y escalares
        categorias = self.obtener_puntuaciones()

        if not categorias:
            self.mostrar_mensaje("Advertencia", "No hay datos disponibles para la prueba de capacidad intelectual.")
            return

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

    def add_graph_compuesto(self, layout):
        # Obtener datos de la tabla conversiones
        conversiones = self.obtener_conversiones()

        if not conversiones:
            self.mostrar_mensaje("Advertencia", "No hay datos disponibles para las conversiones.")
            return

        # Clasificar las conversiones por categoría compuesta
        conversiones_clasificadas = self.clasificar_por_categoria_compuesta(conversiones)

        # Crear el gráfico compuesto y añadirlo al layout
        canvas_compuesto = self.crear_grafico_compuesto(conversiones_clasificadas)
        layout.addWidget(canvas_compuesto)

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

    def obtener_conversiones(self):
        # Obtener conversiones desde el backend
        url = f'http://localhost:5000/conversiones/{self.paciente_seleccionado["codigo_hc"]}'
        response = requests.get(url)

        if response.status_code == 200:
            try:
                data = response.json()  # Ahora `data` es una lista de conversiones
                # Depuración: Imprimir los datos obtenidos
                print("Datos obtenidos de la API:")
                for item in data:
                    print(item)

                # Extraer las subpruebas y sus respectivas puntuaciones compuestas
                conversiones = {
                    item['id_subprueba']: item['puntuacion_compuesta']
                    for item in data if 'puntuacion_compuesta' in item
                }

                # Imprimir los IDs y las puntuaciones compuestas obtenidas
                print("Conversiones obtenidas:", conversiones)

                # Obtener los nombres de las subpruebas
                subpruebas_nombres = self.obtener_nombres_subpruebas(list(conversiones.keys()))
                conversiones_nombres = {
                    subpruebas_nombres[i]: conversiones[subprueba_id]
                    for i, subprueba_id in enumerate(conversiones.keys())
                }

                # Imprimir los nombres de las subpruebas y sus puntuaciones compuestas
                print("Nombres de subpruebas y puntuaciones compuestas:", conversiones_nombres)

                return conversiones_nombres
            except ValueError:
                print("Error al parsear la respuesta JSON")
                return {}
        else:
            print(f"Error en la solicitud: {response.status_code}")
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
            "Velocidad de Procesamiento": ([], []),
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

    def clasificar_por_categoria_compuesta(self, conversiones):
        # Inicializar las categorías con sus siglas
        categorias = {
            "ICV": 0.0,  # Comprensión Verbal
            "IRP": 0.0,  # Razonamiento Perceptual
            "IMT": 0.0,  # Memoria de Trabajo
            "IVP": 0.0,  # Velocidad de Procesamiento
            "CIT": 0.0   # Capacidad Intelectual Total
        }

        # Mapear las subpruebas a las categorías correctas
        mapeo_subpruebas = {
            "COMPRENSIÓN VERBAL": "ICV",
            "RAZONAMIENTO PERCEPTUAL": "IRP",
            "MEMORIA DE TRABAJO": "IMT",
            "VELOCIDAD DE PROCESAMIENTO": "IVP",
            "TOTAL": "CIT"
        }

        # Asignar las puntuaciones compuestas a las categorías correspondientes
        for subprueba, puntuacion in conversiones.items():
            categoria = mapeo_subpruebas.get(subprueba)  # Buscar la categoría correspondiente
            if categoria:
                categorias[categoria] = float(puntuacion)

        # Depuración: Imprimir categorías y sus puntaciones
        for categoria, puntacion in categorias.items():
            print(f"Categoría: {categoria}")
            print(f"  Puntación: {puntacion}")

        return categorias

    def crear_grafico_compuesto(self, conversiones):
        # Extraer las categorías y puntuaciones compuestas
        categories = ["ICV", "IRP", "IMT", "IVP", "CIT"]
        scores = [conversiones.get(cat, 0.0) for cat in categories]  # Obtener el valor de cada categoría o 0.0 si está vacío

        # Crear la figura
        fig, ax = plt.subplots(figsize=(8, 6))
        canvas = FigureCanvas(fig)

        # Y-axis range (matching the example with values from 40 to 160)
        ax.set_yticks(range(40, 161, 5))
        ax.set_ylim(40, 160)

        # Plotting the scores for each category
        ax.plot(categories, scores, marker='o', color='gray', linewidth=2)

        # Drawing a horizontal line at 100 as reference
        ax.axhline(y=100, color='navy', linewidth=3)

        # Customizing the plot
        ax.set_title("Perfil de Puntuaciones Compuestas", fontsize=14)
        ax.set_xlabel("Escala", fontsize=12)
        ax.set_ylabel("Puntuación", fontsize=12)

        # Adding a grid with light lines for better readability
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)

        return canvas

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
        
    def abrir_ventana_anterior(self):
        if hasattr(self, 'paciente_seleccionado'):
            from gui.evaluacion_neuropsicologica import EvaluacionNeuropsicologicaWindow
            self.ventana_anterior = EvaluacionNeuropsicologicaWindow(self.paciente_seleccionado)
            self.ventana_anterior.show()
            self.close()

    def mostrar_mensaje(self, titulo, mensaje, icono=QMessageBox.Information):
        """Función para mostrar un mensaje al usuario."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.setIcon(icono)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

if __name__ == "__main__":
    app = QApplication([])
    paciente = {'codigo_hc': 1, 'nombre': 'Camilo Velasquez'}
    window = VisualizacionWindow(paciente)
    window.show()
    app.exec_()