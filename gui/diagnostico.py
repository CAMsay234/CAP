import sys
import os
import requests
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QWidget, QSpacerItem, QSizePolicy, QListWidget, QListWidgetItem, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class DiagnosticoWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()

        self.paciente_seleccionado = paciente_seleccionado
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

        # ComboBox para seleccionar hipótesis
        self.combo_hipotesis = QComboBox()
        self.combo_hipotesis.setStyleSheet("padding: 5px; border: 1px solid black;")
        left_layout.addWidget(self.combo_hipotesis)

        # Llamar a la función para cargar las hipótesis desde el backend
        self.cargar_hipotesis()

        # Conectar la selección del combo al método de agregar hipótesis seleccionada
        self.combo_hipotesis.currentIndexChanged.connect(self.agregar_hipotesis_seleccionada)

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

    def cargar_hipotesis(self):
        """Función para cargar las hipótesis desde la base de datos usando una petición GET."""
        try:
            response = requests.get('http://127.0.0.1:5000/hipotesis')  # Cambia esta URL si es necesario
            if response.status_code == 200:
                hipotesis = response.json()  # Obtener la lista de hipótesis
                self.combo_hipotesis.clear()  # Limpiar el ComboBox antes de añadir nuevas opciones
                self.combo_hipotesis.addItem("Seleccione una hipótesis")  # Añadir un elemento por defecto
                for h in hipotesis:
                    self.combo_hipotesis.addItem(h['descripcion'])  # Añadir cada hipótesis al ComboBox
            else:
                print(f"Error al obtener las hipótesis: {response.status_code}")
        except Exception as e:
            print(f"Error de conexión: {str(e)}")

    def agregar_hipotesis_seleccionada(self):
        """Función para agregar la hipótesis seleccionada al recuadro."""
        hipotesis_seleccionada = self.combo_hipotesis.currentText()
        if hipotesis_seleccionada != "Seleccione una hipótesis" and hipotesis_seleccionada not in [self.lista_hipotesis.item(i).text() for i in range(self.lista_hipotesis.count())]:
            # Agregar la hipótesis seleccionada al recuadro
            item = QListWidgetItem(hipotesis_seleccionada)  # Crear un nuevo ítem
            self.lista_hipotesis.addItem(item)  # Añadir el ítem a la lista

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
            # Aquí deberías mapear el texto de la hipótesis al ID correspondiente
            # Por simplicidad, asumimos que el texto es el ID
            hipotesis_ids.append(item_text)

        data = {
            "codigo_hc": codigo_hc,
            "plan_Tratamiento": plan_tratamiento,
            "fecha": fecha,
            "conclusion": conclusion,
            "hipotesis_ids": hipotesis_ids
        }

        try:
            response = requests.post('http://127.0.0.1:5000/diagnosticos', json=data)
            if response.status_code == 201:
                QMessageBox.information(self, "Éxito", "Diagnóstico guardado exitosamente")
            else:
                QMessageBox.critical(self, "Error", f"Error al guardar el diagnóstico: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error de conexión: {str(e)}")

    def volver(self):
        """Función para volver a la pantalla de evaluación neuropsicológica."""
        self.close()
        from evaluacion_neuropsicologica import EvaluacionNeuropsicologicaWindow
        self.evaluacion_neuropsicologica = EvaluacionNeuropsicologicaWindow(self.paciente_seleccionado)
        self.evaluacion_neuropsicologica.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    paciente = {"codigo_hc": 1, "nombre": "Camilo Velasquez"}
    window = DiagnosticoWindow(paciente)
    window.show()
    sys.exit(app.exec_())
