import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QScrollArea, QPushButton, QTextEdit
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import sqlite3  # Importar el módulo para trabajar con bases de datos SQLite


class PruebaCapacidadIntelectualWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()
        self.paciente_seleccionado = paciente_seleccionado
        # Configurar la ventana
        self.setWindowTitle("Prueba capacidad intelectual")
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
        pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        header_background_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Título
        self.title = QLabel("CAPACIDAD INTELECTUAL")
        self.title.setFont(QFont('Arial', 18, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        header_background_layout.addWidget(self.title, alignment=Qt.AlignCenter)

        # Campo de código
        self.codigo_label = QLabel(f"Código:{self.paciente_seleccionado['codigo_hc']}")
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
        self.boton_guardar.clicked.connect(self.guardar_prueba)  # Conectar el botón para guardar
        header_background_layout.addWidget(self.boton_guardar, alignment=Qt.AlignRight)

        # Tabla de pruebas
        self.add_table("PRUEBAS", ["DISEÑO CON CUBOS", "SEMEJANZAS", "RETENCIÓN DE DÍGITOS", "MATRICES", "VOCABULARIO",
                                   "ARITMÉTICA", "BÚSQUEDA DE SÍMBOLOS", "ROMPECABEZAS VISUAL", "INFORMACIÓN", "CLAVES",
                                   "SUCESIÓN DE NÚMEROS Y LETRAS", "PESO FIGURADO", "COMPRENSIÓN", "CANCELACIÓN", "FIGURAS INCOMPLETAS"], main_layout)

        # Tabla de conversión de puntuaciones
        self.add_conversion("CONVERSIÓN DE LA SUMA DE PUNTUACIONES ESCALARES A PUNTUACIONES COMPUESTAS", ["COMPRENSIÓN VERBAL", "RAZONAMIENTO PERCEPTUAL", "MEMORIA DE TRABAJO", "VELOCIDAD DE PROCESAMIENTO"], main_layout)
        
        # Configurar el scroll y añadir el widget principal
        scroll.setWidget(scroll_widget)
        self.setCentralWidget(scroll)

    def abrir_evaluacion_neuropsicologica(self):
        if hasattr(self, 'paciente_seleccionado'):
            """Función para abrir la ventana de Evaluación Neuropsicológica."""
            from evaluacion_neuropsicologica import EvaluacionNeuropsicologicaWindow  # Importar la nueva ventana de registro de pacientes
            self.evaluacion_neuropsicologica_window = EvaluacionNeuropsicologicaWindow(self.paciente_seleccionado)  # Crear la ventana de registrar paciente
            self.evaluacion_neuropsicologica_window.show()  # Mostrar la ventana de registrar paciente
            self.close()  # Cerrar la ventana actual

    def guardar_prueba(self):
        # Obtener el nombre de la prueba desde el título de la ventana
        prueba_nombre = self.windowTitle().replace("Prueba ", "")

        # Obtener el ID de la prueba desde la API
        response = requests.get('http://localhost:5000/pruebas')
        if response.status_code != 200:
            print("Error al obtener las pruebas")
            return

        pruebas = response.json()
        prueba_id = next((p['id'] for p in pruebas if p['nombre'].lower() == prueba_nombre.lower()), None)
        if prueba_id is None:
            print(f"Prueba '{prueba_nombre}' no encontrada en la base de datos.")
            return

        # Recorrer cada fila de subpruebas y obtener sus valores
        for row in range(1, self.table_layout.rowCount()):
            subprueba_nombre = self.table_layout.itemAtPosition(row, 0).widget().text()
            puntaje = self.table_layout.itemAtPosition(row, 1).widget().text().strip()
            media = self.table_layout.itemAtPosition(row, 2).widget().text().strip()
            ds = self.table_layout.itemAtPosition(row, 3).widget().text().strip()
            interpretacion = self.table_layout.itemAtPosition(row, 4).widget().text().strip()

            # Verificar que todos los campos estén completos
            if not all([puntaje, media, ds, interpretacion]):
                print(f"Faltan datos para la subprueba '{subprueba_nombre}'.")
                continue

            # Obtener el ID de la subprueba desde la API usando el ID de la prueba
            response = requests.get(f'http://localhost:5000/subpruebas')
            if response.status_code != 200:
                print(f"Error al obtener las subpruebas para la prueba '{subprueba_nombre}'.")
                continue

            subpruebas = response.json()
            subprueba_id = next((sp['id'] for sp in subpruebas if sp['nombre'].lower() == subprueba_nombre.lower() and sp['id_prueba'] == prueba_id), None)
            if subprueba_id is None:
                print(f"Subprueba '{subprueba_nombre}' no encontrada en la base de datos.")
                continue

            # Verificar si ya existe una evaluación para esta combinación de valores
            check_url = f"http://localhost:5000/evaluaciones/{self.paciente_seleccionado['codigo_hc']}/{prueba_id}/{subprueba_id}"
            response = requests.get(check_url)

            data = {
                "codigo_hc": self.paciente_seleccionado['codigo_hc'],
                "id_prueba": prueba_id,
                "id_subprueba": subprueba_id,
                "puntaje": puntaje,
                "media": media,
                "desviacion_estandar": ds,
                "interpretacion": interpretacion
            }

            if response.status_code == 404:
                # No existe, realizar un INSERT
                response = requests.post('http://localhost:5000/evaluaciones', json=data)
                if response.status_code == 201:
                    print(f"Resultados guardados exitosamente para la subprueba '{subprueba_nombre}'.")
                else:
                    print(f"Error al guardar los resultados para la subprueba '{subprueba_nombre}': {response.status_code} - {response.text}")
            elif response.status_code == 200:
                # Ya existe, realizar un UPDATE
                response = requests.put(check_url, json=data)
                if response.status_code == 200:
                    print(f"Resultados actualizados exitosamente para la subprueba '{subprueba_nombre}'.")
                else:
                    print(f"Error al actualizar los resultados para la subprueba '{subprueba_nombre}': {response.status_code} - {response.text}")
            else:
                print(f"Error al verificar la evaluación para la subprueba '{subprueba_nombre}': {response.status_code} - {response.text}")

    def crear_rectangulos_puntuacion_escalar(self, fila):
        escalar_layout = QHBoxLayout()

        # Definir los patrones de colores para cada fila
        patrones = [
            [True, False, True, True],  # Fila 1
            [False, True, True, True],  # Fila 2
            [True, True, False, True],  # Fila 3
            [True, False, True, True],  # Fila 4
            [False, True, True, True],  # Fila 5
            [True, True, False, True],  # Fila 6
            [True, True, True, False],  # Fila 7
            [True, False, True, True],  # Fila 8
            [False, True, True, True],  # Fila 9
            [True, True, True, False],  # Fila 10
            [True, True, False, True],  # Fila 11
            [True, False, True, True],  # Fila 12
            [False, True, True, True],  # Fila 13
            [True, True, True, False],  # Fila 14
            [True, False, True, True]   # Fila 15
        ]

        # Obtener el patrón correspondiente para esta fila
        patron = patrones[fila % len(patrones)]

        for i, pintar in enumerate(patron):
            small_input = QLineEdit()
            small_input.setFixedSize(40, 35)  # Tamaño del recuadro
            small_input.setAlignment(Qt.AlignCenter)

            # Cambiar el color de fondo y habilitar o deshabilitar según el patrón
            if pintar:
                color_fondo = "#005BBB"  # Azul
                color_texto = "white"  # Texto blanco
                small_input.setReadOnly(True)  # Deshabilitar edición
            else:
                color_fondo = "#FFFFFF"  # Blanco
                color_texto = "black"  # Texto negro
                small_input.setReadOnly(False)  # Habilitar edición

            small_input.setStyleSheet(f"""
                QLineEdit {{
                    border: 1px solid black;
                    border-radius: 5px;
                    background-color: {color_fondo};
                    color: {color_texto};
                    font-weight: bold;
                }}
            """)
            escalar_layout.addWidget(small_input)

        return escalar_layout

    def add_table(self, title, tests, layout):
        """Función para agregar una tabla con los datos de las pruebas."""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setStyleSheet("color: black; background-color: #B0C4DE; padding: 10px;")
        layout.addWidget(title_label)

        table_layout = QGridLayout()
        headers = ["PRUEBAS", "PUNTUACIÓN NATURAL", "PUNTUACIÓN ESCALAR", "PUNTUACIÓN ESCALAR TOTAL"]

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
            test_label.setAlignment(Qt.AlignCenter)
            test_label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")
            table_layout.addWidget(test_label, row, 0)

            # Campo de PUNTUACIÓN NATURAL
            natural_input = QLineEdit()
            natural_input.setFixedSize(100, 35)
            natural_input.setAlignment(Qt.AlignCenter)
            natural_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid black;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)
            natural_layout = QHBoxLayout()
            natural_layout.addStretch()
            natural_layout.addWidget(natural_input)
            natural_layout.addStretch()
            table_layout.addLayout(natural_layout, row, 1)

            # PUNTUACIÓN ESCALAR - con 4 rectángulos pequeños
            escalar_layout = self.crear_rectangulos_puntuacion_escalar(row - 1)
            table_layout.addLayout(escalar_layout, row, 2)

            # Campo de PUNTUACIÓN ESCALAR TOTAL
            total_input = QLineEdit()
            total_input.setFixedSize(100, 35)
            total_input.setAlignment(Qt.AlignCenter)
            total_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid black;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)
            total_layout = QHBoxLayout()
            total_layout.addStretch()
            total_layout.addWidget(total_input)
            total_layout.addStretch()
            table_layout.addLayout(total_layout, row, 3)

        # Añadir el título "SUMA DE PUNTUACIONES ESCALARES"
        total_label = QLabel("SUMA DE PUNTUACIONES ESCALARES")
        total_label.setFont(QFont('Arial', 14, QFont.Bold))
        total_label.setStyleSheet("color: black; background-color: #B0C4DE; padding: 10px;")
        total_label.setAlignment(Qt.AlignCenter)
        table_layout.addWidget(total_label, len(tests) + 1, 0, 1, 4)

        # Subtítulos y recuadros de puntuación escalar adicionales
        total_escalar_layout = QHBoxLayout()
        subtitulos = ["VERBAL", "PERCEPTUAL", "MEMORIA", "VELOCIDAD"]

        for subtitulo in subtitulos:
            columna_layout = QVBoxLayout()
            columna_layout.setAlignment(Qt.AlignCenter)

            subtitulo_label = QLabel(subtitulo)
            subtitulo_label.setAlignment(Qt.AlignCenter)
            subtitulo_label.setProperty("subtitulo", True)
            subtitulo_label.setStyleSheet("color: black; padding: 2px;")

            total_escalar_input = QLineEdit()
            total_escalar_input.setFixedSize(40, 35)
            total_escalar_input.setAlignment(Qt.AlignCenter)
            total_escalar_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid black;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)

            columna_layout.addWidget(subtitulo_label)
            columna_layout.addWidget(total_escalar_input)
            total_escalar_layout.addLayout(columna_layout)

        total_escalar_layout.setSpacing(5)
        table_layout.addLayout(total_escalar_layout, len(tests) + 2, 2, alignment=Qt.AlignCenter)

        # Añadir subtítulo y recuadro adicional para CI TOTAL debajo de la columna "Puntuación Escalar Total"
        extra_total_layout = QVBoxLayout()
        extra_total_label = QLabel("CI TOTAL")
        extra_total_label.setAlignment(Qt.AlignCenter)
        extra_total_label.setProperty("subtitulo", True)
        extra_total_label.setStyleSheet("color: black; padding: 2px;")

        extra_total_input = QLineEdit()
        extra_total_input.setFixedSize(100, 35)
        extra_total_input.setAlignment(Qt.AlignCenter)
        extra_total_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid black;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        extra_total_layout.addWidget(extra_total_label)
        extra_total_layout.addWidget(extra_total_input)
        table_layout.addLayout(extra_total_layout, len(tests) + 2, 3, alignment=Qt.AlignCenter)

        # Añadir título "CONVERSIÓN DE LA SUMA DE PUNTUACIONES ESCALARES A PUNTUACIONES COMPUESTAS"
        total_label.setFont(QFont('Arial', 14, QFont.Bold))
        total_label.setStyleSheet("color: black; background-color: #B0C4DE; padding: 10px;")
        total_label.setAlignment(Qt.AlignCenter)
        table_layout.addWidget(total_label, len(tests) + 1, 0, 1, 4)
        layout.addLayout(table_layout)
    
    def add_conversion(self, title, tests, layout):
        """Función para agregar una tabla con las conversiones de las pruebas."""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: black; background-color: #B0C4DE; padding: 10px;")
        layout.addWidget(title_label)

        table_layout = QGridLayout()
        headers = ["ESCALA", "SUMA PUNTUACIONES ESCALARES", "PUNTUACIÓN COMPUESTA", 
                "RANGO PERCENTIL", "INTERVALO CONFIANZA"]

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
            test_label.setAlignment(Qt.AlignCenter)
            test_label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")
            table_layout.addWidget(test_label, row, 0)

            # Campos de entrada alineados al centro para cada columna
            for col in range(1, 5):
                input_field = QLineEdit()
                input_field.setFixedSize(100, 35)
                input_field.setAlignment(Qt.AlignCenter)
                input_field.setStyleSheet("""
                    QLineEdit {
                        border: 1px solid black;
                        border-radius: 5px;
                        padding: 5px;
                    }
                """)

                # Crear un layout horizontal para centrar el campo dentro de su celda
                cell_layout = QHBoxLayout()
                cell_layout.addStretch()  # Espacio a la izquierda
                cell_layout.addWidget(input_field)  # Campo de entrada
                cell_layout.addStretch()  # Espacio a la derecha

                table_layout.addLayout(cell_layout, row, col)

        layout.addLayout(table_layout)


# Función para ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    paciente = {'codigo_hc': 1, 'nombre': 'Camilo Velasquez'}
    window = PruebaCapacidadIntelectualWindow(paciente)
    window.show()
    sys.exit(app.exec_())