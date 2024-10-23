import logging
from app import create_app, db  # Asegúrate de importar db correctamente
from app.config.setup_db import create_tables_and_indices  # Asegúrate de importar correctamente

# Configuración de logging para registrar eventos
logging.basicConfig(level=logging.INFO)

app = create_app()

# Esta función garantiza que se elimine la sesión de base de datos al final de cada solicitud
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == "__main__":
    create_tables_and_indices()
    app.run()