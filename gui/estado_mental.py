import sys
import os
import requests
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QWidget, QGridLayout, QApplication, QLineEdit, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class EstadoMentalWindow(QMainWindow):
    def __init__(self, paciente_seleccionado=None):
        super().__init__()
        self.paciente_seleccionado = paciente_seleccionado
        self.setWindowTitle("Estado Mental")
        self.setFixedSize(800, 600)  # Tamaño fijo más pequeño

        # Configurar el layout principal
        main_layout = QVBoxLayout()

        # Crear la barra azul con el logo, título y el campo de código
        header_layout = QHBoxLayout()
        header_background = QWidget()
        header_background.setStyleSheet("background-color: #005BBB;")
        header_background_layout = QHBoxLayout(header_background)

        # Logo UPB
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Tamaño más pequeño
        self.logo.setPixmap(pixmap)
        header_background_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

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

        # Botón "Guardar" en la esquina derecha
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
        self.boton_guardar.clicked.connect(self.guardar_estado_mental)
        header_background_layout.addWidget(self.boton_guardar, alignment=Qt.AlignRight)

        # Sección de estados mentales
        estados_mentales = ["Atención", "Memoria", "Lenguaje", "Pensamiento", "Introspección"]
        self.campos_estado_mental = self.add_comment_section("ESTADO MENTAL", estados_mentales, main_layout)

        # Configurar el widget principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Llamar a la función verificar_datos_estado_mental para cargar los datos al abrir la ventana
        self.verificar_datos_estado_mental()

    def verificar_datos_estado_mental(self):
        """Función para verificar si hay datos del estado mental y cargarlos si existen."""
        try:
            # Realizar la solicitud GET al backend
            url = f"http://localhost:5000/estado_mental/{self.paciente_seleccionado['codigo_hc']}"
            response = requests.get(url)
            
            if response.status_code == 200:
                estado_mental = response.json()
                
                # Llenar los campos de texto con los datos obtenidos
                self.campos_estado_mental["Atención"].setPlainText(estado_mental.get('atencion', ''))
                self.campos_estado_mental["Memoria"].setPlainText(estado_mental.get('memoria', ''))
                self.campos_estado_mental["Lenguaje"].setPlainText(estado_mental.get('lenguaje', ''))
                self.campos_estado_mental["Pensamiento"].setPlainText(estado_mental.get('pensamiento', ''))
                self.campos_estado_mental["Introspección"].setPlainText(estado_mental.get('introspeccion', ''))
            
            elif response.status_code == 404:
                # No hay datos de estado mental, permitir registrar nuevos datos
                pass
            
            else:
                # Mostrar ventana de error si hay un problema con la solicitud
                error_msg = QMessageBox()
                error_msg.setIcon(QMessageBox.Critical)
                error_msg.setWindowTitle("Error")
                error_msg.setText("Error al verificar el estado mental")
                error_msg.setInformativeText("Por favor, asegúrese de que los datos del paciente sean correctos.")
                error_msg.setDetailedText(f"Status Code: {response.status_code}, Error: {response.text}")
                error_msg.setStandardButtons(QMessageBox.Ok)
                error_msg.exec_()

        except requests.exceptions.RequestException as e:
            # Mostrar ventana de error si hay problemas de conexión
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowTitle("Error de Conexión")
            error_msg.setText("No se pudo conectar con el servidor")
            error_msg.setInformativeText("Revise su conexión a internet o intente más tarde.")
            error_msg.setDetailedText(str(e))
            error_msg.setStandardButtons(QMessageBox.Ok)
            error_msg.exec_()

    def guardar_estado_mental(self):
        try:
            # Validar que todos los campos de estado mental estén llenos
            for campo in self.campos_estado_mental.values():
                if not campo.toPlainText():
                    raise ValueError("Todos los campos obligatorios deben estar completos.")

            # Obtener los datos de estado mental desde los campos de entrada
            data = {
                "codigo_hc": self.paciente_seleccionado['codigo_hc'],
                "documento_paciente": self.paciente_seleccionado['documento'],
                "atencion": self.campos_estado_mental["Atención"].toPlainText(),
                "memoria": self.campos_estado_mental["Memoria"].toPlainText(),
                "lenguaje": self.campos_estado_mental["Lenguaje"].toPlainText(),
                "pensamiento": self.campos_estado_mental["Pensamiento"].toPlainText(),
                "introspeccion": self.campos_estado_mental["Introspección"].toPlainText()
            }

            # Realizar la solicitud POST para guardar el estado mental
            response = requests.post('http://localhost:5000/estado_mental', json=data)
            
            if response.status_code == 201:
                # Mostrar mensaje de éxito
                success_msg = QMessageBox()
                success_msg.setIcon(QMessageBox.Information)  # Icono de información para éxito
                success_msg.setWindowTitle("Éxito")
                success_msg.setText("Estado mental guardado correctamente.")
                success_msg.setStyleSheet("""
                    QMessageBox {
                        background-color: #f8f8f8;
                        font-size: 10px;
                    }
                    QLabel {
                        font-size: 12px;
                        color: #333333;
                    }
                    QPushButton {
                        background-color: #005BBB;
                        font-size: 10px;
                        color: white;
                        padding: 2px;
                        border-radius: 2px;
                    }
                    QPushButton:hover {
                        background-color: #004C99;
                    }
                """)
                success_msg.exec_()
            else:
                # Mostrar mensaje de error si la respuesta no fue exitosa
                error_msg = QMessageBox()
                error_msg.setIcon(QMessageBox.Critical)
                error_msg.setWindowTitle("Error")
                error_msg.setText(f"Error al guardar el estado mental. Código: {response.status_code}")
                error_msg.setStyleSheet("""
                    QMessageBox {
                        background-color: #f8f8f8;
                        font-size: 10px;
                    }
                    QLabel {
                        font-size: 12px;
                        color: #333333;
                    }
                    QPushButton {
                        background-color: #005BBB;
                        font-size: 10px;
                        color: white;
                        padding: 2px;
                        border-radius: 2px;
                    }
                    QPushButton:hover {
                        background-color: #004C99;
                    }
                """)
                error_msg.exec_()

        except ValueError as ve:
            # Mostrar mensaje de advertencia si hay algún campo vacío
            warning_msg = QMessageBox()
            warning_msg.setIcon(QMessageBox.Warning)
            warning_msg.setWindowTitle("Advertencia")
            warning_msg.setText(str(ve))
            warning_msg.setStyleSheet("""
                QMessageBox {
                    background-color: #f8f8f8;
                    font-size: 10px;
                }
                QLabel {
                    font-size: 12px;
                    color: #333333;
                }
                QPushButton {
                    background-color: #005BBB;
                    font-size: 10px;
                    color: white;
                    padding: 2px;
                    border-radius: 2px;
                }
                QPushButton:hover {
                    background-color: #004C99;
                }
            """)
            warning_msg.exec_()

        except requests.exceptions.RequestException as re:
            # Mostrar ventana de error si hubo un problema con la conexión al servidor
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowTitle("Error de conexión")
            error_msg.setText(f"No se pudo conectar con el servidor. Detalles: {str(re)}")
            error_msg.setStyleSheet("""
                QMessageBox {
                    background-color: #f8f8f8;
                    font-size: 10px;
                }
                QLabel {
                    font-size: 12px;
                    color: #333333;
                }
                QPushButton {
                    background-color: #005BBB;
                    font-size: 10px;
                    color: white;
                    padding: 2px;
                    border-radius: 2px;
                }
                QPushButton:hover {
                    background-color: #004C99;
                }
            """)
            error_msg.exec_()

        except Exception as e:
            # Mostrar ventana de error si ocurrió un error inesperado
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowTitle("Error inesperado")
            error_msg.setText(f"Ocurrió un error inesperado: {str(e)}")
            error_msg.setStyleSheet("""
                QMessageBox {
                    background-color: #f8f8f8;
                    font-size: 10px;
                }
                QLabel {
                    font-size: 12px;
                    color: #333333;
                }
                QPushButton {
                    background-color: #005BBB;
                    font-size: 10px;
                    color: white;
                    padding: 2px;
                    border-radius: 2px;
                }
                QPushButton:hover {
                    background-color: #004C99;
                }
            """)
            error_msg.exec_()

    def add_comment_section(self, title, comments, layout):
        """Añadir sección de comentarios clínicos con múltiples líneas"""
        title_label = QLabel(title)
        title_label.setFont(QFont('Arial', 14, QFont.Bold))  # Letra más pequeña
        title_label.setStyleSheet("background-color: #4A90E2; color: white; padding: 5px; border-radius: 5px;")  # Fondo azul claro y letra blanca
        layout.addWidget(title_label)

        comment_layout = QGridLayout()
        campos = {}
        for i, comment in enumerate(comments):
            label = QLabel(comment)
            label.setFont(QFont('Arial', 12)) 
            label.setProperty("comentarios", True) # Letra más pequeña
            label.setStyleSheet("color: black; background-color: #f0f0f0; padding: 5px;")  # Letra negra y fondo gris
            label.setWordWrap(True)  # Asegurar que el texto se envuelva
            comment_layout.addWidget(label, i, 0)

            # Añadir campo de texto asociado al comentario
            input_field = QTextEdit()
            input_field.setFont(QFont('Arial', 10))
            input_field.setStyleSheet("border: 1px solid black;")  # Añadir borde a las casillas de comentarios
            input_field.setFixedHeight(100)  # Ajustar altura fija
            comment_layout.addWidget(input_field, i, 1)
            campos[comment] = input_field

        layout.addLayout(comment_layout)
        return campos

# Función para ejecutar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    paciente = {'codigo_hc': 1, 'nombre': 'Camilo Velasquez'}
    window = EstadoMentalWindow(paciente)
    window.show()
    sys.exit(app.exec_())