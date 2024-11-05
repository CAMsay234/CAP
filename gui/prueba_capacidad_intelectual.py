import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QScrollArea, QPushButton, QTextEdit
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
import threading  # Importar el módulo para trabajar con bases de datos SQLite
 
 
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
        self.boton_guardar.clicked.connect(self.guardar_todo)  # Conectar el botón para guardar
        header_background_layout.addWidget(self.boton_guardar, alignment=Qt.AlignRight)
 
        # Tabla de pruebas
        self.add_table("PRUEBAS", ["DISEÑO CON CUBOS", "SEMEJANZAS", "RETENCIÓN DE DÍGITOS", "MATRICES", "VOCABULARIO",
                                   "ARITMÉTICA", "BÚSQUEDA DE SÍMBOLOS", "ROMPECABEZAS VISUAL", "INFORMACIÓN", "CLAVES",
                                   "SUCESIÓN DE NÚMEROS Y LETRAS", "PESO FIGURADO", "COMPRENSIÓN", "CANCELACIÓN", "FIGURAS INCOMPLETAS"], main_layout)
 
        # Tabla de conversión de puntuaciones
        self.add_conversion("CONVERSIÓN DE LA SUMA DE PUNTUACIONES ESCALARES A PUNTUACIONES COMPUESTAS", ["COMPRENSIÓN VERBAL", "RAZONAMIENTO PERCEPTUAL", "MEMORIA DE TRABAJO", "VELOCIDAD DE PROCESAMIENTO", "TOTAL"], main_layout)
       
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
   
    def obtener_puntuaciones_escalas(self):
        """Obtiene las puntuaciones escalares totales de cada subprueba."""
        puntuaciones = {}
        for row in range(1, self.table_layout.rowCount()):
            # Obtener el widget de subprueba
            subprueba_widget = self.table_layout.itemAtPosition(row, 0).widget()
            if subprueba_widget and isinstance(subprueba_widget, QLabel):
                subprueba = subprueba_widget.text().strip()
            else:
                continue  # Si no hay subprueba, pasa a la siguiente fila
 
            # Obtener el widget de la puntuación escalar total
            puntuacion_widget = self.table_layout.itemAtPosition(row, 3).widget()
            if puntuacion_widget and isinstance(puntuacion_widget, QLineEdit):
                try:
                    puntuacion = int(puntuacion_widget.text().strip())
                except ValueError:
                    puntuacion = 0  # Si no es un número válido, asigna 0
            else:
                puntuacion = 0  # Si no hay widget, asigna 0
 
            puntuaciones[subprueba] = puntuacion
 
        return puntuaciones
 

    
    def guardar_prueba(self):
        """Función para guardar los valores de la prueba."""
        def guardar_prueba_thread():
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
        
            print("Verificando widgets en el layout...")
        
            # Recorrer cada fila de subpruebas y obtener sus valores
            for row in range(1, self.table_layout.rowCount()):
                subprueba_widget = self.table_layout.itemAtPosition(row, 0)
                puntaje_widget = self.table_layout.itemAtPosition(row, 1)
                escalar_container = self.table_layout.itemAtPosition(row, 2)
        
                # Verificar que los widgets existen
                if not subprueba_widget or not puntaje_widget or not escalar_container:
                    print(f"Error: Faltan datos en la fila {row}.")
                    return
        
                # Obtener los valores de los widgets
                subprueba_nombre = subprueba_widget.widget().text().strip() if subprueba_widget.widget() else "N/A"
                puntaje = puntaje_widget.widget().text().strip() if puntaje_widget.widget() else None
        
                # Acceder al layout del widget contenedor para la puntuación escalar
                escalar_layout = escalar_container.widget().layout()
                escalar_values = []
        
                # Obtener el patrón para esta fila
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
                patron = patrones[(row - 1) % len(patrones)]  # Obtener el patrón correcto
        
                # Extraer los valores solo de los campos habilitados (False en el patrón)
                for i, pintar in enumerate(patron):
                    escalar_input = escalar_layout.itemAt(i).widget()
                    if escalar_input and not pintar:  # Si el campo está habilitado (False en el patrón)
                        value = escalar_input.text().strip() or None
                        escalar_values.append(value)
        
                # Verificar que todos los campos de escalar tengan un valor
                if not all(escalar_values):
                    print(f"Faltan datos para la subprueba '{subprueba_nombre}'.")
                    continue
        
                # Depuración: Mostrar los valores de puntuación escalar
                print(f"Puntuaciones escalares para '{subprueba_nombre}': {escalar_values}")
        
                # Verificar si la subprueba existe en la base de datos
                response = requests.get(f'http://localhost:5000/subpruebas')
                if response.status_code != 200:
                    print(f"Error al obtener las subpruebas para la prueba '{subprueba_nombre}'.")
                    continue
        
                subpruebas = response.json()
                subprueba_id = next(
                    (sp['id'] for sp in subpruebas if sp['nombre'].lower() == subprueba_nombre.lower() and sp['id_prueba'] == prueba_id),
                    None
                )
        
                # Registrar la subprueba si no existe
                if subprueba_id is None:
                    data_subprueba = {"id_prueba": prueba_id, "nombre": subprueba_nombre}
                    response = requests.post('http://localhost:5000/subpruebas', json=data_subprueba)
                    if response.status_code == 201:
                        # Obtener el ID de la subprueba recién creada
                        response = requests.get(f'http://localhost:5000/subpruebas')
                        if response.status_code == 200:
                            subpruebas = response.json()
                            subprueba_id = next(
                                (sp['id'] for sp in subpruebas if sp['nombre'].lower() == subprueba_nombre.lower() and sp['id_prueba'] == prueba_id),
                                None
                            )
                            if subprueba_id:
                                print(f"Subprueba '{subprueba_nombre}' registrada exitosamente con ID {subprueba_id}.")
                            else:
                                print(f"No se encontró el ID de la subprueba '{subprueba_nombre}' después de registrarla.")
                                continue
                        else:
                            print(f"Error al obtener subpruebas después de crear '{subprueba_nombre}': {response.status_code}")
                            continue
                    else:
                        print(f"Error al registrar la subprueba '{subprueba_nombre}': {response.status_code} - {response.text}")
                        continue
        
                # Verificar si ya existe una evaluación para esta combinación de valores
                check_url = f"http://localhost:5000/evaluaciones/{self.paciente_seleccionado['codigo_hc']}/{prueba_id}/{subprueba_id}"
                response = requests.get(check_url)
        
                data = {
                    "codigo_hc": self.paciente_seleccionado['codigo_hc'],
                    "id_prueba": prueba_id,
                    "id_subprueba": subprueba_id,
                    "puntaje": puntaje,
                    "media" : None,
                    "desviacion_estandar" : None,
                    "escalar": ", ".join(escalar_values),  # Guardar como string separado por comas
                    "interpretacion": None
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
    
        # Iniciar el hilo
        thread = threading.Thread(target=guardar_prueba_thread)
        thread.start()
        
    
    
    def guardar_conversion(self):
        """Función para guardar los valores de la tabla de conversión."""
        def guardar_conversion_thread():
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
    
            # Recorrer las filas y obtener los valores
            for row, fields in enumerate(self.input_fields, start=1):
                subprueba_nombre = self.conversion_layout.itemAtPosition(row, 0).widget().text().strip()
                
                # Verificar si la subprueba existe en la base de datos
                response = requests.get(f'http://localhost:5000/subpruebas')
                if response.status_code != 200:
                    print(f"Error al obtener las subpruebas para la prueba '{subprueba_nombre}'.")
                    continue
    
                subpruebas = response.json()
                subprueba_id = next(
                    (sp['id'] for sp in subpruebas if sp['nombre'].lower() == subprueba_nombre.lower() and sp['id_prueba'] == prueba_id),
                    None
                )
    
                # Registrar la subprueba si no existe
                if subprueba_id is None:
                    data_subprueba = {"id_prueba": prueba_id, "nombre": subprueba_nombre}
                    response = requests.post('http://localhost:5000/subpruebas', json=data_subprueba)
                    if response.status_code == 201:
                        # Obtener el ID de la subprueba recién creada
                        response = requests.get(f'http://localhost:5000/subpruebas')
                        if response.status_code == 200:
                            subpruebas = response.json()
                            subprueba_id = next(
                                (sp['id'] for sp in subpruebas if sp['nombre'].lower() == subprueba_nombre.lower() and sp['id_prueba'] == prueba_id),
                                None
                            )
                            if subprueba_id:
                                print(f"Subprueba '{subprueba_nombre}' registrada exitosamente con ID {subprueba_id}.")
                            else:
                                print(f"No se encontró el ID de la subprueba '{subprueba_nombre}' después de registrarla.")
                                continue
                        else:
                            print(f"Error al obtener subpruebas después de crear '{subprueba_nombre}': {response.status_code}")
                            continue
                    else:
                        print(f"Error al registrar la subprueba '{subprueba_nombre}': {response.status_code} - {response.text}")
                        continue
                
                try:
                    suma_puntuacion = float(fields[0].text().strip() or 0.0)
                    puntuacion_compuesta = float(fields[1].text().strip() or 0.0)
                    rango_percentil = float(fields[2].text().strip() or 0.0)
                    intervalo_confianza = float(fields[3].text().strip() or 0.0)
                except ValueError as e:
                    print(f"Error al convertir los valores en la fila {row}: {e}")
                    continue
                
                print(f"Subprueba: {subprueba_nombre}, Suma: {suma_puntuacion}, "
                    f"Compuesta: {puntuacion_compuesta}, Percentil: {rango_percentil}, IC: {intervalo_confianza}")
    
                # Verificar si ya existe una evaluación para esta combinación de valores
                check_url = f"http://localhost:5000/conversiones/{self.paciente_seleccionado['codigo_hc']}/{prueba_id}/{subprueba_id}"
                response = requests.get(check_url)
     
                # Preparar los datos para la API
                data = {
                    "codigo_hc": self.paciente_seleccionado['codigo_hc'],
                    "id_prueba": prueba_id,
                    "id_subprueba": subprueba_id,  
                    "suma_puntuacion": suma_puntuacion,
                    "puntuacion_compuesta": puntuacion_compuesta,
                    "rango_percentil": rango_percentil,
                    "intervalo_confianza": intervalo_confianza
                }
    
                # Realizar la solicitud
                response = requests.post(f"http://localhost:5000/conversiones", json=data)
                if response.status_code == 201:
                    print(f"Conversión guardada exitosamente para la subprueba '{subprueba_id}'.")
                else:
                    print(f"Error al guardar la conversión: {response.status_code} - {response.text}")
    
        # Iniciar el hilo
        thread = threading.Thread(target=guardar_conversion_thread)
        thread.start()

    def guardar_todo(self):
        """Función para guardar tanto las pruebas como las conversiones."""
        self.guardar_prueba()
        self.guardar_conversion()

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
 
        # Crear el layout de la tabla
        self.table_layout = QGridLayout()  # Asegurarse de que self.table_layout esté disponible en toda la clase
        headers = ["PRUEBAS", "PUNTUACIÓN NATURAL", "PUNTUACIÓN ESCALAR", "PUNTUACIÓN ESCALAR TOTAL"]
 
        # Agregar encabezados a la tabla
        for col, header in enumerate(headers):
            header_label = QLabel(header)
            header_label.setFont(QFont('Arial', 14, QFont.Bold))
            header_label.setStyleSheet("color: white; background-color: #4A90E2; padding: 10px; border-radius: 5px;")
            header_label.setAlignment(Qt.AlignCenter)
            self.table_layout.addWidget(header_label, 0, col)
 
        # Agregar filas de pruebas
        for row, test in enumerate(tests, start=1):
            # Nombre de la prueba
            test_label = QLabel(test)
            test_label.setAlignment(Qt.AlignCenter)
            test_label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")
            self.table_layout.addWidget(test_label, row, 0)
 
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
            self.table_layout.addWidget(natural_input, row, 1)
 
            # PUNTUACIÓN ESCALAR - con 4 rectángulos pequeños
            escalar_layout = self.crear_rectangulos_puntuacion_escalar(row - 1)
 
            # Asegúrate de colocar el layout de forma correcta
            container_widget = QWidget()
            container_widget.setLayout(escalar_layout)
            self.table_layout.addWidget(container_widget, row, 2)
 
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
            self.table_layout.addWidget(total_input, row, 3)
 
        layout.addLayout(self.table_layout)
 
    def add_conversion(self, title, tests, layout):
        """Función para agregar una tabla con las conversiones de las pruebas."""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 16, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: black; background-color: #B0C4DE; padding: 10px;")
        layout.addWidget(title_label)

        self.conversion_layout = QGridLayout()  # Crear el layout de conversiones
        headers = ["ESCALA", "SUMA PUNTUACIONES ESCALARES", "PUNTUACIÓN COMPUESTA",
                "RANGO PERCENTIL", "INTERVALO CONFIANZA, TOTAL"]

        # Agregar encabezados
        for col, header in enumerate(headers):
            header_label = QLabel(header)
            header_label.setFont(QFont('Arial', 14, QFont.Bold))
            header_label.setStyleSheet("color: white; background-color: #4A90E2; padding: 10px; border-radius: 5px;")
            header_label.setAlignment(Qt.AlignCenter)
            self.conversion_layout.addWidget(header_label, 0, col)

        # Agregar filas de datos
        self.input_fields = []  # Almacenar los campos para referencia futura

        for row, test in enumerate(tests, start=1):
            # Añadir nombre de la subprueba
            test_label = QLabel(test)
            test_label.setAlignment(Qt.AlignCenter)
            test_label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")
            self.conversion_layout.addWidget(test_label, row, 0)

            # Crear y añadir campos de entrada
            row_fields = []  # Almacenar los campos de esta fila
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
                self.conversion_layout.addWidget(input_field, row, col)
                row_fields.append(input_field)

            self.input_fields.append(row_fields)  # Guardar los campos de la fila

        layout.addLayout(self.conversion_layout)

# Función para ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    paciente = {'codigo_hc': 1, 'nombre': 'Camilo Velasquez'}
    window = PruebaCapacidadIntelectualWindow(paciente)
    window.show()
    sys.exit(app.exec_())