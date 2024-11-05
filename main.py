import threading
from app import create_app
from PyQt5.QtWidgets import QApplication
from gui.main_window import LoginWindow  # Asegúrate de que esta importación sea correcta
from gui.registro import RegisterWindow  # Asegúrate de que esta importación sea correcta
from datetime import timedelta
import sys

def run_flask():
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def run_pyqt():
    app = QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.showFullScreen()  # Mostrar la ventana en pantalla completa
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Iniciar el servidor Flask en un hilo separado
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Iniciar la aplicación PyQt5 en el hilo principal
    run_pyqt()