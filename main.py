import sys
import threading
import requests  # Importar el módulo requests
import os
from PyQt5.QtWidgets import QApplication
from app import create_app, stop_event
from gui.main_window import LoginWindow

def run_flask():
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

def stop_flask_server():
    stop_event.set()
    # Realizar una solicitud al servidor para activar el cierre
    try:
        requests.post('http://127.0.0.1:5000/shutdown')
        sys.exit(0)
    except requests.exceptions.RequestException:
        pass

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    app = QApplication(sys.argv)
    main_window = LoginWindow()
    main_window.showFullScreen()
    
    app.exec_()

    stop_flask_server()
    flask_thread.join()
    sys.exit(0)  # Salir del script