import sys
import os
import requests
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QWidget, QScrollArea, QFormLayout, QSpacerItem, QSizePolicy, QDialog, QApplication, QMessageBox
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from gui.areas import AreasWindow
from gui.estado_mental import EstadoMentalWindow
from gui.evaluacion_neuropsicologica import EvaluacionNeuropsicologicaWindow
 
class HistoriaClinicaWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()
 
        self.paciente_seleccionado = paciente_seleccionado  # Datos del paciente seleccionado
 
        # Configurar la ventana
        self.setWindowTitle(f"Historia Clínica de {self.paciente_seleccionado['nombre']}")
        self.showMaximized()
        self.setStyleSheet("background-color: white;")
 
        # Layout principal
        main_layout = QVBoxLayout()
 
        # Crear la barra azul con el logo y el botón de "Volver"
        header_layout = QHBoxLayout()
 
        # Crear un widget que actúe como barra azul
        header_background = QWidget()
        header_background.setStyleSheet("background-color: #005BBB;")
        header_background_layout = QHBoxLayout(header_background)
        header_background_layout.setContentsMargins(0, 0, 0, 0)
 
        # Logo de UPB
        logo_label = QLabel()
        logo_pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'src', 'upb.png')).scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        header_background_layout.addWidget(logo_label, alignment=Qt.AlignLeft)
 
        # Título
        titulo = QLabel("HISTORIA CLÍNICA")
        titulo.setFont(QFont('Arial', 24))
        titulo.setStyleSheet("color: white;")
        header_background_layout.addWidget(titulo, alignment=Qt.AlignCenter)
 
        # Botón "Volver" en la esquina superior derecha
        self.boton_volver = QPushButton("Volver")
        self.boton_volver.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #005BBB;
                border-radius: 5px;
                padding: 5px 15px;
                font-size: 14px;
                min-width: 80px;
                border: 1px solid #005BBB;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        self.boton_volver.clicked.connect(self.volver_a_seleccionar_registrar)
        header_background_layout.addWidget(self.boton_volver, alignment=Qt.AlignRight)
 
        # Añadir el layout del fondo azul al header
        header_layout.addWidget(header_background)
        main_layout.addLayout(header_layout)
 
        # Añadir los campos de "Código" y "Nombre" debajo del banner
        paciente_info_layout = QHBoxLayout()
 
        codigo_label = QLabel(f"Código: {self.paciente_seleccionado['codigo_hc']}")
        codigo_label.setProperty("subtitulo", True)
        paciente_info_layout.addWidget(codigo_label, alignment=Qt.AlignLeft)
 
        nombre_label = QLabel(f"Nombre: {self.paciente_seleccionado['nombre']}")
        nombre_label.setProperty("subtitulo", True)
        paciente_info_layout.addWidget(nombre_label, alignment=Qt.AlignLeft)
 
        main_layout.addLayout(paciente_info_layout)
 
        # Crear un espaciador debajo de los datos del paciente
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))
 
        # Scroll area para el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
 
        # Crear un widget central para la parte de formulario
        scroll_content = QWidget()
        scroll_layout = QFormLayout(scroll_content)
 
        # Campos del formulario con borde y en QTextEdit
        self.campos = {
            "motivo_consulta": ("Motivo de consulta", "Ingrese el motivo de consulta del paciente"),
            "estado_actual": ("Estado actual", "Describa el estado actual del paciente"),
            "antecedentes": ("Antecedentes psiquiátricos familiares", "Ingrese antecedentes psiquiátricos familiares"),
            "historial_personal": ("Historia personal", "Ingrese la historia personal del paciente"),
            "historial_familiar": ("Historia de la dinámica familiar", "Ingrese la historia de la dinámica familiar")
        }
 
        for key, (label, placeholder) in self.campos.items():
            label_widget = QLabel(f"{label}:")
            label_widget.setFont(QFont('Arial', 18))
            label_widget.setStyleSheet("color:black;")
            input_widget = QTextEdit()  # Cambiado a QTextEdit
            input_widget.setPlaceholderText(placeholder)
            input_widget.setFont(QFont('Arial', 12))
            input_widget.setStyleSheet("""
                QTextEdit {
                    border: 1px solid #005BBB;
                    padding: 5px;
                    height: 100px;  /* Aumenta la altura para permitir múltiples líneas */
                }
            """)
            setattr(self, key, input_widget)
            scroll_layout.addRow(label_widget, input_widget)
 
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
 
        # Crear los botones en la parte inferior
        button_layout = QVBoxLayout()
 
        # Crear los botones para subpestañas
        sub_buttons_layout = QHBoxLayout()
 
        estado_mental_button = QPushButton("Estado Mental")
        estado_mental_button.setFont(QFont('Arial', 16))
        estado_mental_button.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                padding: 10px;
                border-radius: 5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #003F73;
            }
        """)
        estado_mental_button.clicked.connect(self.abrir_estado_mental)
        sub_buttons_layout.addWidget(estado_mental_button)
 
        areas_button = QPushButton("Áreas")
        areas_button.setFont(QFont('Arial', 16))
        areas_button.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                padding: 10px;
                border-radius: 5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #003F73;
            }
        """)
        areas_button.clicked.connect(self.abrir_areas)
        sub_buttons_layout.addWidget(areas_button)
 
        button_layout.addLayout(sub_buttons_layout)
 
        # Botón para guardar historia clínica
        boton_guardar = QPushButton("Actualizar historia clínica")
        boton_guardar.setFont(QFont('Arial', 16))
        boton_guardar.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                padding: 10px;
                border-radius: 5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #003F73;
            }
        """)
        button_layout.addWidget(boton_guardar, alignment=Qt.AlignCenter)
        boton_guardar.clicked.connect(self.guardar_historia_clinica)
 
        # Añadir el layout de botones al layout principal
        main_layout.addLayout(button_layout)
 
        # Crear el widget principal
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)
 
        # Llamar a la función verificar_datos_historia_clinica para cargar los datos al abrir la ventana
        self.verificar_datos_historia_clinica()
 
    def volver_a_seleccionar_registrar(self):
        # Ir a la ventana de seleccionar_registrar_paciente.py
        from gui.seleccionar_registrar_paciente import SeleccionarRegistrarPacienteWindow
        self.seleccionar_registrar_window = SeleccionarRegistrarPacienteWindow()
        self.seleccionar_registrar_window.show()
        self.close()  # Cerrar la ventana actual
 
    def abrir_estado_mental(self):
        if hasattr(self, 'paciente_seleccionado'):
            self.estado_mental = EstadoMentalWindow(self.paciente_seleccionado)
            self.estado_mental.show()
 
    def abrir_areas(self):
        if hasattr(self, 'paciente_seleccionado'):
            self.areas = AreasWindow(self.paciente_seleccionado)
            self.areas.show()
 
    def abrir_evaluacion_neuropsicologica(self):
        if hasattr(self, 'paciente_seleccionado'):
            self.evaluaciones_neuropsicologicas = EvaluacionNeuropsicologicaWindow(self.paciente_seleccionado)
            self.evaluaciones_neuropsicologicas.show()
            self.close()
 
    def verificar_datos_historia_clinica(self):
        """Función para verificar si hay datos de la historia clínica y cargarlos si existen."""
        try:
            # Realizar la solicitud GET al backend
            url = f"http://localhost:5000/historias/{self.paciente_seleccionado['codigo_hc']}"
            response = requests.get(url)
           
            if response.status_code == 200:
                historia_clinica = response.json()
               
                # Llenar los campos de texto con los datos obtenidos
                self.motivo_consulta.setPlainText(historia_clinica.get('motivo_consulta', ''))
                self.estado_actual.setPlainText(historia_clinica.get('estado_actual', ''))
                self.antecedentes.setPlainText(historia_clinica.get('antecedentes', ''))
                self.historial_personal.setPlainText(historia_clinica.get('historial_personal', ''))
                self.historial_familiar.setPlainText(historia_clinica.get('historial_familiar', ''))
           
            elif response.status_code == 404:
                # No hay datos de historia clínica, permitir registrar nuevos datos
                pass
           
            else:
                # Mostrar ventana de error si hay un problema con la solicitud
                error_msg = QMessageBox()
                error_msg.setIcon(QMessageBox.Critical)
                error_msg.setWindowTitle("Error")
                error_msg.setText("Error al verificar la historia clínica")
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
 
    def guardar_historia_clinica(self):
        try:
            # Validar que todos los campos de la historia clínica estén llenos
            if not self.motivo_consulta.toPlainText() or not self.estado_actual.toPlainText() or not self.antecedentes.toPlainText() or not self.historial_personal.toPlainText() or not self.historial_familiar.toPlainText():
                raise ValueError("Todos los campos obligatorios deben estar completos.")
       
            # Obtener los datos de la historia clínica desde los campos de entrada
            data = {
                "codigo_hc": self.paciente_seleccionado['codigo_hc'],
                "documento_paciente": self.paciente_seleccionado['documento'],
                "motivo_consulta": self.motivo_consulta.toPlainText(),
                "estado_actual": self.estado_actual.toPlainText(),
                "antecedentes": self.antecedentes.toPlainText(),
                "historial_personal": self.historial_personal.toPlainText(),
                "historial_familiar": self.historial_familiar.toPlainText()
            }
       
            # Verificar si la historia clínica ya existe
            url = f"http://localhost:5000/historias/{self.paciente_seleccionado['codigo_hc']}"
            response = requests.get(url)
           
            if response.status_code == 200:
                # Historia clínica existente, realizar una solicitud PUT para actualizarla
                response = requests.put(url, json=data)
                if response.status_code == 200:
                    # Mostrar mensaje de éxito
                    success_msg = QMessageBox()
                    success_msg.setIcon(QMessageBox.Information)  # Icono de información para éxito
                    success_msg.setWindowTitle("Éxito")
                    success_msg.setText("Historia clínica actualizada correctamente.")
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
                    self.abrir_evaluacion_neuropsicologica()
                else:
                    # Mostrar mensaje de error si la respuesta no fue exitosa
                    error_msg = QMessageBox()
                    error_msg.setIcon(QMessageBox.Critical)
                    error_msg.setWindowTitle("Error")
                    error_msg.setText(f"Error al actualizar la historia clínica. Código: {response.status_code}")
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
            elif response.status_code == 404:
                # Historia clínica no existente, realizar una solicitud POST para crearla
                response = requests.post('http://localhost:5000/historias', json=data)
                if response.status_code == 201:
                    # Mostrar mensaje de éxito
                    success_msg = QMessageBox()
                    success_msg.setIcon(QMessageBox.Information)  # Icono de información para éxito
                    success_msg.setWindowTitle("Éxito")
                    success_msg.setText("Historia clínica guardada correctamente.")
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
                    self.abrir_evaluacion_neuropsicologica()
                else:
                    # Mostrar mensaje de error si la respuesta no fue exitosa
                    error_msg = QMessageBox()
                    error_msg.setIcon(QMessageBox.Critical)
                    error_msg.setWindowTitle("Error")
                    error_msg.setText(f"Error al guardar la historia clínica. Código: {response.status_code}")
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
            else:
                # Mostrar mensaje de error si la respuesta no fue exitosa
                error_msg = QMessageBox()
                error_msg.setIcon(QMessageBox.Critical)
                error_msg.setWindowTitle("Error")
                error_msg.setText(f"Error al verificar la historia clínica. Código: {response.status_code}")
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
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    paciente = {'codigo_hc': 1, 'nombre': 'Camilo Velasquez'}
    window = HistoriaClinicaWindow(paciente)
    window.show()
    sys.exit(app.exec_())