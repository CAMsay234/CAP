import os
from PyQt5.QtWidgets import QMainWindow,QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QSpacerItem, QSizePolicy, QGridLayout, QComboBox, QDateEdit
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QDate
import requests  # Para realizar las solicitudes al backend
from datetime import datetime

class RegistrarPacienteWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configurar la ventana
        self.setWindowTitle("Registrar Paciente")
        self.showMaximized()  # Abrir la ventana maximizada
        self.setStyleSheet("background-color: white;")  # Fondo blanco

        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Crear la barra azul con el logo y el campo de código
        header_layout = QHBoxLayout()

        # Crear un widget que actúe como barra azul
        header_background = QWidget()
        header_background.setStyleSheet("background-color: #005BBB;")
        header_background_layout = QHBoxLayout(header_background)
        header_background_layout.setContentsMargins(0, 0, 0, 0)

        # Logo de UPB
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        header_background_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Título
        titulo = QLabel("DATOS PERSONALES")
        titulo.setFont(QFont('Arial', 40))  # Tamaño más grande para el título principal
        titulo.setStyleSheet("color: white;")
        header_background_layout.addWidget(titulo, alignment=Qt.AlignCenter)

        
        # Campo de código
        codigo_layout = QVBoxLayout()
        codigo_label = QLabel("Código:")
        codigo_label.setFont(QFont('Arial', 10))
        codigo_label.setStyleSheet("color: white;")
        codigo_label.setProperty('subtitulo', True)
        codigo_layout.addWidget(codigo_label)

        # Crear el campo de texto de código
        self.codigo_input = QLineEdit()
        self.codigo_input.setText(f"{self.obtener_siguiente_codigo()}")
        self.codigo_input.setFixedWidth(100)
        codigo_layout.addWidget(self.codigo_input, alignment=Qt.AlignRight)
        header_background_layout.addLayout(codigo_layout)

        # Añadir el layout del fondo azul al header
        header_layout.addWidget(header_background)
        main_layout.addLayout(header_layout)

        # Crear un espaciador debajo de la barra azul
        main_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

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
                min-width: 250px;  /* Asegúrate de que el ancho sea lo suficientemente grande */
            }
            QPushButton:hover {
                background-color: #003F73;  /* Color más oscuro al pasar el cursor */
            }
        """)
          
        buttons_layout.addWidget(self.boton_guardar, alignment=Qt.AlignCenter)
         # Conectar el botón "Guardar datos personales" con la función para guardar el paciente
        self.boton_guardar.clicked.connect(self.guardar_paciente)
        

        self.boton_continuar = QPushButton("Continuar historia clínica")
        self.boton_continuar.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;  /* Color azul */
                color: white;
                font-size: 16px;
                padding: 15px 30px;  /* Aumenta el padding */
                border-radius: 10px;  /* Aumenta el radio del borde */
                min-width: 250px;  /* Asegúrate de que el ancho sea lo suficientemente grande */
            }
            QPushButton:hover {
                background-color: #003F73;  /* Color más oscuro al pasar el cursor */
            }
        """)
        buttons_layout.addWidget(self.boton_continuar, alignment=Qt.AlignCenter)

        main_layout.addLayout(buttons_layout)

        # Crear un widget central para contener los elementos
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

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
            # Validar y convertir los datos críticos
            codigo = int(self.codigo_input.text())  # Convertir el código a entero
            edad = int(self.edad_input.text())  # Convertir la edad a entero

            # Obtener el ID del nivel de escolaridad seleccionado
            id_escolaridad = self.escolaridad_combo.currentData()  # Obtiene el dato asociado (ID) de la opción seleccionada
            if id_escolaridad is None:
                raise ValueError("No se ha seleccionado un nivel de escolaridad válido.")

            # Verificar campos obligatorios
            if not self.documento_input.text() or not self.nombre_input.text() or not self.profesion_input.text():
                raise ValueError("Todos los campos son obligatorios.")

            # Obtener la fecha de nacimiento como objeto de tipo date
            fecha_nacimiento_qdate = self.fecha_nacimiento_input.date()
            fecha_nacimiento = datetime(
                fecha_nacimiento_qdate.year(),
                fecha_nacimiento_qdate.month(),
                fecha_nacimiento_qdate.day()
            ).date()

            # Crear el diccionario de datos
            data = {
                'codigo': codigo,
                'documento': self.documento_input.text(),
                'nombre': self.nombre_input.text(),
                'edad': edad,
                'fecha_nacimiento': fecha_nacimiento.isoformat(),  # En formato ISO 'yyyy-MM-dd'
                'id_escolaridad': id_escolaridad,
                'profesion': self.profesion_input.text(),
                'telefono': self.telefono_input.text(),
                'celular': self.celular_input.text(),
                'remision': self.remision_input.text()
            }

            # Realizar la solicitud al backend para guardar el paciente
            url = "http://127.0.0.1:5000/paciente/nuevo"
            response = requests.post(url, json=data)

            # Mostrar mensaje de éxito o error según la respuesta del servidor
            if response.status_code == 201:
                QMessageBox.information(self, "Éxito", "Paciente registrado exitosamente.")
            else:
                try:
                    error_message = response.json().get('error', 'Error desconocido')
                except requests.exceptions.JSONDecodeError:
                    error_message = f"Error no esperado: {response.text}"

                QMessageBox.warning(self, "Error", f"Error al registrar el paciente: {error_message}")

        except ValueError as ve:
            QMessageBox.warning(self, "Error de entrada", f"Error en los datos ingresados: {str(ve)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {str(e)}")

