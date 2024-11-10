import sqlite3
import sys
import os
import requests
import platform
from reportlab.pdfgen import canvas
from PyQt5.QtWidgets import QMessageBox
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QWidget, QSpacerItem, QSizePolicy, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class DiagnosticoWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()

        self.paciente_seleccionado = paciente_seleccionado
        self.hipotesis_map = {}  # Diccionario para mapear descripciones de hipótesis a sus IDs
        self.diagnostico_existente = False  # Bandera para saber si el diagnóstico ya existe

        # Configurar la ventana
        self.setWindowTitle(f"Diagnóstico de {self.paciente_seleccionado['nombre']}")
        self.showMaximized()  # Abrir la ventana maximizada
        self.setStyleSheet("background-color: white;")  # Fondo blanco

        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Crear el banner azul más grande
        header_layout = QHBoxLayout()
        header_background = QWidget()
        header_background.setStyleSheet("background-color: #005BBB;")
        header_background_layout = QHBoxLayout(header_background)
        header_background.setFixedHeight(150)  # Ajustar el tamaño del banner

        # Logo UPB
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        header_background_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Título en el banner
        self.label_titulo = QLabel("DIAGNÓSTICO")
        self.label_titulo.setFont(QFont('Arial', 36, QFont.Bold))
        self.label_titulo.setStyleSheet("color: white;")
        header_background_layout.addWidget(self.label_titulo, alignment=Qt.AlignCenter)

        # Información del paciente en el banner
        self.label_codigo = QLabel(f"Código: {self.paciente_seleccionado['codigo_hc']}")
        self.label_codigo.setFont(QFont('Arial', 14))
        self.label_nombre = QLabel(f"Nombre paciente: {self.paciente_seleccionado['nombre']}")
        self.label_nombre.setFont(QFont('Arial', 14))
        header_background_layout.addWidget(self.label_codigo, alignment=Qt.AlignRight)
        header_background_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))  # Añadir espacio entre código y nombre
        header_background_layout.addWidget(self.label_nombre, alignment=Qt.AlignRight)

        # Botón Volver en el banner
        self.boton_volver = QPushButton("VOLVER")
        self.boton_volver.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #005BBB;
                border-radius: 5px;
                padding: 5px;
                color: #005BBB;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #005BBB;
                color: white;
            }
        """)
        self.boton_volver.clicked.connect(self.volver)
        header_background_layout.addWidget(self.boton_volver, alignment=Qt.AlignRight)

        header_layout.addWidget(header_background)
        main_layout.addLayout(header_layout)

        # Espaciador debajo del banner
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Layout de contenido principal
        content_layout = QHBoxLayout()

        # Sección Izquierda: Hipótesis Diagnóstica
        left_layout = QVBoxLayout()
        self.hipotesis_button = QPushButton("HIPÓTESIS DIAGNÓSTICA")
        self.hipotesis_button.setStyleSheet("""
            QPushButton {
                background-color: #8AA4F7;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        left_layout.addWidget(self.hipotesis_button)

        # Campo de texto para ingresar hipótesis
        hipotesis_layout = QHBoxLayout()
        self.hipotesis_input = QLineEdit()
        self.hipotesis_input.setPlaceholderText("Ingrese la hipótesis")
        self.hipotesis_input.setStyleSheet("padding: 5px; border: 1px solid black;")
        self.hipotesis_input.returnPressed.connect(self.agregar_hipotesis_seleccionada)  # Conectar Enter para agregar hipótesis
        hipotesis_layout.addWidget(self.hipotesis_input)

        # Botón "+" para agregar hipótesis
        self.boton_agregar_hipotesis = QPushButton("+")
        self.boton_agregar_hipotesis.setStyleSheet("""
            QPushButton {
                background-color: #8AA4F7;
                color: white;
                padding: 5px;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        self.boton_agregar_hipotesis.clicked.connect(self.agregar_hipotesis_seleccionada)
        hipotesis_layout.addWidget(self.boton_agregar_hipotesis)

        left_layout.addLayout(hipotesis_layout)

        # Lista para mostrar las hipótesis seleccionadas
        self.lista_hipotesis = QListWidget()
        self.lista_hipotesis.setStyleSheet("border: 1px solid black; padding: 5px;")
        self.lista_hipotesis.itemClicked.connect(self.eliminar_hipotesis_seleccionada)  # Conectar al clic
        left_layout.addWidget(self.lista_hipotesis)

        # Campo de diagnóstico
        self.diagnostico_button = QPushButton("DIAGNÓSTICO")
        self.diagnostico_button.setStyleSheet("""
            QPushButton {
                background-color: #8AA4F7;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        left_layout.addWidget(self.diagnostico_button)

        self.diagnostico_input = QTextEdit()
        self.diagnostico_input.setPlaceholderText("Ingrese el diagnóstico")
        self.diagnostico_input.setStyleSheet("border: 1px solid black; padding: 5px;")
        left_layout.addWidget(self.diagnostico_input)

        content_layout.addLayout(left_layout)

        # Sección Derecha: Plan de Tratamiento
        right_layout = QVBoxLayout()
        self.tratamiento_button = QPushButton("PLAN DE TRATAMIENTO")
        self.tratamiento_button.setStyleSheet("""
            QPushButton {
                background-color: #8AA4F7;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        right_layout.addWidget(self.tratamiento_button)

        self.tratamiento_input = QTextEdit()
        self.tratamiento_input.setPlaceholderText("Ingrese el plan de tratamiento")
        self.tratamiento_input.setStyleSheet("border: 1px solid black; padding: 5px;")
        right_layout.addWidget(self.tratamiento_input)

        content_layout.addLayout(right_layout)
        main_layout.addLayout(content_layout)

        # Espaciador para separarlos de las firmas
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Botones para Guardar y Generar PDF
        botones_layout = QHBoxLayout()
        self.boton_guardar = QPushButton("GUARDAR")
        self.boton_guardar.setMaximumWidth(300)
        self.boton_guardar.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        self.boton_guardar.clicked.connect(self.guardar_diagnostico)  # Conectar el botón con la función guardar_diagnostico
        self.boton_pdf = QPushButton("GENERAR PDF")
        self.boton_pdf.setMaximumWidth(300)
        self.boton_pdf.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                padding: 10px;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        botones_layout.addWidget(self.boton_guardar)
        botones_layout.addWidget(self.boton_pdf)

        main_layout.addLayout(botones_layout)

        # Crear el widget principal
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Cargar diagnóstico del paciente si existe
        self.cargar_diagnostico_paciente()

        # Conectar el botón de PDF con la función generar_pdf
        self.boton_pdf.clicked.connect(self.generar_pdf)

    def cargar_diagnostico_paciente(self):
        """Función para cargar el diagnóstico del paciente si existe."""
        try:
            response = requests.get(f'http://127.0.0.1:5000/diagnosticos/{self.paciente_seleccionado["codigo_hc"]}')
            if response.status_code == 200:
                diagnostico = response.json()
                self.tratamiento_input.setPlainText(diagnostico['plan_tratamiento'])
                self.diagnostico_input.setPlainText(diagnostico['conclusion'])
                for hipotesis in diagnostico['hipotesis']:
                    item = QListWidgetItem(hipotesis['descripcion'])
                    self.lista_hipotesis.addItem(item)
                self.diagnostico_existente = True  # Marcar que el diagnóstico ya existe
            elif response.status_code == 404:
                print("No se encontró diagnóstico para este paciente.")
            else:
                print(f"Error al obtener el diagnóstico: {response.status_code}")
        except Exception as e:
            print(f"Error de conexión: {str(e)}")

    def agregar_hipotesis_seleccionada(self):
        """Función para agregar la hipótesis ingresada al recuadro."""
        hipotesis_seleccionada = self.hipotesis_input.text().strip()
        if hipotesis_seleccionada and hipotesis_seleccionada not in [self.lista_hipotesis.item(i).text() for i in range(self.lista_hipotesis.count())]:
            # Verificar si la hipótesis ya existe en la base de datos
            response = requests.get(f'http://127.0.0.1:5000/hipotesis')
            if response.status_code == 200:
                hipotesis_list = response.json()
                hipotesis_existente = next((h for h in hipotesis_list if h['descripcion'] == hipotesis_seleccionada), None)
                if hipotesis_existente:
                    hipotesis_id = hipotesis_existente['id']
                else:
                    # Crear una nueva hipótesis si no existe
                    response = requests.post('http://127.0.0.1:5000/hipotesis', json={"descripcion": hipotesis_seleccionada})
                    if response.status_code == 201:
                        hipotesis_id = response.json()['id']
                    else:
                        QMessageBox.critical(self, "Error", f"Error al crear la hipótesis: {response.status_code}")
                        return
                # Agregar la hipótesis ingresada al recuadro
                item = QListWidgetItem(hipotesis_seleccionada)  # Crear un nuevo ítem
                self.lista_hipotesis.addItem(item)  # Añadir el ítem a la lista
                self.hipotesis_map[hipotesis_seleccionada] = hipotesis_id  # Mapear la descripción al ID
                self.hipotesis_input.clear()  # Limpiar el campo de texto
            else:
                QMessageBox.critical(self, "Error", f"Error al obtener las hipótesis: {response.status_code}")

    def eliminar_hipotesis_seleccionada(self, item):
        """Función para eliminar una hipótesis seleccionada al hacer clic en ella."""
        self.lista_hipotesis.takeItem(self.lista_hipotesis.row(item))  # Eliminar el ítem seleccionado

    def guardar_diagnostico(self):
        """Función para guardar el diagnóstico en la base de datos."""
        codigo_hc = self.paciente_seleccionado['codigo_hc']
        plan_tratamiento = self.tratamiento_input.toPlainText()
        fecha = datetime.now().strftime("%Y-%m-%d")  # Obtener la fecha actual
        conclusion = self.diagnostico_input.toPlainText()
        hipotesis_ids = []  # Aquí deberías obtener los IDs de las hipótesis seleccionadas

        # Obtener las hipótesis seleccionadas
        for index in range(self.lista_hipotesis.count()):
            item_text = self.lista_hipotesis.item(index).text()
            hipotesis_id = self.hipotesis_map.get(item_text)  # Obtener el ID de la hipótesis
            if hipotesis_id:
                hipotesis_ids.append(hipotesis_id)

        data = {
            "codigo_hc": codigo_hc,
            "plan_Tratamiento": plan_tratamiento,
            "fecha": fecha,
            "conclusion": conclusion,
            "hipotesis_ids": hipotesis_ids
        }

        try:
            if self.diagnostico_existente:
                response = requests.put(f'http://127.0.0.1:5000/diagnosticos/{codigo_hc}', json=data)
                if response.status_code == 200:
                    QMessageBox.information(self, "Éxito", "Diagnóstico actualizado exitosamente")
                else:
                    QMessageBox.critical(self, "Error", f"Error al actualizar el diagnóstico: {response.status_code}")
            else:
                response = requests.post('http://127.0.0.1:5000/diagnosticos', json=data)
                if response.status_code == 201:
                    QMessageBox.information(self, "Éxito", "Diagnóstico guardado exitosamente")
                    self.diagnostico_existente = True  # Marcar que el diagnóstico ahora existe
                else:
                    QMessageBox.critical(self, "Error", f"Error al guardar el diagnóstico: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error de conexión: {str(e)}")

    def volver(self):
        """Función para volver a la pantalla de evaluación neuropsicológica."""
        self.close()
        from gui.evaluacion_neuropsicologica import EvaluacionNeuropsicologicaWindow
        self.evaluacion_neuropsicologica = EvaluacionNeuropsicologicaWindow(self.paciente_seleccionado)
        self.evaluacion_neuropsicologica.show()
    
    def generar_pdf(self):
        """Función para generar el PDF con la información del diagnóstico y otros detalles relevantes del paciente."""
        # Ruta para guardar el PDF en la carpeta de Descargas
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        pdf_filename = os.path.join(downloads_path, f"diagnostico_{self.paciente_seleccionado['codigo_hc']}.pdf")

        try:
            # Crear un objeto canvas de ReportLab para el PDF
            c = canvas.Canvas(pdf_filename)

            # Obtener la información del paciente desde la base de datos
            db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance', 'CAP.db'))

            if not os.path.exists(db_path):
                QMessageBox.critical(self, "Error", "El archivo de la base de datos no existe en la ruta especificada.")
                return

            # Configurar el cursor para que devuelva filas como diccionarios
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # Extraer información del paciente
            cursor.execute("SELECT * FROM pacientes WHERE codigo_hc=?", (self.paciente_seleccionado['codigo_hc'],))
            paciente_data = cursor.fetchone()

            # Extraer información del diagnóstico
            cursor.execute("SELECT * FROM diagnosticos WHERE codigo_hc=?", (self.paciente_seleccionado['codigo_hc'],))
            diagnostico_data = cursor.fetchone()

            # Verificar si los datos del paciente y diagnóstico existen
            if not paciente_data or not diagnostico_data:
                QMessageBox.critical(self, "Error", "No se encontró información del paciente o del diagnóstico en la base de datos.")
                return

            # Iniciar posición vertical para la escritura
            y_position = 800

            # Escribir información en el PDF utilizando nombres de columnas correctos
            c.setFont("Helvetica-Bold", 20)
            c.drawString(100, y_position, "Historia Clínica Neuropsicológica")
            y_position -= 40

            c.setFont("Helvetica", 14)
            c.drawString(100, y_position, f"Código: {paciente_data['codigo_hc']}")
            y_position -= 20
            c.drawString(100, y_position, f"Nombre del paciente: {paciente_data['nombre']}")
            y_position -= 20
            c.drawString(100, y_position, f"Edad: {paciente_data['edad']}")
            y_position -= 20
            c.drawString(100, y_position, f"Fecha de Nacimiento: {paciente_data['fecha_nacimiento']}")
            y_position -= 20
            c.drawString(100, y_position, f"Escolaridad (ID): {paciente_data['id_escolaridad']}")
            y_position -= 20
            c.drawString(100, y_position, f"Profesión: {paciente_data['profesion']}")
            y_position -= 20
            c.drawString(100, y_position, f"Teléfono: {paciente_data['telefono']}")
            y_position -= 20
            c.drawString(100, y_position, f"Celular: {paciente_data['celular']}")
            y_position -= 20
            c.drawString(100, y_position, f"Remisión: {paciente_data['remision']}")
            y_position -= 40

            # Conclusión
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, y_position, "Conclusión:")
            y_position -= 20
            c.setFont("Helvetica", 12)
            c.drawString(120, y_position, diagnostico_data['conclusion'])
            y_position -= 40

            # Plan de Tratamiento
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, y_position, "Plan de Tratamiento:")
            y_position -= 20
            c.setFont("Helvetica", 12)
            c.drawString(120, y_position, diagnostico_data['plan_Tratamiento'])
            y_position -= 40

            # Hipótesis Diagnóstica
            c.setFont("Helvetica-Bold", 16)
            c.drawString(100, y_position, "Hipótesis Diagnóstica:")
            y_position -= 20
            c.setFont("Helvetica", 12)

            cursor.execute("""
                SELECT h.descripcion 
                FROM diagnostico_hipotesis dh
                JOIN hipotesis h ON dh.codigo_hipotesis = h.id
                WHERE dh.codigo_hc=?
            """, (self.paciente_seleccionado['codigo_hc'],))
            hipotesis = cursor.fetchall()
            for hip in hipotesis:
                c.drawString(120, y_position, f"- {hip['descripcion']}")
                y_position -= 20

            # Guardar el PDF
            c.save()

            # Mostrar mensaje de confirmación
            QMessageBox.information(self, "Éxito", f"PDF generado exitosamente: {pdf_filename}")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error", f"Error en la base de datos: {str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ha ocurrido un error: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    paciente = {"codigo_hc": 1, "nombre": "Camilo Velasquez"}
    window = DiagnosticoWindow(paciente)
    window.show()
    sys.exit(app.exec_())