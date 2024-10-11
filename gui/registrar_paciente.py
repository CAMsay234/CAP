import os
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QGridLayout, QComboBox, QDateEdit
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QDate
import requests  # Para realizar las solicitudes al backend
from datetime import datetime
from evaluacion_neuropsicologica import EvaluacionNeuropsicologicaWindow  # Importar la clase de la ventana de evaluación neuropsicológica

class RegistrarPacienteWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar el layout principal
        main_layout = QVBoxLayout()

        # Configurar la ventana
        self.setWindowTitle("Registrar paciente")
        self.showMaximized()  # Abrir la ventana maximizada
        self.setStyleSheet("background-color: white;")  # Fondo blanco

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
        self.title = QLabel("DATOS PERSONALES")
        self.title.setFont(QFont('Arial', 18, QFont.Bold))
        self.title.setStyleSheet("color: white;")
        header_background_layout.addWidget(self.title, alignment=Qt.AlignCenter)

        # Campo de código
        # Crear el campo de texto de código
        self.codigo_label = QLabel("Código:")
        self.codigo_label.setFont(QFont('Arial', 10))  # Reducir el tamaño de la fuente
        self.codigo_input = QLabel()
        self.codigo_input.setText(f"{self.obtener_siguiente_codigo()}")
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
        self.boton_volver.clicked.connect(self.abrir_seleccionar_registrar_paciente)
        header_background_layout.addWidget(self.boton_volver, alignment=Qt.AlignRight)

        # Crear el formulario de datos personales
        form_layout = QGridLayout()

        labels = ["Nombre completo", "Fecha de nacimiento", "Escolaridad", "Profesión/Ocupación", "Celular"]
        right_labels = ["Edad", "Documento de identidad", "Fecha actual", "Teléfono", "Remisión"]

        # Agregar los campos del lado izquierdo con títulos en la parte superior
        for i, label in enumerate(labels):
            label_widget = QLabel(label)
            label_widget.setProperty('subtitulo', True)  # Aplicar el estilo de subtítulo

            if label == "Fecha de nacimiento":
                self.fecha_nacimiento_input = QDateEdit()  # Asignar a un atributo de la clase
                self.fecha_nacimiento_input.setCalendarPopup(True)
                self.fecha_nacimiento_input.setStyleSheet("color: #000000; width: 80px")
                input_widget = self.fecha_nacimiento_input
            elif label == "Escolaridad":
                self.escolaridad_combo = QComboBox()  # Crear el combo box para el nivel de escolaridad
                self.load_niveles_escolaridad()  # Cargar los niveles de escolaridad en el combo box
                input_widget = self.escolaridad_combo
            else:
                # Asignar los campos de texto como atributos
                if label == "Nombre completo":
                    self.nombre_input = QLineEdit()
                    input_widget = self.nombre_input
                elif label == "Profesión/Ocupación":
                    self.profesion_input = QLineEdit()
                    input_widget = self.profesion_input
                elif label == "Celular":
                    self.celular_input = QLineEdit()
                    input_widget = self.celular_input
                else:
                    input_widget = QLineEdit()

                input_widget.setPlaceholderText(f"Ingrese {label.lower()}")

            form_layout.addWidget(label_widget, i, 0)  # Título
            form_layout.addWidget(input_widget, i, 1)  # Campo de entrada

        # Agregar los campos del lado derecho con títulos en la parte superior
        for i, label in enumerate(right_labels):
            label_widget = QLabel(label)
            label_widget.setProperty('subtitulo', True)  # Aplicar el estilo de subtítulo

            if label == "Fecha actual":
                self.fecha_actual_input = QDateEdit()  # Asignar a un atributo de la clase
                self.fecha_actual_input.setDate(QDate.currentDate())  # Fecha actual automática
                self.fecha_actual_input.setCalendarPopup(True)
                self.fecha_actual_input.setStyleSheet("color: #000000; width: 80px")
                input_widget = self.fecha_actual_input

            else:
                if label == "Documento de identidad":
                    self.documento_input = QLineEdit()
                    input_widget = self.documento_input
                elif label == "Edad":
                    self.edad_input = QLineEdit()
                    input_widget = self.edad_input
                elif label == "Teléfono":
                    self.telefono_input = QLineEdit()
                    input_widget = self.telefono_input
                elif label == "Remisión":
                    self.remision_input = QLineEdit()
                    input_widget = self.remision_input
                else:
                    input_widget = QLineEdit()

                input_widget.setPlaceholderText(f"Ingrese {label.lower()}")

            form_layout.addWidget(label_widget, i, 2)  # Título
            form_layout.addWidget(input_widget, i, 3)  # Campo de entrada

        form_widget = QWidget()
        form_widget.setStyleSheet("""
            QWidget {
                border: 2px solid #E0E0E0;
                border-radius: 15px;
                padding: 20px;
                background-color: #F8F8F8;
            }
            QLineEdit {
                font-size: 14px;
                padding: 5px;
                border: 1px solid #B0B0B0;
                border-radius: 5px;
            }
        """)
        form_widget.setLayout(form_layout)
        main_layout.addWidget(form_widget)

        # Crear los botones inferiores
        buttons_layout = QHBoxLayout()

        self.boton_guardar = QPushButton("Guardar datos personales")
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

        # Conectar el botón "Guardar datos personales" con la función para guardar el paciente y abrir la ventana de evaluación
        self.boton_guardar.clicked.connect(self.guardar_paciente)

        main_layout.addLayout(buttons_layout)

        # Crear un widget central para contener los elementos
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    def abrir_seleccionar_registrar_paciente(self):
        from seleccionar_registrar_paciente import SeleccionarRegistrarPacienteWindow  # Importar la nueva ventana de registro de pacientes
        self.seleccionar_registrar_paciente_window = SeleccionarRegistrarPacienteWindow()   # Crear la ventana de registrar paciente
        self.seleccionar_registrar_paciente_window.show()  # Mostrar la ventana de registrar paciente
        self.close()  # Cerrar la ventana actual

    def load_niveles_escolaridad(self):
        """Cargar los niveles de escolaridad desde la base de datos al combo box."""
        url = "http://127.0.0.1:5000/niveles_escolaridad"  # URL de la API
        try:
            response = requests.get(url)
            if response.status_code == 200:
                niveles = response.json()
                self.escolaridad_combo.clear()  # Limpiar el combo box antes de agregar nuevos niveles
                for nivel in niveles:
                    # Agregar la descripción con su ID como dato asociado
                    self.escolaridad_combo.addItem(nivel['descripcion'], nivel['id'])
            else:
                print("Error al obtener los niveles de escolaridad")
        except Exception as e:
            print(f"Error de conexión: {str(e)}")

    def guardar_y_abrir_hc(self):
        """Cierra la ventana actual y abre la ventana EvaluacionNeuropsicologicaWindow."""
        from historia_clinica import HistoriaClinicaWindow  # Importar la nueva ventana de registro de pacientes
        if hasattr(self, 'paciente_seleccionado'):
            self.historia_clinica_window = HistoriaClinicaWindow(self.paciente_seleccionado)  
            self.historia_clinica_window.show()  
            self.close()

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

    def guardar_paciente(self):
        try:
            # Validar que todos los campos requeridos estén llenos
            if not self.documento_input.text() or not self.nombre_input.text() or not self.edad_input.text():
                raise ValueError("Todos los campos obligatorios deben estar completos.")

            # Intentar convertir el campo de edad a un entero
            edad = int(self.edad_input.text())

            # Obtener los datos del paciente desde los campos de entrada
            data = {
                "documento": self.documento_input.text(),
                "nombre": self.nombre_input.text(),
                "edad": edad,
                "fecha_nacimiento": self.fecha_nacimiento_input.date().toString("yyyy-MM-dd"),
                "id_escolaridad": self.escolaridad_combo.currentData(),
                "profesion": self.profesion_input.text(),
                "telefono": self.telefono_input.text(),
                "celular": self.celular_input.text(),
                "remision": self.remision_input.text()
            }

            # Realizar la solicitud POST para guardar el paciente
            response = requests.post('http://localhost:5000/paciente/nuevo', json=data)

            if response.status_code == 201:
                # Mostrar mensaje de éxito
                success_msg = QMessageBox()
                success_msg.setIcon(QMessageBox.Information)  # Icono de información para éxito
                success_msg.setWindowTitle("Éxito")
                success_msg.setText("Paciente guardado correctamente.")
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
                paciente = response.json()
                self.paciente_seleccionado = paciente  # Guardar la respuesta del paciente
                self.guardar_y_abrir_hc()  # Guardar el paciente y abrir la ventana de evaluación neuropsicológica
            else:
                # Mostrar mensaje de error si la respuesta no fue exitosa
                error_msg = QMessageBox()
                error_msg.setIcon(QMessageBox.Critical)
                error_msg.setWindowTitle("Error")
                error_msg.setText(f"Error al guardar el paciente. Código: {response.status_code}")
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
            # Mostrar mensaje de advertencia si hay algún campo vacío o si la edad no es válida
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

    


# Ejemplo de cómo llamar a la clase
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = RegistrarPacienteWindow()
    window.show()
    sys.exit(app.exec_())