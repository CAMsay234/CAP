import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QScrollArea, QPushButton, QTextEdit, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
import requests
from datetime import datetime, date

class SeguimientoWindow(QMainWindow): 
    def __init__(self, paciente_seleccionado):
        super().__init__()
        self.paciente_seleccionado = paciente_seleccionado

        # Configurar la ventana
        self.setWindowTitle(f"Seguimiento de {self.paciente_seleccionado['nombre']}")
        self.showMaximized()  # Abrir la ventana maximizada
        self.setStyleSheet("background-color: white;")  # Fondo blanco

        # Crear el layout principal
        main_layout = QVBoxLayout()

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
        pixmap = QPixmap(image_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        header_background_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Título
        self.title = QLabel("SEGUIMIENTO")
        self.title.setFont(QFont('Arial', 24, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        header_background_layout.addWidget(self.title, alignment=Qt.AlignCenter)

        # Información del paciente en el banner
        self.label_codigo = QLabel(f"Código: {self.paciente_seleccionado['codigo_hc']}")
        self.label_codigo.setFont(QFont('Arial', 14))
        self.label_nombre = QLabel(f"Nombre paciente: {self.paciente_seleccionado['nombre']}")
        self.label_nombre.setFont(QFont('Arial', 14))
        header_background_layout.addWidget(self.label_codigo, alignment=Qt.AlignRight)
        header_background_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))  # Añadir espacio entre código y nombre
        header_background_layout.addWidget(self.label_nombre, alignment=Qt.AlignRight)

        # Botón "Volver" en la esquina derecha
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
        self.boton_volver.clicked.connect(self.abrir_evaluacion_neuropsicologica)  # Conectar el botón para volver
        header_background_layout.addWidget(self.boton_volver, alignment=Qt.AlignRight)

        header_layout.addWidget(header_background)
        main_layout.addLayout(header_layout)

        # Espaciador debajo del banner
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Layout principal dividido en dos secciones: Izquierda y Derecha
        content_layout = QHBoxLayout()

        # ======== Sección Izquierda: Número de sesión y Fecha ========
        left_layout = QVBoxLayout()

        # Botón "Número de la sesión"
        self.sesion_button = QPushButton("Número de la sesión")
        self.sesion_button.setFixedSize(200, 40)  # Ancho y altura fija para consistencia
        self.sesion_button.setStyleSheet("""
            QPushButton {
                background-color: #8AA4F7;
                color: white;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        left_layout.addWidget(self.sesion_button, alignment=Qt.AlignCenter)

        # Campo de entrada para el número de la sesión
        self.sesion_input = QLineEdit()
        self.sesion_input.setPlaceholderText("Ingrese el número de la sesión")
        self.sesion_input.setFixedSize(500, 35)
        self.sesion_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid black;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        left_layout.addWidget(self.sesion_input, alignment=Qt.AlignCenter)

        # Espacio entre los elementos
        left_layout.addSpacing(20)

        # Botón "Fecha de la sesión"
        self.fecha_button = QPushButton("Fecha de la sesión")
        self.fecha_button.setFixedSize(200, 40)
        self.fecha_button.setStyleSheet("""
            QPushButton {
                background-color: #8AA4F7;
                color: white;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        left_layout.addWidget(self.fecha_button, alignment=Qt.AlignCenter)

        # Campo de entrada para la fecha
        self.fecha_input = QLineEdit()
        self.fecha_input.setPlaceholderText("dd/mm/aaaa")
        self.fecha_input.setFixedSize(500, 35)
        self.fecha_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid black;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        left_layout.addWidget(self.fecha_input, alignment=Qt.AlignCenter)

        # Añadir la sección izquierda al layout principal
        content_layout.addLayout(left_layout)

        # ======== Sección Derecha: Motivo de consulta ========
        right_layout = QVBoxLayout()

        # Botón "Motivo de consulta"
        self.motivo_button = QPushButton("Motivo de consulta")
        self.motivo_button.setFixedSize(500, 40)
        self.motivo_button.setStyleSheet("""
            QPushButton {
                background-color: #8AA4F7;
                color: white;
                font-size: 14px;
                border-radius: 5px;
            }
        """)
        right_layout.addWidget(self.motivo_button, alignment=Qt.AlignCenter)

        # Campo de texto para el motivo de consulta
        self.motivo_input = QTextEdit()
        self.motivo_input.setPlaceholderText("Ingrese el motivo de consulta")
        self.motivo_input.setFixedSize(800, 100)
        self.motivo_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid black;
                padding: 5px;
                border-radius: 5px;
            }
        """)
        right_layout.addWidget(self.motivo_input, alignment=Qt.AlignCenter)

        # Añadir la sección derecha al layout principal
        content_layout.addLayout(right_layout)

        # ======== Añadir el layout de contenido al layout principal ========
        main_layout.addLayout(content_layout)

        # ======== Botón Inferior "Guardar seguimiento" ========
        buttons_layout = QHBoxLayout()

        self.boton_guardar = QPushButton("Guardar seguimiento")
        self.boton_guardar.setFixedSize(250, 50)
        self.boton_guardar.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #003F73;
            }
        """)
        buttons_layout.addWidget(self.boton_guardar, alignment=Qt.AlignCenter)

        # Conectar el botón "Guardar seguimiento"
        self.boton_guardar.clicked.connect(self.guardar_seguimiento)

        main_layout.addLayout(buttons_layout)

        # Establecer el widget central con scroll
        scroll.setWidget(scroll_widget)
        self.setCentralWidget(scroll)

    def obtener_siguiente_codigo(self):
        """Función para obtener el siguiente código disponible desde el backend."""
        url = "http://127.0.0.1:5000/pacientes/count"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return str(data.get('count', 0) + 1)  # Incrementar en 1 para el siguiente código
            else:
                return "Error"
        except Exception as e:
            print(f"Error de conexión: {str(e)}")
            return "Error"
        
    def abrir_evaluacion_neuropsicologica(self):
        from gui.evaluacion_neuropsicologica import EvaluacionNeuropsicologicaWindow
        self.close()
        self.evaluacion_neuropsicologica_ventana = EvaluacionNeuropsicologicaWindow(paciente_seleccionado=self.paciente_seleccionado)
        self.evaluacion_neuropsicologica_ventana.show()
        self.close()

    def guardar_seguimiento(self):
        """Función para guardar el seguimiento en la base de datos."""
        try:
            codigo_hc = self.paciente_seleccionado['codigo_hc']
            num_seccion = int(self.sesion_input.text())  # Asegúrate de que sea un número
            fecha_str = self.fecha_input.text()  # Obtener la fecha como cadena
            descripcion = self.motivo_input.toPlainText()

            # Verificar si los campos están completos
            if not num_seccion or not fecha_str or not descripcion:
                QMessageBox.critical(self, "Error", "Por favor completa todos los campos.")
                return

            # Convertir la fecha de 'dd/mm/yyyy' a un objeto datetime.date
            try:
                fecha = datetime.strptime(fecha_str, "%d/%m/%Y").date()
            except ValueError:
                QMessageBox.critical(self, "Error", "Formato de fecha incorrecto. Usa 'dd/mm/aaaa'.")
                return

            # Convertir la fecha a una cadena en formato 'YYYY-MM-DD'
            fecha_json = fecha.strftime("%Y-%m-%d")

            data = {
                "codigo_hc": codigo_hc,
                "num_sesion": num_seccion,
                "fecha": fecha_json,  # Enviar la fecha como cadena serializable
                "descripcion": descripcion
            }

            print(f"Datos enviados: {data}")  # Log para depuración

            # Enviar la solicitud al backend
            if hasattr(self, 'diagnostico_existente') and self.diagnostico_existente:
                response = requests.put(f'http://127.0.0.1:5000/seguimientos/{codigo_hc}', json=data)
            else:
                response = requests.post('http://127.0.0.1:5000/seguimientos', json=data)

            print(f"Respuesta del servidor: {response.status_code} - {response.text}")

            if response.status_code in [200, 201]:
                QMessageBox.information(self, "Éxito", "Seguimiento guardado exitosamente")
                self.diagnostico_existente = True  # Marcar que el seguimiento ahora existe
            else:
                QMessageBox.critical(self, "Error", f"Error al guardar: {response.status_code}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error de conexión: {str(e)}")
            print(f"Error de conexión: {str(e)}")  # Log del error

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SeguimientoWindow(paciente_seleccionado={})
    window.show()
    sys.exit(app.exec_())