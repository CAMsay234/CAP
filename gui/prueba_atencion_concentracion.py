import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QScrollArea, QTextEdit, QPushButton
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class PruebaAtencionConcentracionWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()
        self.paciente_seleccionado = paciente_seleccionado
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
        self.boton_guardar.clicked.connect(self.guardar_todo)  # Conectar el botón para guardar
        header_background_layout.addWidget(self.boton_guardar, alignment=Qt.AlignRight)

        # Tabla de pruebas
        self.table_layout = QGridLayout()
        headers = ["PRUEBAS", "PUNTAJE", "MEDIA", "DS", "INTERPRETACIÓN"]
        tests = [
            "Dígitos", "CPT Auditivo Aciertos", "CPT Auditivo Omisiones", "CPT Visual Aciertos",
            "CPT Visual Omisiones", "Control Mental", "Claves (WISC-III)", "Otra Prueba"
        ]

        # Agregar encabezados a la tabla
        for col, header in enumerate(headers):
            header_label = QLabel(header)
            header_label.setFont(QFont('Arial', 14, QFont.Bold))
            header_label.setStyleSheet("color: white; background-color: #4A90E2; padding: 10px;")
            header_label.setAlignment(Qt.AlignCenter)
            self.table_layout.addWidget(header_label, 0, col)

        # Agregar filas de pruebas
        for row, test in enumerate(tests, start=1):
            # Nombre de la prueba
            test_label = QLabel(test)
            test_label.setAlignment(Qt.AlignCenter)
            test_label.setProperty("pruebas", True)
            test_label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")
            test_label.setMinimumWidth(500)
            self.table_layout.addWidget(test_label, row, 0)

            # Campos de entrada para Puntaje, Media, DS, Interpretación
            for col in range(1, 5):
                input_field = QLineEdit()
                input_field.setStyleSheet("border: 1px solid black;")
                input_field.setFixedHeight(35)
                self.table_layout.addWidget(input_field, row, col)

        main_layout.addLayout(self.table_layout)

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
        self.add_conclusion_section("CONCLUSIONES GENERALES", main_layout)

        # Configurar el scroll y añadir el widget principal
        scroll.setWidget(scroll_widget)
        self.setCentralWidget(scroll)

    def add_section(self, title, fields, layout):
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

        layout.addLayout(section_layout)

    def add_comment_section(self, title, comments, layout):
        """Añadir sección de comentarios clínicos con múltiples líneas"""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 14, QFont.Bold))  # Letra más pequeña
        title_label.setStyleSheet("background-color: #4A90E2; color: white; padding: 5px; border-radius: 5px;")  # Fondo azul claro y letra blanca
        layout.addWidget(title_label)

        self.comment_layout = QGridLayout()
        for i, comment in enumerate(comments):
            label = QLabel(comment)
            label.setFont(QFont('Arial', 14))
            label.setProperty("comentarios", True)  # Letra más pequeña
            label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")  # Letra negra y fondo gris
            label.setWordWrap(True)  # Asegurar que el texto se envuelva
            self.comment_layout.addWidget(label, i, 0)

            # Añadir campo de texto asociado al comentario
            input_field = QTextEdit()
            input_field.setFont(QFont('Arial', 12))
            input_field.setStyleSheet("border: 1px solid black;")  # Añadir borde a las casillas de comentarios
            input_field.setFixedHeight(150)  # Ajustar altura fija
            self.comment_layout.addWidget(input_field, i, 1)

        layout.addLayout(self.comment_layout)

    def add_conclusion_section(self, title, layout):
        """Añadir sección de conclusiones generales"""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        title_label.setStyleSheet("background-color: #4A90E2; color: white; padding: 5px; border-radius: 5px;")
        layout.addWidget(title_label)

        self.conclusion_text_edit = QTextEdit()
        self.conclusion_text_edit.setFont(QFont('Arial', 12))
        self.conclusion_text_edit.setStyleSheet("border: 1px solid black;")
        self.conclusion_text_edit.setFixedHeight(150)  # Ajustar altura fija
        layout.addWidget(self.conclusion_text_edit)

    def abrir_evaluacion_neuropsicologica(self):
        """Función para abrir la ventana de Evaluación Neuropsicológica."""
        if hasattr(self, 'paciente_seleccionado'):
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

        # Recorrer cada fila de tests y obtener sus valores
        for row in range(1, self.table_layout.rowCount()):
            test_nombre = self.table_layout.itemAtPosition(row, 0).widget().text()
            puntaje = self.table_layout.itemAtPosition(row, 1).widget().text().strip()
            media = self.table_layout.itemAtPosition(row, 2).widget().text().strip()
            ds = self.table_layout.itemAtPosition(row, 3).widget().text().strip()
            interpretacion = self.table_layout.itemAtPosition(row, 4).widget().text().strip()

            # Verificar que todos los campos estén completos
            if not all([puntaje, media, ds, interpretacion]):
                print(f"Faltan datos para la subprueba '{test_nombre}'.")
                continue

            # Obtener el ID de la subprueba desde la API usando el ID de la prueba
            response = requests.get(f'http://localhost:5000/subpruebas')
            if response.status_code != 200:
                print(f"Error al obtener las subpruebas para la prueba '{test_nombre}'.")
                continue

            subpruebas = response.json()
            subprueba_id = next((sp['id'] for sp in subpruebas if sp['nombre'].lower() == test_nombre.lower() and sp['id_prueba'] == prueba_id), None)
            if subprueba_id is None:
                print(f"Subprueba '{test_nombre}' no encontrada en la base de datos.")
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
                    print(f"Resultados guardados exitosamente para la subprueba '{test_nombre}'.")
                else:
                    print(f"Error al guardar los resultados para la subprueba '{test_nombre}': {response.status_code} - {response.text}")
            elif response.status_code == 200:
                # Ya existe, realizar un UPDATE
                response = requests.put(check_url, json=data)
                if response.status_code == 200:
                    print(f"Resultados actualizados exitosamente para la subprueba '{test_nombre}'.")
                else:
                    print(f"Error al actualizar los resultados para la subprueba '{test_nombre}': {response.status_code} - {response.text}")
            else:
                print(f"Error al verificar la evaluación para la subprueba '{test_nombre}': {response.status_code} - {response.text}")



    def guardar_comentarios(self):
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
            print("Prueba no encontrada en la base de datos.")
            return

        # Recorrer cada comentario y obtener sus valores
        for i in range(self.comment_layout.rowCount()):
            comment_label = self.comment_layout.itemAtPosition(i, 0).widget().text()
            comment_text = self.comment_layout.itemAtPosition(i, 1).widget().toPlainText()

            # Guardar los comentarios en la base de datos
            data = {
                "codigo_hc": self.paciente_seleccionado['codigo_hc'],  # Usar el código del paciente seleccionado
                "id_prueba": prueba_id,
                "tipo_comentario": comment_label,
                "comentario": comment_text
            }
            response = requests.post('http://localhost:5000/comentarios', json=data)
            if response.status_code != 201:
                print(f"Error al guardar el comentario '{comment_label}'")

        print("Comentarios guardados exitosamente")

    def guardar_conclusion(self):
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
            print("Prueba no encontrada en la base de datos.")
            return

        # Guardar la conclusión como un comentario adicional
        conclusion_text = self.conclusion_text_edit.toPlainText()
        data = {
            "codigo_hc": self.paciente_seleccionado['codigo_hc'],
            "id_prueba": prueba_id,
            "tipo_comentario": "Conclusión",
            "comentario": conclusion_text
        }
        response = requests.post('http://localhost:5000/comentarios', json=data)
        if response.status_code != 201:
            print("Error al guardar la conclusión")

        print("Conclusión guardada exitosamente")

    def guardar_todo(self):
        self.guardar_prueba()
        self.guardar_comentarios()
        self.guardar_conclusion()

# Función para ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    paciente_seleccionado = {
        'nombre': 'Juan Pérez',
        'codigo_hc': '12345'
    }
    window = PruebaAtencionConcentracionWindow(paciente_seleccionado)
    window.show()
    sys.exit(app.exec_())