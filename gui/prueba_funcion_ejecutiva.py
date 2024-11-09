import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QScrollArea, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import requests
import threading

class PruebaFuncionEjecutivaWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()
        self.paciente_seleccionado = paciente_seleccionado
        # Configurar la ventana
        self.setWindowTitle("Prueba función ejecutiva")
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
        self.title = QLabel("FUNCIÓN EJECUTIVA")
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
        self.add_table("PRUEBAS", ["Stroop lectura", "Stroop color", "Stroop conflicto", "TMT B", "Errores", "Fluidez verbal fonológica", "Otra prueba"], main_layout)
        
        # Sección de comentarios clínicos con celdas para cada comentario
        comentarios_clinicos = [
            "Planeación", "Conceptualización", "Flexibilidad cognitiva", "Impulsividad y autocontrol"]
        self.add_comment_section("COMENTARIO CLÍNICO: Habilidades metacognitivas evaluadas", comentarios_clinicos, main_layout)

        # Sección de "Conclusiones Generales" con un solo cuadro grande
        self.add_conclusion_section("CONCLUSIONES GENERALES", main_layout)
        self.cargar_datos_subpruebas()
        self.cargar_datos_comentarios()
        # Configurar el scroll y añadir el widget principal
        scroll.setWidget(scroll_widget)
        self.setCentralWidget(scroll)

    def abrir_evaluacion_neuropsicologica(self):
        if hasattr(self, 'paciente_seleccionado'):
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

    def cargar_datos_subpruebas(self):
        def cargar_tabla(subpruebas, prueba_id, table_layout):
            for row, subprueba_nombre in enumerate(subpruebas, start=1):
                subprueba_nombre_completo = subprueba_nombre.lower()
                subprueba_id = subpruebas_dict.get(subprueba_nombre_completo)
                if subprueba_id:
                    # Obtener los datos de la evaluación para la subprueba
                    response = requests.get(f"http://localhost:5000/evaluaciones/{self.paciente_seleccionado['codigo_hc']}/{prueba_id}/{subprueba_id}")
                    if response.status_code == 200:
                        evaluacion = response.json()
                        # Ubicar los datos en los espacios correspondientes
                        table_layout.itemAtPosition(row, 1).widget().setText(evaluacion.get('puntaje', ''))
                        table_layout.itemAtPosition(row, 2).widget().setText(evaluacion.get('media', ''))
                        table_layout.itemAtPosition(row, 3).widget().setText(evaluacion.get('desviacion_estandar', ''))
                        table_layout.itemAtPosition(row, 4).widget().setText(evaluacion.get('interpretacion', ''))
                    else:
                        # Si no hay datos, dejar los espacios en blanco
                        table_layout.itemAtPosition(row, 1).widget().setText('')
                        table_layout.itemAtPosition(row, 2).widget().setText('')
                        table_layout.itemAtPosition(row, 3).widget().setText('')
                        table_layout.itemAtPosition(row, 4).widget().setText('')
                else:
                    # Si no hay subprueba, dejar los espacios en blanco
                    table_layout.itemAtPosition(row, 1).widget().setText('')
                    table_layout.itemAtPosition(row, 2).widget().setText('')
                    table_layout.itemAtPosition(row, 3).widget().setText('')
                    table_layout.itemAtPosition(row, 4).widget().setText('')

        # Obtener el ID de la prueba general "Función Ejecutiva" desde la API
        response = requests.get('http://localhost:5000/pruebas')
        if response.status_code != 200:
            print("Error al obtener las pruebas")
            return
        
        pruebas = response.json()
        prueba_id = next((p['id'] for p in pruebas if p['nombre'].lower() == "función ejecutiva"), None)
        if prueba_id is None:
            print(f"Prueba 'Función Ejecutiva' no encontrada en la base de datos.")
            return

        # Obtener todas las subpruebas asociadas a la prueba "Función Ejecutiva"
        response = requests.get('http://localhost:5000/subpruebas')
        if response.status_code != 200:
            print("Error al obtener las subpruebas")
            return
        
        subpruebas = response.json()
        subpruebas_dict = {sp['nombre'].lower(): sp['id'] for sp in subpruebas if sp['id_prueba'] == prueba_id}

        # Cargar los datos de la tabla
        cargar_tabla(
            ["Stroop lectura", "Stroop color", "Stroop conflicto", "TMT B", "Errores", "Fluidez verbal fonológica", "Otra prueba"],
            prueba_id,
            self.table_layout
        )

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
    
    def cargar_datos_comentarios(self):
        # Obtener el ID de la prueba general "Función Ejecutiva" desde la API
        response = requests.get('http://localhost:5000/pruebas')
        if response.status_code != 200:
            print("Error al obtener las pruebas")
            return
        
        pruebas = response.json()
        prueba_id = next((p['id'] for p in pruebas if p['nombre'].lower() == "función ejecutiva"), None)
        if prueba_id is None:
            print(f"Prueba 'Función Ejecutiva' no encontrada en la base de datos.")
            return

        # Obtener todos los comentarios asociados a la prueba "Función Ejecutiva"
        response = requests.get(f'http://localhost:5000/comentarios/{self.paciente_seleccionado["codigo_hc"]}/{prueba_id}')
        if response.status_code != 200:
            print("Error al obtener los comentarios")
            return
        
        comentarios = response.json()
        comentarios_dict = {c['tipo_comentario'].lower(): c['comentario'] for c in comentarios}

        # Cargar los datos de los comentarios clínicos
        for row, comentario_tipo in enumerate([
            "Planeación", "Conceptualización", "Flexibilidad cognitiva", "Impulsividad y autocontrol"
        ]):
            comentario_tipo_lower = comentario_tipo.lower()
            comentario_texto = comentarios_dict.get(comentario_tipo_lower, "")
            self.comment_layout.itemAtPosition(row, 1).widget().setPlainText(comentario_texto)

        # Cargar la conclusión
        conclusion_texto = comentarios_dict.get("conclusión", "")
        self.conclusion_text_edit.setPlainText(conclusion_texto)

    def guardar_prueba(self):
        prueba_nombre = self.windowTitle().replace("Prueba ", "")
        
        response = requests.get('http://localhost:5000/pruebas')
        if response.status_code != 200:
            print("Error al obtener las pruebas")
            return
        
        pruebas = response.json()
        prueba_id = next((p['id'] for p in pruebas if p['nombre'].lower() == prueba_nombre.lower()), None)
        if prueba_id is None:
            print(f"Prueba '{prueba_nombre}' no encontrada en la base de datos.")
            return
        
        for row in range(1, self.table_layout.rowCount()):
            widget = self.table_layout.itemAtPosition(row, 0).widget()
            if isinstance(widget, QLineEdit):
                subprueba_nombre = widget.text().strip()
            else:
                subprueba_nombre = widget.text().strip()
            
            puntaje_widget = self.table_layout.itemAtPosition(row, 1)
            media_widget = self.table_layout.itemAtPosition(row, 2)
            ds_widget = self.table_layout.itemAtPosition(row, 3)
            interpretacion_widget = self.table_layout.itemAtPosition(row, 4)
            
            puntaje = puntaje_widget.widget().text().strip() if puntaje_widget and puntaje_widget.widget() else None
            media = media_widget.widget().text().strip() if media_widget and media_widget.widget() else ""
            ds = ds_widget.widget().text().strip() if ds_widget and ds_widget.widget() else ""
            interpretacion = interpretacion_widget.widget().text().strip() if interpretacion_widget and interpretacion_widget.widget() else None
        
            if not puntaje or not interpretacion:
                print(f"Faltan datos obligatorios para la subprueba '{subprueba_nombre}'.")
                continue
        
            response = requests.get(f'http://localhost:5000/subpruebas')
            if response.status_code != 200:
                print(f"Error al obtener las subpruebas para la prueba '{subprueba_nombre}'.")
                continue
        
            subpruebas = response.json()
            subprueba_id = next((sp['id'] for sp in subpruebas if sp['nombre'].lower() == subprueba_nombre.lower() and sp['id_prueba'] == prueba_id), None)
        
            if subprueba_id is None:
                data_subprueba = {
                    "id_prueba": prueba_id,
                    "nombre": subprueba_nombre
                }
                response = requests.post('http://localhost:5000/subpruebas', json=data_subprueba)
                if response.status_code == 201:
                    response = requests.get(f'http://localhost:5000/subpruebas')
                    if response.status_code == 200:
                        subpruebas = response.json()
                        subprueba_id = next((sp['id'] for sp in subpruebas if sp['nombre'].lower() == subprueba_nombre.lower() and sp['id_prueba'] == prueba_id), None)
                        if subprueba_id:
                            print(f"Subprueba '{subprueba_nombre}' registrada exitosamente con ID {subprueba_id}.")
                        else:
                            print(f"Error: No se pudo encontrar el ID de la subprueba '{subprueba_nombre}' después de crearla.")
                            continue
                    else:
                        print(f"Error al obtener las subpruebas después de crear '{subprueba_nombre}': {response.status_code}")
                        continue
                else:
                    print(f"Error al registrar la subprueba '{subprueba_nombre}': {response.status_code} - {response.text}")
                    continue
        
            check_url = f"http://localhost:5000/evaluaciones/{self.paciente_seleccionado['codigo_hc']}/{prueba_id}/{subprueba_id}"
            response = requests.get(check_url)
        
            data = {
                "codigo_hc": self.paciente_seleccionado['codigo_hc'],
                "id_prueba": prueba_id,
                "id_subprueba": subprueba_id,
                "puntaje": puntaje,
                "media": media,
                "desviacion_estandar": ds,
                "escalar": "N/A",
                "interpretacion": interpretacion
            }
        
            if response.status_code == 404:
                response = requests.post('http://localhost:5000/evaluaciones', json=data)
                if response.status_code == 201:
                    print(f"Resultados guardados exitosamente para la subprueba '{subprueba_nombre}'.")
                else:
                    print(f"Error al guardar los resultados para la subprueba '{subprueba_nombre}': {response.status_code} - {response.text}")
            elif response.status_code == 200:
                response = requests.put(check_url, json=data)
                if response.status_code == 200:
                    print(f"Resultados actualizados exitosamente para la subprueba '{subprueba_nombre}'.")
                else:
                    print(f"Error al actualizar los resultados para la subprueba '{subprueba_nombre}': {response.status_code} - {response.text}")
            else:
                print(f"Error al verificar la evaluación para la subprueba '{subprueba_nombre}': {response.status_code} - {response.text}")

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
        prueba_nombre = self.windowTitle().replace("Prueba ", "")

        response = requests.get('http://localhost:5000/pruebas')
        if response.status_code != 200:
            print("Error al obtener las pruebas")
            return

        pruebas = response.json()
        prueba_id = next((p['id'] for p in pruebas if p['nombre'].lower() == prueba_nombre.lower()), None)
        if prueba_id is None:
            print("Prueba no encontrada en la base de datos.")
            return

        conclusion_text = self.conclusion_text_edit.toPlainText().strip()
        if not conclusion_text:
            print("La conclusión está vacía, no se guardará.")
            return

        data = {
            "codigo_hc": self.paciente_seleccionado['codigo_hc'],
            "id_prueba": prueba_id,
            "tipo_comentario": "Conclusión",
            "comentario": conclusion_text
        }

        try:
            response = requests.post('http://localhost:5000/comentarios', json=data)
            
            if response.status_code == 201:
                print("Conclusión guardada exitosamente")
            elif response.status_code == 500 and "UNIQUE constraint failed" in response.text:
                update_url = f"http://localhost:5000/comentarios/{data['codigo_hc']}/{data['id_prueba']}/{data['tipo_comentario']}"
                update_response = requests.put(update_url, json={"comentario": conclusion_text})
                
                if update_response.status_code == 200:
                    print("Conclusión actualizada exitosamente")
                else:
                    print(f"Error al actualizar la conclusión: {update_response.status_code} - {update_response.text}")
            else:
                print(f"Error al guardar la conclusión: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud: {e}")

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
    window = PruebaFuncionEjecutivaWindow({'codigo_hc': '12345'})
    window.show()
    sys.exit(app.exec_())