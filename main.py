import sys
import time
from multiprocessing import Process
from PyQt5.QtWidgets import QApplication
from app import create_app
from gui.main_window import LoginWindow

def run_flask():
    print("Iniciando el servidor Flask...")
    app = create_app()
    try:
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        print(f"Error al iniciar Flask: {e}")

def run_pyqt():
    # Esperar un momento para asegurarse de que el servidor Flask esté listo
    time.sleep(5)
    print("Iniciando la aplicación PyQt...")
    app = QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    print("Iniciando la aplicación principal...")

    # Crear proceso para Flask
    flask_process = Process(target=run_flask)
    flask_process.start()

    try:
        # Ejecutar PyQt en el proceso principal
        run_pyqt()
    except KeyboardInterrupt:
        print("Cerrando aplicación...")
    finally:
        # Terminar el proceso Flask si aún está corriendo
        flask_process.terminate()
        flask_process.join()
        print("Aplicación terminada.")
