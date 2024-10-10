import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QScrollArea, QPushButton, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt
import requests

class SeguimientoWindow(QMainWindow): 
    def __init__(self, paciente_seleccionado):
        super().__init__()
        self.paciente_seleccionado = paciente_seleccionado

        # Configurar la ventana
        self.setWindowTitle("Seguimiento")
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
        pixmap = QPixmap(image_path).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        header_background_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Título
        self.title = QLabel("SEGUIMIENTO")
        self.title.setFont(QFont('Arial', 24, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        header_background_layout.addWidget(self.title, alignment=Qt.AlignCenter)

        # Campo de código
        self.codigo_label = QLabel(f"Código:{self.paciente_seleccionado['codigo_hc']}")
        self.codigo_label.setFont(QFont('Arial', 10))  # Reducir el tamaño de la fuente
        self.codigo_input = QLabel()
        self.codigo_input.setFixedWidth(100)
        codigo_layout = QHBoxLayout()  # Definir el layout antes de usarlo
        codigo_layout.addWidget(self.codigo_label, alignment=Qt.AlignRight)
        codigo_layout.addWidget(self.codigo_input, alignment=Qt.AlignRight)
        self.codigo_input.setFont(QFont('Arial', 10))  # Reducir el tamaño de la fuente para el valor del código
        header_background_layout.addLayout(codigo_layout)

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
                font-size: 12px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.boton_volver.clicked.connect(self.abrir_evaluacion_neuropsicologica)  # Conectar el botón para volver
        header_background_layout.addWidget(self.boton_volver, alignment=Qt.AlignRight)

        # Botón "guardar" en la esquina derecha
        self.boton_guardar = QPushButton("GUARDAR")
        self.boton_guardar.setStyleSheet("""
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
        self.boton_guardar.clicked.connect(self.guardar_seguimiento)  # Conectar el botón para volver
        header_background_layout.addWidget(self.boton_guardar, alignment=Qt.AlignRight)

        header_layout.addWidget(header_background)
        main_layout.addLayout(header_layout)

        # Crear el formulario de seguimiento
        form_layout = QGridLayout()

        labels = ["ID seguimiento", "Fecha", "Motivo de consulta", "Objetivo de la sesión"]
        right_labels = ["Intervención", "Observaciones", "Plan de tratamiento", "Próxima cita"]

        # Agregar los campos del lado izquierdo con títulos en la parte superior
        for i, label in enumerate(labels):
            label_widget = QLabel(label)
            label_widget.setFont(QFont('Arial', 14))
            label_widget.setProperty('subtitulo', True)  # Aplicar el estilo de subtítulo

            if label == "Fecha":
                self.fecha_input = QLineEdit()
                self.fecha_input.setPlaceholderText("dd/mm/aaaa")
                input_widget = self.fecha_input
            else:
                input_widget = QTextEdit()
                input_widget.setPlaceholderText(f"Ingrese {label.lower()}")

            form_layout.addWidget(label_widget, i, 0)  # Título
            form_layout.addWidget(input_widget, i, 1)  # Campo de entrada

        # Agregar los campos del lado derecho con títulos en la parte superior
        for i, label in enumerate(right_labels):
            label_widget = QLabel(label)
            label_widget.setFont(QFont('Arial', 14))
            label_widget.setProperty('subtitulo', True)  # Aplicar el estilo de subtítulo

            input_widget = QTextEdit()
            input_widget.setPlaceholderText(f"Ingrese {label.lower()}")

            form_layout.addWidget(label_widget, i, 2)  # Título
            form_layout.addWidget(input_widget, i, 3)  # Campo de entrada

        form_widget = QWidget()
        form_widget.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 20px;
            }
            QLineEdit, QTextEdit {
                font-size: 14px;
                border: 1px solid #999;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        form_widget.setLayout(form_layout)
        main_layout.addWidget(form_widget)

        # Crear los botones inferiores
        buttons_layout = QHBoxLayout()

        self.boton_guardar = QPushButton("Guardar seguimiento")
        self.boton_guardar.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;  /* Color azul */
                color: white;
                font-size: 16px;
                padding: 15px 30px;  /* Aumenta el padding */
                border-radius: 10px;  /* Aumenta el radio del borde */
                width: 250px;  /* Asegúrate de que el ancho sea lo suficientemente grande */
            }
            QPushButton:hover {
                background-color: #003F73;  /* Color más oscuro al pasar el cursor */
            }
        """)
        buttons_layout.addWidget(self.boton_guardar, alignment=Qt.AlignCenter)

        # Conectar el botón "Guardar seguimiento" con la función para guardar el seguimiento
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
        from evaluacion_neuropsicologica import EvaluacionNeuropsicologicaWindow
        self.close()
        self.evaluacion_neuropsicologica_ventana = EvaluacionNeuropsicologicaWindow(paciente_seleccionado=self.paciente_seleccionado)
        self.evaluacion_neuropsicologica_ventana.show()
        self.close()

    def guardar_seguimiento(self):
        # Implementar la lógica para guardar el seguimiento
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SeguimientoWindow(paciente_seleccionado={})
    window.show()
    sys.exit(app.exec_())