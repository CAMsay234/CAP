
import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

class SeleccionarPacienteWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle("Seleccionar Paciente")
        self.showMaximized()  # Abrir la ventana maximizada

        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Crear un layout horizontal para la barra azul con el logo, título, y botón de "Volver"
        header_layout = QHBoxLayout()

        # Barra azul más pequeña
        header_background = QWidget()
        header_background.setStyleSheet("background-color: #005BBB;")
        header_background_layout = QHBoxLayout(header_background)
        header_background_layout.setContentsMargins(0, 0, 0, 0)
        header_background.setFixedHeight(80)  # Ajusta la altura del banner

        # Logo de UPB
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(70, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Logo más pequeño
        self.logo.setPixmap(pixmap)
        header_background_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Título de la ventana
        titulo = QLabel("SELECCIONAR PACIENTE")
        titulo.setObjectName("titulo")  # Usar el estilo del archivo .qss para títulos
        header_background_layout.addWidget(titulo, alignment=Qt.AlignCenter)

        # Botón "Volver" para regresar a la página anterior
        self.boton_volver = QPushButton("Volver")
        self.boton_volver.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #005BBB;
                border-radius: 5px;
                padding: 5px 15px;  /* Ajustar padding para que el botón sea más pequeño */
                font-size: 14px;  /* Mantener el tamaño de la letra */
                min-width: 80px;  /* Cambiar el ancho mínimo del botón */
                border: 1px solid #005BBB;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.boton_volver.clicked.connect(self.volver_a_seleccionar_registrar)  # Conectar el botón a la función
        header_background_layout.addWidget(self.boton_volver, alignment=Qt.AlignRight)

        # Añadir el header al layout principal
        header_layout.addWidget(header_background)
        main_layout.addLayout(header_layout)

        # Crear un espaciador debajo de la barra azul
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Fondo blanco debajo del banner superior
        form_background = QWidget()
        form_background.setStyleSheet("background-color: white;")
        form_layout = QVBoxLayout(form_background)

        # Crear la etiqueta de documento de identidad
        label_documento = QLabel("DOCUMENTO DE IDENTIDAD DEL PACIENTE")
        label_documento.setFont(QFont('Arial', 18))  # Tamaño de fuente más pequeño
        label_documento.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(label_documento)

        # Crear el campo de entrada para el documento con borde negro
        self.input_documento = QLineEdit()
        self.input_documento.setPlaceholderText("Ingrese el documento del paciente")
        self.input_documento.setFont(QFont('Arial', 14))
        self.input_documento.setAlignment(Qt.AlignCenter)
        self.input_documento.setFixedWidth(300)  # Ajustar el tamaño del recuadro
        self.input_documento.setStyleSheet("""
            QLineEdit {
                border: 2px solid black;  /* Borde negro */
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        form_layout.addWidget(self.input_documento, alignment=Qt.AlignCenter)

        # Crear un botón de búsqueda con un ícono de lupa
        buscar_button_layout = QHBoxLayout()
        self.boton_buscar = QPushButton("Buscar Paciente")
        self.boton_buscar.setFont(QFont('Arial', 16))
        self.boton_buscar.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #003F73;
            }
        """)
        self.boton_buscar.clicked.connect(self.buscar_paciente)
        buscar_button_layout.addWidget(self.boton_buscar, alignment=Qt.AlignCenter)

        # Añadir el botón al layout principal
        form_layout.addLayout(buscar_button_layout)

        # Crear una etiqueta para mostrar el resultado del paciente encontrado
        self.label_resultado_paciente = QLabel("")
        self.label_resultado_paciente.setFont(QFont('Arial', 14))  # Ajustar el tamaño de la fuente
        self.label_resultado_paciente.setAlignment(Qt.AlignCenter)
        self.label_resultado_paciente.setStyleSheet("""
            QLabel {
                color: black;
                padding: 10px;
            }
        """)
        form_layout.addWidget(self.label_resultado_paciente, alignment=Qt.AlignCenter)

        # Crear el botón para ver la historia clínica
        self.boton_historia_clinica = QPushButton("Ver Historia Clínica")
        self.boton_historia_clinica.setFont(QFont('Arial', 14))
        self.boton_historia_clinica.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #003F73;
            }
        """)
        self.boton_historia_clinica.setVisible(False)  # Se oculta hasta que se haga una búsqueda exitosa
        self.boton_historia_clinica.clicked.connect(self.ir_a_historia_clinica)
        form_layout.addWidget(self.boton_historia_clinica, alignment=Qt.AlignCenter)

        #Crear boton para ir a evaluacion neuropsicologica
        self.boton_evaluacion_neuropsicologica = QPushButton("Evaluación Neuropsicológica")
        self.boton_evaluacion_neuropsicologica.setFont(QFont('Arial', 14))
        self.boton_evaluacion_neuropsicologica.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                border-radius: 10px;
                padding: 10px;
                width: 200px;
            }
            QPushButton:hover {
                background-color: #003F73;
            }
        """)
        self.boton_evaluacion_neuropsicologica.setVisible(False)  # Se oculta hasta que se haga una búsqueda exitosa
        self.boton_evaluacion_neuropsicologica.clicked.connect(self.ir_a_evaluacion_neuropsicologica)
        form_layout.addWidget(self.boton_evaluacion_neuropsicologica, alignment=Qt.AlignCenter)

        # Añadir los layouts al layout principal
        main_layout.addWidget(form_background)

        # Crear un widget central para contener los elementos
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def buscar_paciente(self):
        documento = self.input_documento.text().strip()  # Eliminar espacios y saltos de línea

        if not documento:
            QMessageBox.warning(self, "Error", "Por favor ingrese el documento del paciente.")
            return

        # Realizar la solicitud GET al backend para buscar el paciente
        url = f"http://127.0.0.1:5000/paciente/buscar?documento={documento}"

        try:
            response = requests.get(url)
            print(f"Status code: {response.status_code}")
            print(f"Response text: {response.text}")

            if response.status_code == 200:
                try:
                    paciente = response.json()  # Interpretar el JSON

                    # Verificar si el campo 'nombre' está en el JSON
                    if isinstance(paciente, dict) and 'nombre' in paciente:
                        # Mostrar solo el nombre del paciente en la interfaz
                        self.label_resultado_paciente.setText(f"Nombre: {paciente['nombre']}")
                        self.paciente_seleccionado = paciente  # Guardar el paciente seleccionado
                        
                        # Mostrar botón "Ver Historia Clínica"
                        self.boton_historia_clinica.setVisible(True)
                        self.boton_evaluacion_neuropsicologica.setVisible(True)
                    else:
                        self.label_resultado_paciente.setText("Formato de respuesta inesperado o falta de campo 'nombre'.")
                except ValueError as e:
                    self.label_resultado_paciente.setText("Error al interpretar la respuesta del servidor.")
            elif response.status_code == 404:
                self.label_resultado_paciente.setText("No se encontró el paciente.")
            else:
                QMessageBox.warning(self, "Error", f"Error en la solicitud al servidor. Código: {response.status_code}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al conectar con el servidor: {str(e)}")





    def volver_a_seleccionar_registrar(self):
        # Importar y abrir la ventana anterior
        from seleccionar_registrar_paciente import SeleccionarRegistrarPacienteWindow
        self.seleccionar_registrar_window = SeleccionarRegistrarPacienteWindow()
        self.seleccionar_registrar_window.show()
        self.close()
    
    def ir_a_historia_clinica(self):
        if hasattr(self, 'paciente_seleccionado'):
            # Pasar los datos del paciente seleccionado a la nueva ventana
            from historia_clinica import HistoriaClinicaWindow
            self.historia_clinica_window = HistoriaClinicaWindow(self.paciente_seleccionado)
            self.historia_clinica_window.show()
            self.close()  # Cerrar la ventana actual
        else:
            QMessageBox.warning(self, "Error", "No se ha seleccionado un paciente.")
    
    def ir_a_evaluacion_neuropsicologica(self):
        if hasattr(self, 'paciente_seleccionado'):
            # Pasar los datos del paciente seleccionado a la nueva ventana
            from evaluacion_neuropsicologica import EvaluacionNeuropsicologicaWindow
            self.evaluacion_neuropsicologica_window = EvaluacionNeuropsicologicaWindow(self.paciente_seleccionado)#pself.paciente_seleccionado)
            self.evaluacion_neuropsicologica_window.show()
            self.close()

# Función para cargar el archivo de estilos
def load_stylesheet(app):
    with open("styles.qss", "r") as file:
        app.setStyleSheet(file.read())

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Cargar el stylesheet general
    load_stylesheet(app)

    # Crear una instancia de la ventana principal
    ventana = SeleccionarPacienteWindow()
    ventana.show()

    sys.exit(app.exec_())
