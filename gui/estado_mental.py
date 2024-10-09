import sys
import os
import requests
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QWidget, QScrollArea, QFormLayout, QSpacerItem, QSizePolicy, QDialog
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

class EstadoMentalWindow(QMainWindow):
    def __init__(self, paciente_seleccionado):
        super().__init__()
        self.paciente_seleccionado = paciente_seleccionado
        self.setWindowTitle("Estado Mental")
        self.setFixedSize(400, 300)

        # Mostrar el paciente seleccionado
        label = QLabel(f"Paciente: {self.paciente_seleccionado}")
        layout = QVBoxLayout()
        layout.addWidget(label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)