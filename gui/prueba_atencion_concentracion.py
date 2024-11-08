import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QScrollArea, QTextEdit, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import threading

class PruebaAtencionConcentracionWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()
        self.paciente_seleccionado = paciente_seleccionado
        self.prueba_id = None  # ID de la prueba de atención y concentración
        self.subpruebas_map = {}  # Diccionario para mapear nombres de subpruebas a sus IDs

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
        header_background_layout.addWidget(self.codigo_label, alignment=Qt.AlignRight)

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

        self.section_inputs = {}  # Inicializar el diccionario para todas las subpruebas y secciones

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
            if test == "Otra Prueba":
                # Campo de entrada para el nombre de la prueba
                test_label = QLineEdit()
                test_label.setPlaceholderText("Ingrese el nombre de la prueba")
                test_label.setAlignment(Qt.AlignCenter)
                test_label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")
                test_label.setMinimumWidth(500)
                self.table_layout.addWidget(test_label, row, 0)
                input_fields = [test_label]  # Incluir el campo de nombre para "Otra Prueba"
            else:
                # Nombre de la prueba
                test_label = QLabel(test)
                test_label.setAlignment(Qt.AlignCenter)
                test_label.setProperty("pruebas", True)
                test_label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")
                test_label.setMinimumWidth(500)
                self.table_layout.addWidget(test_label, row, 0)
                input_fields = []  # Lista para almacenar los campos de entrada de cada prueba

            # Campos de entrada para Puntaje, Media, DS, Interpretación
            for col in range(1, 5):
                input_field = QLineEdit()
                input_field.setStyleSheet("border: 1px solid black;")
                input_field.setFixedHeight(35)
                self.table_layout.addWidget(input_field, row, col)
                input_fields.append(input_field)

            # Agregar las referencias de los campos de entrada al diccionario section_inputs usando el nombre de la prueba
            self.section_inputs[test] = input_fields

        main_layout.addLayout(self.table_layout)

        # Sección de "Tachado de Cuadros"
        self.add_section("TACHADO DE CUADROS", ["Aciertos 48/", "Errores", "Tiempo Tachado de cuadros"], main_layout)

        # Sección de "Test de Rastreo de Caminos A."
        self.add_section("TEST DE RASTREOS DE CAMINOS A.", ["Tiempo Test de rastreo", "Curva de Memoria. Span"], main_layout)

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

        # Llamar a la función para cargar los datos del paciente
        self.cargar_datos_paciente()

            
    def add_section(self, title, fields, layout):
        """Añadir secciones con campos de entrada de texto y almacenar sus referencias."""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 14, QFont.Bold))
        title_label.setStyleSheet("background-color: #4A90E2; color: white; padding: 5px; border-radius: 5px;")
        layout.addWidget(title_label)

        section_layout = QGridLayout()

        # Crear un diccionario para almacenar los campos de entrada por nombre de subprueba
        self.section_inputs = self.section_inputs if hasattr(self, 'section_inputs') else {}

        for i, field in enumerate(fields):
            label = QLabel(field)
            label.setFont(QFont('Arial', 12))
            label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")
            label.setMinimumWidth(500)
            section_layout.addWidget(label, i, 0)

            # Añadir campos de entrada y guardar las referencias
            input_fields = []
            for col in range(1, 5):
                input_field = QLineEdit()
                input_field.setStyleSheet("border: 1px solid black;")
                input_field.setFixedHeight(35)
                section_layout.addWidget(input_field, i, col)
                input_fields.append(input_field)

            # Guardar las referencias en el diccionario usando el nombre del campo como clave
            self.section_inputs[field] = input_fields

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
    
    def cargar_datos_paciente(self):
        """Función para cargar los datos de las evaluaciones del paciente."""
        try:
            # Obtener el ID de la prueba de atención y concentración
            response = requests.get('http://localhost:5000/pruebas')
            if response.status_code == 200:
                pruebas = response.json()
                self.prueba_id = next((p['id'] for p in pruebas if p['nombre'].lower() == "atención y concentración"), None)
                if self.prueba_id is None:
                    print("Prueba de atención y concentración no encontrada.")
                    return
            else:
                print(f"Error al obtener las pruebas: {response.status_code}")
                return

            # Obtener todas las subpruebas para crear un mapeo basado en los nombres
            response = requests.get('http://localhost:5000/subpruebas')
            if response.status_code == 200:
                subpruebas = response.json()
                # Crear un mapeo de nombre de subprueba a ID
                subpruebas_map = {sp['nombre']: sp['id'] for sp in subpruebas}
                print("Contenido de subpruebas_map:", subpruebas_map)
            else:
                print(f"Error al obtener las subpruebas: {response.status_code}")
                subpruebas_map = {}

            # Obtener las evaluaciones del paciente para esta prueba
            url = f"http://localhost:5000/evaluaciones/{self.paciente_seleccionado['codigo_hc']}/{self.prueba_id}"
            response = requests.get(url)
            if response.status_code == 200:
                evaluaciones = response.json()
                print(f"Evaluaciones obtenidas: {evaluaciones}")

                # Llenar los campos de la tabla de subpruebas con los datos correspondientes
                for evaluacion in evaluaciones:
                    subprueba_nombre = next((nombre for nombre, id in subpruebas_map.items() if id == evaluacion['id_subprueba']), "Desconocido")

                    # Asignar datos a las subpruebas normales
                    if subprueba_nombre in self.section_inputs:
                        input_fields = self.section_inputs[subprueba_nombre]
                        if input_fields:
                            input_fields[0].setText(str(evaluacion['puntaje']))
                            input_fields[1].setText(str(evaluacion['media']))
                            input_fields[2].setText(str(evaluacion['desviacion_estandar']))
                            input_fields[3].setText(evaluacion['interpretacion'])

                # Cargar los datos específicos de las secciones adicionales
                secciones_adicionales = ["Aciertos 48/", "Errores", "Tiempo Tachado de cuadros", "Tiempo Test de rastreo", "Curva de Memoria verbal. Spán"]
                for seccion in secciones_adicionales:
                    if seccion in self.section_inputs:
                        # Buscar la evaluación correspondiente a la sección
                        evaluacion_seccion = next((e for e in evaluaciones if subpruebas_map.get(seccion) == e['id_subprueba']), None)
                        if evaluacion_seccion:
                            # Llenar los campos de entrada de la sección con los valores obtenidos
                            input_fields = self.section_inputs[seccion]
                            print(f"Cargando datos para la sección: {seccion}")
                            input_fields[0].setText(str(evaluacion_seccion['puntaje']))
                            input_fields[1].setText(str(evaluacion_seccion['media']))
                            input_fields[2].setText(str(evaluacion_seccion['desviacion_estandar']))
                            input_fields[3].setText(evaluacion_seccion['interpretacion'])
                        else:
                            print(f"No se encontró evaluación para la sección: {seccion}")

                print("Datos cargados exitosamente.")
            elif response.status_code == 404:
                print("No se encontraron evaluaciones para este paciente.")
            else:
                print(f"Error al obtener las evaluaciones: {response.status_code}")

            # Obtener los comentarios del paciente para esta prueba
            url = f"http://localhost:5000/comentarios/{self.paciente_seleccionado['codigo_hc']}/{self.prueba_id}/"
            response = requests.get(url)
            if response.status_code == 200:
                comentarios = response.json()
                print(f"Comentarios obtenidos: {comentarios}")

                # Llenar los campos de comentarios con los datos obtenidos
                for i, comentario in enumerate(comentarios):
                    if i < self.comment_layout.rowCount():
                        self.comment_layout.itemAtPosition(i, 1).widget().setPlainText(comentario['comentario'])
            else:
                print(f"Error al obtener los comentarios: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {str(e)}")

    def abrir_evaluacion_neuropsicologica(self):
        """Función para abrir la ventana de Evaluación Neuropsicológica."""
        from gui.evaluacion_neuropsicologica import EvaluacionNeuropsicologicaWindow  # Importar la nueva ventana de evaluación neuropsicológica
        self.evaluacion_neuropsicologica_window = EvaluacionNeuropsicologicaWindow(self.paciente_seleccionado)  # Crear la ventana de evaluación neuropsicológica
        self.evaluacion_neuropsicologica_window.show()  # Mostrar la ventana de evaluación neuropsicológica
        self.close()  # Cerrar la ventana actual

    def guardar_prueba(self):
        def procesar_subprueba(nombre_subprueba, input_fields):
            # Extraer los valores ingresados
            puntaje = input_fields[0].text().strip() or None
            media = input_fields[1].text().strip() or None
            ds = input_fields[2].text().strip() or None
            interpretacion = input_fields[3].text().strip()

            if not interpretacion:
                print(f"Faltan datos para la subprueba '{nombre_subprueba}'.")
                return

            # Verificar si la subprueba existe en la base de datos
            response = requests.get('http://localhost:5000/subpruebas')
            if response.status_code != 200:
                print(f"Error al obtener las subpruebas: {response.status_code}")
                return

            subpruebas = response.json()
            subprueba_id = next(
                (sp['id'] for sp in subpruebas if sp['nombre'].lower() == nombre_subprueba.lower()), None
            )

            # Si no existe, registrar la subprueba
            if subprueba_id is None:
                data = {"id_prueba": self.prueba_id, "nombre": nombre_subprueba}
                response = requests.post('http://localhost:5000/subpruebas', json=data)
                if response.status_code == 201:
                    subprueba_id = response.json().get('id')
                else:
                    print(f"Error al registrar la subprueba '{nombre_subprueba}': {response.text}")
                    return

            # Preparar los datos para guardar la evaluación
            data = {
                "codigo_hc": self.paciente_seleccionado['codigo_hc'],
                "id_prueba": self.prueba_id,
                "id_subprueba": subprueba_id,
                "puntaje": puntaje,
                "media": media,
                "desviacion_estandar": ds,
                "escalar": "N/A",
                "interpretacion": interpretacion
            }

            # Verificar si ya existe la evaluación
            url = f"http://localhost:5000/evaluaciones/{self.paciente_seleccionado['codigo_hc']}/{self.prueba_id}/{subprueba_id}"
            response = requests.get(url)

            if response.status_code == 404:
                # Insertar nueva evaluación
                response = requests.post('http://localhost:5000/evaluaciones', json=data)
                if response.status_code == 201:
                    print(f"Evaluación guardada para '{nombre_subprueba}'.")
                else:
                    print(f"Error al guardar la evaluación: {response.text}")
            elif response.status_code == 200:
                # Actualizar evaluación existente
                response = requests.put(url, json=data)
                if response.status_code == 200:
                    print(f"Evaluación actualizada para '{nombre_subprueba}'.")
                else:
                    print(f"Error al actualizar la evaluación: {response.text}")

        # Obtener el ID de la prueba
        response = requests.get('http://localhost:5000/pruebas')
        if response.status_code != 200:
            print("Error al obtener las pruebas.")
            return

        pruebas = response.json()
        self.prueba_id = next((p['id'] for p in pruebas if p['nombre'].lower() == "atención y concentración"), None)
        if self.prueba_id is None:
            print("Prueba no encontrada.")
            return

        # Procesar las subpruebas normales y las secciones adicionales
        threads = []
        
        # Procesar las secciones adicionales (Tachado de Cuadros, Rastreo de Caminos)
        for nombre, input_fields in self.section_inputs.items():
            thread = threading.Thread(target=procesar_subprueba, args=(nombre, input_fields))
            threads.append(thread)
            thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()

        print("Todas las subpruebas y secciones adicionales han sido guardadas.")

    def guardar_secciones(self):
        """Función para guardar los datos de las secciones adicionales."""
        def procesar_seccion(nombre_seccion, input_fields):
            # Extraer los valores ingresados
            puntaje = input_fields[0].text().strip() or None
            media = input_fields[1].text().strip() or None
            ds = input_fields[2].text().strip() or None
            interpretacion = input_fields[3].text().strip()

            if not interpretacion:
                print(f"Faltan datos para la sección '{nombre_seccion}'.")
                return

            # Verificar si la subprueba existe en la base de datos
            response = requests.get('http://localhost:5000/subpruebas')
            if response.status_code != 200:
                print(f"Error al obtener las subpruebas para '{nombre_seccion}': {response.status_code}")
                return

            subpruebas = response.json()
            subprueba_id = next(
                (sp['id'] for sp in subpruebas if sp['nombre'].lower() == nombre_seccion.lower()), None
            )

            # Si no existe, registrar la subprueba
            if subprueba_id is None:
                data = {"id_prueba": self.prueba_id, "nombre": nombre_seccion}
                response = requests.post('http://localhost:5000/subpruebas', json=data)
                if response.status_code == 201:
                    subprueba_id = response.json().get('id')
                else:
                    print(f"Error al registrar '{nombre_seccion}': {response.text}")
                    return

            # Preparar los datos para guardar la evaluación
            data = {
                "codigo_hc": self.paciente_seleccionado['codigo_hc'],
                "id_prueba": self.prueba_id,
                "id_subprueba": subprueba_id,
                "puntaje": puntaje,
                "media": media,
                "desviacion_estandar": ds,
                "escalar": "N/A",
                "interpretacion": interpretacion
            }

            # Verificar si ya existe la evaluación
            url = f"http://localhost:5000/evaluaciones/{self.paciente_seleccionado['codigo_hc']}/{self.prueba_id}/{subprueba_id}"
            response = requests.get(url)

            if response.status_code == 404:
                # Insertar nueva evaluación
                response = requests.post('http://localhost:5000/evaluaciones', json=data)
                if response.status_code == 201:
                    print(f"Evaluación guardada para '{nombre_seccion}'.")
                else:
                    print(f"Error al guardar la evaluación: {response.text}")
            elif response.status_code == 200:
                # Actualizar evaluación existente
                response = requests.put(url, json=data)
                if response.status_code == 200:
                    print(f"Evaluación actualizada para '{nombre_seccion}'.")
                else:
                    print(f"Error al actualizar la evaluación: {response.text}")

        # Crear y empezar hilos para cada sección
        threads = []
        for nombre, input_fields in self.section_inputs.items():
            thread = threading.Thread(target=procesar_seccion, args=(nombre, input_fields))
            threads.append(thread)
            thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()

        print("Todas las secciones adicionales han sido guardadas.")

    def guardar_comentarios(self):
        def procesar_comentario(i):
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
    
        # Crear y empezar hilos para cada comentario
        threads = []
        for i in range(self.comment_layout.rowCount()):
            thread = threading.Thread(target=procesar_comentario, args=(i,))
            threads.append(thread)
            thread.start()
    
        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()
    
        print("Comentarios guardados exitosamente")

    def guardar_conclusion(self):
        try:
            # Obtener el nombre de la prueba desde el título de la ventana
            prueba_nombre = self.windowTitle().replace("Prueba ", "")
            
            # Obtener el ID de la prueba desde la API
            response = requests.get('http://localhost:5000/pruebas')
            response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
            
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
            response.raise_for_status()  # Lanza una excepción si la solicitud no fue exitosa
            
            print("Conclusión guardada exitosamente")
        except requests.exceptions.RequestException as e:
            print(f"Error al guardar la conclusión: {e}")

    def mostrar_mensaje(self, titulo, mensaje, icono=QMessageBox.Information):
        """Función para mostrar un mensaje al usuario."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(titulo)
        msg_box.setText(mensaje)
        msg_box.setIcon(icono)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def guardar_todo(self):
        """Función para guardar todas las evaluaciones, comentarios y conclusiones."""
        try:
            # Intentar guardar todas las secciones
            self.guardar_prueba()
            self.guardar_secciones()
            self.guardar_comentarios()
            self.guardar_conclusion()

            # Mostrar mensaje de éxito si todo se guardó correctamente
            self.mostrar_mensaje("Éxito", "Datos guardados correctamente", QMessageBox.Information)
        except Exception as e:
            # Mostrar mensaje de error si hubo algún problema
            self.mostrar_mensaje("Error", f"Ocurrió un error al guardar los datos: {str(e)}", QMessageBox.Critical)


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