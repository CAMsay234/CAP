import logging
from app import create_app, db
from sqlalchemy import inspect

# Configuración de logging para registrar eventos
logging.basicConfig(level=logging.INFO)

app = create_app()

def create_tables_if_needed():
    """Crea las tablas solo si no existen."""
    try:
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()  # Obtiene la lista de tablas existentes en la base de datos

        # Lista de todas las tablas que deberían existir según los modelos definidos
        required_tables = [
            'nivel_escolaridad', 'pruebas', 'sub_pruebas', 'pacientes', 
            'historias_clinicas', 'estado_mental', 'areas', 
            'evaluaciones_neuropsicologicas', 'hipotesis', 'diagnosticos', 'seguimientos', 'comentarios_clinicos', 'usuarios'
        ]

        # Verifica si alguna tabla falta
        missing_tables = [table for table in required_tables if table not in existing_tables]

        if missing_tables:
            logging.info(f"Creando las siguientes tablas: {', '.join(missing_tables)}")
            db.create_all()  # Crea todas las tablas faltantes
        else:
            logging.info("La base de datos ya tiene todas las tablas.")
    except Exception as e:
        logging.error(f"Error creando las tablas: {str(e)}")

# Esta función garantiza que se elimine la sesión de base de datos al final de cada solicitud
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

if __name__ == '__main__':
    with app.app_context():
        create_tables_if_needed()  # Verifica si es necesario crear las tablas
    app.run(debug=app.config.get('DEBUG', False))  # Cambia el modo de debug según la configuración



