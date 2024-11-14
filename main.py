import sys
from threading import Thread
from PyQt5.QtWidgets import QApplication
from app import create_app
from gui.main_window import LoginWindow
import time

def run_flask():
    print("Iniciando el servidor Flask...")
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def run_pyqt():
    print("Iniciando la aplicación PyQt...")
    app = QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.showFullScreen()
    app.exec_()

if __name__ == "__main__":
    try:
        # Iniciar el servidor Flask en un hilo separado
        flask_thread = Thread(target=run_flask)
        flask_thread.daemon = True  # Asegurar que el hilo termine con la aplicación principal
        flask_thread.start()

        # Esperar un tiempo para asegurar que Flask inicie antes de PyQt
        time.sleep(3)

        # Ejecutar PyQt en el hilo principal
        run_pyqt()

    except KeyboardInterrupt:
        print("Cerrando aplicación...")

    finally:
        print("Aplicación terminada.")
