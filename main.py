import sys
from multiprocessing import Process
from PyQt5.QtWidgets import QApplication
from app import create_app
from gui.main_window import LoginWindow

def run_flask():
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)  # Ejecuta Flask sin intentar apagarlo con shutdown

def run_pyqt():
    app = QApplication(sys.argv)
    ventana = LoginWindow()
    ventana.showFullScreen()  # Mostrar la ventana en pantalla completa
    app.exec_()

if __name__ == "__main__":
    # Crear procesos para Flask y PyQt
    flask_process = Process(target=run_flask)
    pyqt_process = Process(target=run_pyqt)

    # Iniciar ambos procesos
    flask_process.start()
    pyqt_process.start()

    try:
        pyqt_process.join()  # Mantener PyQt en ejecución hasta que se cierre la ventana
    except KeyboardInterrupt:
        print("Cerrando aplicación...")
    finally:
        flask_process.terminate()  # Forzar la terminación de Flask
        flask_process.join()  # Asegurarse de que Flask ha terminado antes de salir
