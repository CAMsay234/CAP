import os
from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy, QGridLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class EvaluacionNeuropsicologicaWindow(QMainWindow):
    def __init__(self,paciente_seleccionado):
        super().__init__()

        self.paciente_seleccionado = paciente_seleccionado
        # Configurar la ventana
        self.setWindowTitle(f"Evaluación Neuropsicológica de {self.paciente_seleccionado['nombre']}")
        self.showMaximized()  # Abrir la ventana maximizada
        self.setStyleSheet("background-color: white;")  # Fondo blanco

        # Crear el layout principal
        main_layout = QVBoxLayout()

        # Crear un layout horizontal para la barra azul con el logo
        header_layout = QHBoxLayout()

        # Crear un widget que actúe como barra azul
        header_background = QWidget()
        header_background.setStyleSheet("background-color: #005BBB;")
        header_background_layout = QHBoxLayout(header_background)
        header_background_layout.setContentsMargins(0, 0, 0, 0)

        # Logo de UPB
        image_path = os.path.join(os.path.dirname(__file__), 'src', 'upb.png')
        self.logo = QLabel(self)
        pixmap = QPixmap(image_path).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # Ajustar el tamaño del logo
        self.logo.setPixmap(pixmap)
        header_background_layout.addWidget(self.logo, alignment=Qt.AlignLeft)

        # Campos de Código y Nombre del paciente
        self.label_codigo = QLabel(f"Código: {self.paciente_seleccionado['codigo_hc']}")
        self.label_codigo.setFont(QFont('Arial', 14))
        self.input_codigo = QLineEdit()
        self.input_codigo.setFixedWidth(100)

        self.label_nombre = QLabel(f"Nombre paciente: {self.paciente_seleccionado['nombre']}")
        self.label_nombre.setFont(QFont('Arial', 14))
        self.input_nombre = QLineEdit()
        self.input_nombre.setFixedWidth(300)

        # Añadir los campos de código y nombre al banner
        header_background_layout.addWidget(self.label_codigo)
        header_background_layout.addWidget(self.input_codigo)
        header_background_layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum))
        header_background_layout.addWidget(self.label_nombre)
        header_background_layout.addWidget(self.input_nombre)

        # Botones de "Actualizar Datos Personales" y "Actualizar Historia Clínica" en el banner azul
        self.btn_actualizar_datos = QPushButton("ACTUALIZAR DATOS PERSONALES")
        self.btn_actualizar_datos.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #005BBB;
                font-size: 14px;
                padding: 10px 20px;
                border-radius: 5px;
                min-width: 250px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.btn_actualizar_historia = QPushButton("ACTUALIZAR HISTORIA CLÍNICA")
        self.btn_actualizar_historia.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #005BBB;
                font-size: 14px;
                padding: 10px 20px;
                border-radius: 5px;
                min-width: 250px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)

        # Conectar los botones con las funciones para abrir las ventanas
        self.btn_actualizar_datos.clicked.connect(self.abrir_ventana_registrar_paciente)
        self.btn_actualizar_historia.clicked.connect(self.abrir_ventana_historia_clinica)

        # Agregar los botones al layout del banner
        header_background_layout.addWidget(self.btn_actualizar_datos, alignment=Qt.AlignLeft)
        header_background_layout.addWidget(self.btn_actualizar_historia, alignment=Qt.AlignLeft)

        # Añadir el layout del fondo azul (con el logo y los botones) al header
        header_layout.addWidget(header_background)

        # Añadir el layout del header al layout principal
        main_layout.addLayout(header_layout)

        # Crear un espaciador grande debajo de la imagen
        main_layout.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Título de la sección
        self.label_titulo = QLabel("EVALUACIÓN NEUROPSICOLÓGICA")
        self.label_titulo.setFont(QFont('Arial', 20, QFont.Bold))
        self.label_titulo.setAlignment(Qt.AlignCenter)
        self.label_titulo.setStyleSheet("color: #005BBB;")
        main_layout.addWidget(self.label_titulo)

        # Layout para los botones de evaluación
        evaluation_grid = QGridLayout()

        # Crear botones y conectarlos con las funciones de abrir ventanas
        self.buttons = {
            "ATENCIÓN Y CONCENTRACIÓN": self.abrir_ventana_atencion_concentracion,
            "PROCESOS PERCEPTUALES": self.abrir_ventana_procesos_perceptuales,
            "FUNCIONES NEUROCOGNITIVAS": self.abrir_ventana_funciones_neurocognitivas,
            "LENGUAJE": self.abrir_ventana_lenguaje,
            "PROCESOS DE MEMORIA": self.abrir_ventana_memoria,
            "FUNCIÓN EJECUTIVA": self.abrir_ventana_funcion_ejecutiva,
            "CAPACIDAD INTELECTUAL": self.abrir_ventana_capacidad_intelectual
        }

        # Estilo para los botones de evaluación
        button_style = """
            QPushButton {
                background-color: #F0F0F0;
                color: #005BBB;
                font-size: 18px;
                padding: 20px;
                border-radius: 10px;
                border: 2px solid #005BBB;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """

        # Agregar botones al grid
        # Reorganizamos las posiciones para que "CAPACIDAD INTELECTUAL" esté debajo de "PROCESOS DE MEMORIA"
        positions = {
            "ATENCIÓN Y CONCENTRACIÓN": (0, 0),
            "PROCESOS PERCEPTUALES": (0, 1),
            "FUNCIONES NEUROCOGNITIVAS": (0, 2),
            "LENGUAJE": (1, 0),
            "PROCESOS DE MEMORIA": (1, 1),
            "FUNCIÓN EJECUTIVA": (1, 2),
            "CAPACIDAD INTELECTUAL": (2, 1),  # Mover "CAPACIDAD INTELECTUAL" debajo de "PROCESOS DE MEMORIA"
        }

# Añadimos los botones al grid usando las posiciones especificadas
        for button_name, position in positions.items():
            button = QPushButton(button_name)
            button.setStyleSheet(button_style)
            button.clicked.connect(self.buttons[button_name])  # Conectar el clic con la función correspondiente
            evaluation_grid.addWidget(button, *position)

        # Agregar grid al layout principal
        main_layout.addLayout(evaluation_grid)

        # Espaciador entre grid y los botones inferiores
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Layout para los botones inferiores
        bottom_buttons_layout = QHBoxLayout()

        # Botones "Seguimiento", "Diagnóstico" y "Visualizaciones" en azul
        self.btn_seguimiento = QPushButton("SEGUIMIENTO")
        self.btn_seguimiento.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                font-size: 16px;
                border: none;
                font-weight: bold;
                padding: 10px;
            }
        """)
        self.btn_diagnostico = QPushButton("DIAGNÓSTICO")
        self.btn_diagnostico.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                font-size: 16px;
                border: none;
                font-weight: bold;
                padding: 10px;
            }
        """)
        self.btn_visualizaciones = QPushButton("VISUALIZACIONES")
        self.btn_visualizaciones.setStyleSheet("""
            QPushButton {
                background-color: #005BBB;
                color: white;
                font-size: 16px;
                border: none;
                font-weight: bold;
                padding: 10px;
            }
        """)

        # Agregar los botones inferiores al layout
        bottom_buttons_layout.addWidget(self.btn_seguimiento, alignment=Qt.AlignCenter)
        bottom_buttons_layout.addWidget(self.btn_diagnostico, alignment=Qt.AlignCenter)
        bottom_buttons_layout.addWidget(self.btn_visualizaciones, alignment=Qt.AlignCenter)

        main_layout.addLayout(bottom_buttons_layout)

        # Crear un widget central para contener los elementos
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

    # Funciones para abrir ventanas específicas
    def abrir_ventana_registrar_paciente(self):
        from registrar_paciente import RegistrarPacienteWindow
        self.ventana_registrar = RegistrarPacienteWindow()
        self.ventana_registrar.show()
        self.close()

    def abrir_ventana_historia_clinica(self):
          if hasattr(self, 'paciente_seleccionado'):
            from historia_clinica import HistoriaClinicaWindow
            self.historia_clinica_window = HistoriaClinicaWindow(self.paciente_seleccionado)
            self.historia_clinica_window.show()
            self.close()

    def abrir_ventana_atencion_concentracion(self):
        from prueba_atencion_concentracion import PruebaAtencionConcentracionWindow
        self.ventana_atencion = PruebaAtencionConcentracionWindow()
        self.ventana_atencion.show()
        self.close()

    def abrir_ventana_procesos_perceptuales(self):
        from prueba_procesos_perceptuales import PruebaProcesosPerceptualesWindow
        self.ventana_procesos = PruebaProcesosPerceptualesWindow()
        self.ventana_procesos.show()
        self.close()

    def abrir_ventana_funciones_neurocognitivas(self):
        from prueba_funciones_neurocognitivas import PruebaFuncionesNeurocognitivasWindow
        self.ventana_neurocognitivas = PruebaFuncionesNeurocognitivasWindow()
        self.ventana_neurocognitivas.show()
        self.close()

    def abrir_ventana_lenguaje(self):
        from prueba_lenguaje import PruebaLenguajeWindow
        self.ventana_lenguaje = PruebaLenguajeWindow()
        self.ventana_lenguaje.show()
        self.close()

    def abrir_ventana_memoria(self):
        from prueba_procesos_memoria import PruebaProcesosMemoriaWindow
        self.ventana_memoria = PruebaProcesosMemoriaWindow()
        self.ventana_memoria.show()
        self.close()

    def abrir_ventana_funcion_ejecutiva(self):
        from prueba_funcion_ejecutiva import PruebaFuncionEjecutivaWindow
        self.ventana_funcion_ejecutiva = PruebaFuncionEjecutivaWindow()
        self.ventana_funcion_ejecutiva.show()
        self.close()

    def abrir_ventana_capacidad_intelectual(self):
        from prueba_capacidad_intelectual import PruebaCapacidadIntelectualWindow
        self.ventana_capacidad_intelectual = PruebaCapacidadIntelectualWindow()
        self.ventana_capacidad_intelectual.show()
        self.close()


      
# Ejecutar la aplicación
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)

    ventana = EvaluacionNeuropsicologicaWindow()
    ventana.show()

    sys.exit(app.exec_())

