import sys
import os
import requests
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QWidget, QScrollArea, QFormLayout, QSpacerItem, QSizePolicy, QDialog
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class AreasWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()
        self.paciente_seleccionado = paciente_seleccionado
        self.setWindowTitle("Áreas")
        self.setFixedSize(800, 500)

        # Mostrar el paciente seleccionado
        label = QLabel(f"Paciente: {self.paciente_seleccionado['nombre']}")
        label_codigo = QLabel(f"Codigo: {self.paciente_seleccionado['codigo']}")
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(label_codigo)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
