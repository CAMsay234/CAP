import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QScrollArea, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import requests  # Importar el módulo para trabajar con bases de datos SQLite
import threading

class PruebaLenguajeWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()
        self.paciente_seleccionado = paciente_seleccionado
        # Configurar la ventana
        self.setWindowTitle("Prueba lenguaje")
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
        self.title = QLabel("LENGUAJE")
        self.title.setFont(QFont('Arial', 18, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        header_background_layout.addWidget(self.title, alignment=Qt.AlignCenter)

        # Campo de código
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

        # Tabla de pruebas
        self.add_table("PRUEBAS", ["Fluidez verbal semántica", "Fluidez verbal fonológica", "Token test", "Vocabulario", "Comprensión", "Mecánica de la escritura/5", "Escritura seriada/47", "Otra prueba"], main_layout)

        # Sección de comentarios clínicos con celdas para cada comentario
        comentarios_clinicos = [
            "Fonológico: (evaluación de la producción y comprensión de sonidos del lenguaje: fonemas)", 
            "Morfológico (Unidades con significado compuesta por uno o varios fonemas)",
            "Sintaxis (Se refiere a la organización adecuada de las palabras dentro de la oración)",
            "Semántica (se refiere al significado de las palabras; alteraciones en el contenido del lenguaje)",
            "Pragmática  (se refiere a la utilización adecuada del lenguaje dentro de un contexto social)"
        ]
        self.add_comment_section("COMENTARIO CLÍNICO", comentarios_clinicos, main_layout)

        # Sección de "Conclusiones Generales" con un solo cuadro grande
        self.add_conclusion_section("CONCLUSIONES GENERALES", main_layout)

        # Configurar el scroll y añadir el widget principal
        scroll.setWidget(scroll_widget)
        self.setCentralWidget(scroll)

    def abrir_evaluacion_neuropsicologica(self):
        """Función para abrir la ventana de Evaluación Neuropsicológica."""
        from gui.evaluacion_neuropsicologica import EvaluacionNeuropsicologicaWindow  # Importar la nueva ventana de registro de pacientes
        self.evaluacion_neuropsicologica_window = EvaluacionNeuropsicologicaWindow(self.paciente_seleccionado)  # Crear la ventana de registrar paciente
        self.evaluacion_neuropsicologica_window.show()  # Mostrar la ventana de registrar paciente
        self.close()  # Cerrar la ventana actual

    def add_table(self, title, tests, layout):
        """Función para agregar una tabla con los datos de las pruebas."""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setStyleSheet("color: black; background-color: #B0C4DE; padding: 10px;")
        layout.addWidget(title_label)

        self.table_layout = QGridLayout()  # Inicializar self.table_layout
        headers = ["PRUEBAS", "PUNTAJE", "MEDIA", "DS", "INTERPRETACIÓN"]

        # Agregar encabezados a la tabla
        for col, header in enumerate(headers):
            header_label = QLabel(header)
            header_label.setFont(QFont('Arial', 14, QFont.Bold))
            header_label.setStyleSheet("color: white; background-color: #4A90E2; padding: 10px; border-radius: 5px;")
            header_label.setAlignment(Qt.AlignCenter)
            self.table_layout.addWidget(header_label, 0, col)

        # Agregar filas de pruebas
        for row, test in enumerate(tests, start=1):
            if test == "Otra prueba":
                # Campo de entrada para "Otra prueba"
                test_label = QLineEdit()
                test_label.setPlaceholderText("Ingrese el nombre de la prueba")
                test_label.setAlignment(Qt.AlignCenter)
                test_label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")
                self.table_layout.addWidget(test_label, row, 0)
            else:
                # Nombre de la prueba
                test_label = QLabel(test)
                test_label.setProperty("pruebas", True)
                test_label.setAlignment(Qt.AlignCenter)
                test_label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")
                self.table_layout.addWidget(test_label, row, 0)

            # Campos de entrada para Puntaje, Media, DS, Interpretación
            for col in range(1, 5):
                input_field = QLineEdit()
                input_field.setFixedHeight(35)
                input_field.setStyleSheet("border: 1px solid black;")  # Añadir borde
                self.table_layout.addWidget(input_field, row, col)

        layout.addLayout(self.table_layout)

    def add_comment_section(self, title, comments, layout):
            """Añadir sección de comentarios clínicos con múltiples líneas"""
            title_label = QLabel(title)
            title_label.setFont(QFont('Arial', 14, QFont.Bold))
            title_label.setStyleSheet("background-color: #4A90E2; color: white; padding: 5px; border-radius: 5px;")
            layout.addWidget(title_label)

            self.comment_layout = QGridLayout()
            self.comment_fields = {}  # Diccionario para almacenar los QTextEdit asociados a cada comentario

            for i, comment in enumerate(comments):
                label = QLabel(comment)
                label.setFont(QFont('Arial', 14))
                label.setProperty("comentarios", True)
                label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")
                label.setWordWrap(True)
                self.comment_layout.addWidget(label, i, 0)

                # Añadir campo de texto asociado al comentario
                input_field = QTextEdit()
                input_field.setFont(QFont('Arial', 12))
                input_field.setStyleSheet("border: 1px solid black;")
                input_field.setFixedHeight(150)
                self.comment_layout.addWidget(input_field, i, 1)

                # Guardar el campo de texto en el diccionario usando el comentario como clave
                self.comment_fields[comment] = input_field

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
                # Obtener el ID de la prueba de lenguaje
                response = requests.get('http://localhost:5000/pruebas')
                if response.status_code == 200:
                    pruebas = response.json()
                    self.prueba_id = next((p['id'] for p in pruebas if p['nombre'].lower() == "lenguaje"), None)
                    if self.prueba_id is None:
                        print("Prueba de lenguaje no encontrada.")
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
                else:
                    print(f"Error al obtener las subpruebas: {response.status_code}")
                    subpruebas_map = {}

                # Obtener las evaluaciones del paciente para esta prueba
                url = f"http://localhost:5000/evaluaciones/{self.paciente_seleccionado['codigo_hc']}/{self.prueba_id}"
                response = requests.get(url)
                if response.status_code == 200:
                    evaluaciones = response.json()
                    print(f"Evaluaciones obtenidas: {evaluaciones}")

                    # Llenar los campos de la tabla con los datos correspondientes
                    for evaluacion in evaluaciones:
                        subprueba_nombre = next((nombre for nombre, id in subpruebas_map.items() if id == evaluacion['id_subprueba']), "Desconocido")

                        # Asignar datos a las subpruebas normales
                        for row in range(1, self.table_layout.rowCount()):
                            widget = self.table_layout.itemAtPosition(row, 0).widget()
                            if isinstance(widget, QLabel):
                                nombre_subprueba = widget.text().strip()
                                if nombre_subprueba == subprueba_nombre:
                                    self.table_layout.itemAtPosition(row, 1).widget().setText(str(evaluacion['puntaje']))
                                    self.table_layout.itemAtPosition(row, 2).widget().setText(str(evaluacion['media']))
                                    self.table_layout.itemAtPosition(row, 3).widget().setText(str(evaluacion['desviacion_estandar']))
                                    self.table_layout.itemAtPosition(row, 4).widget().setText(evaluacion['interpretacion'])
                                    break

                        if subprueba_nombre == "Otra prueba":
                            otra_prueba_widget = self.table_layout.itemAtPosition(8, 0).widget()
                            otra_prueba_widget.setText("Otra prueba")
                            self.table_layout.itemAtPosition(8, 1).widget().setText(str(evaluacion['puntaje']))
                            self.table_layout.itemAtPosition(8, 2).widget().setText(str(evaluacion['media']))
                            self.table_layout.itemAtPosition(8, 3).widget().setText(str(evaluacion['desviacion_estandar']))
                            self.table_layout.itemAtPosition(8, 4).widget().setText(evaluacion['interpretacion'])

                    print("Datos cargados exitosamente.")
                elif response.status_code == 404:
                    print("No se encontraron evaluaciones para este paciente.")
                else:
                    print(f"Error al obtener las evaluaciones: {response.status_code}")

                # Obtener los comentarios del paciente para esta prueba
                url = f"http://localhost:5000/comentarios/{self.paciente_seleccionado['codigo_hc']}/{self.prueba_id}"
                response = requests.get(url)
                if response.status_code == 200:
                    comentarios = response.json()
                    print(f"Comentarios obtenidos: {comentarios}")

                    # Llenar los campos de comentarios con los datos obtenidos
                    for comentario in comentarios:
                        if comentario['tipo_comentario'] == "Conclusión":
                            self.conclusion_text_edit.setPlainText(comentario['comentario'])
                        elif comentario['tipo_comentario'] in self.comment_fields:
                            self.comment_fields[comentario['tipo_comentario']].setPlainText(comentario['comentario'])
                else:
                    print(f"Error al obtener los comentarios: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"Error de conexión: {str(e)}")

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
    
            # Verificar si el comentario ya existe
            check_url = f"http://localhost:5000/comentarios/{self.paciente_seleccionado['codigo_hc']}/{prueba_id}/{comment_label}"
            response = requests.get(check_url)
            
            if response.status_code == 404:
                # No existe, realizar un INSERT
                response = requests.post('http://localhost:5000/comentarios', json=data)
                if response.status_code == 201:
                    print(f"Comentario '{comment_label}' guardado exitosamente.")
                else:
                    print(f"Error al guardar el comentario '{comment_label}': {response.status_code} - {response.text}")
            elif response.status_code == 200:
                # Ya existe, realizar un UPDATE
                response = requests.put(check_url, json=data)
                if response.status_code == 200:
                    print(f"Comentario '{comment_label}' actualizado exitosamente.")
                else:
                    print(f"Error al actualizar el comentario '{comment_label}': {response.status_code} - {response.text}")
            else:
                print(f"Error al verificar el comentario '{comment_label}': {response.status_code} - {response.text}")
    
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
    
        # Verificar si la conclusión ya existe
        check_url = f"http://localhost:5000/comentarios/{self.paciente_seleccionado['codigo_hc']}/{prueba_id}/Conclusión"
        response = requests.get(check_url)
        
        if response.status_code == 404:
            # No existe, realizar un INSERT
            response = requests.post('http://localhost:5000/comentarios', json=data)
            if response.status_code == 201:
                print("Conclusión guardada exitosamente.")
            else:
                print(f"Error al guardar la conclusión: {response.status_code} - {response.text}")
        elif response.status_code == 200:
            # Ya existe, realizar un UPDATE
            response = requests.put(check_url, json=data)
            if response.status_code == 200:
                print("Conclusión actualizada exitosamente.")
            else:
                print(f"Error al actualizar la conclusión: {response.status_code} - {response.text}")
        else:
            print(f"Error al verificar la conclusión: {response.status_code} - {response.text}")    
            
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
    window = PruebaLenguajeWindow()
    window.show()
    sys.exit(app.exec_())