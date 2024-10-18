import logging
from sqlalchemy import inspect, text
from app import create_app, db

def create_tables_and_indices():
    """Crea las tablas solo si no existen y crea índices necesarios."""
    app = create_app()
    with app.app_context():
        try:
            inspector = inspect(db.engine)
            existing_tables = inspector.get_table_names()  # Obtiene la lista de tablas existentes en la base de datos

            # Lista de todas las tablas que deberían existir según los modelos definidos
            required_tables = [
                'nivel_escolaridad', 'pruebas', 'sub_pruebas', 'pacientes', 
                'historias_clinicas', 'estado_mental', 'areas', 
                'evaluaciones_neuropsicologicas', 'hipotesis', 'diagnosticos', 'seguimientos', 'comentarios_clinicos', 'usuarios',
                'conversiones'
            ]

            # Verifica si alguna tabla falta
            missing_tables = [table for table in required_tables if table not in existing_tables]

            if missing_tables:
                logging.info(f"Creando las siguientes tablas: {', '.join(missing_tables)}")
                db.create_all()  # Crea todas las tablas faltantes
            else:
                logging.info("La base de datos ya tiene todas las tablas.")

            # Crear índices necesarios
            with db.engine.connect() as connection:
                connection.execute(text("CREATE INDEX IF NOT EXISTS idx_codigo_hc ON evaluaciones_neuropsicologicas(codigo_hc);"))
                connection.execute(text("CREATE INDEX IF NOT EXISTS idx_id_prueba ON evaluaciones_neuropsicologicas(id_prueba);"))
                connection.execute(text("CREATE INDEX IF NOT EXISTS idx_id_subprueba ON evaluaciones_neuropsicologicas(id_subprueba);"))
                connection.execute(text("CREATE INDEX IF NOT EXISTS idx_codigo_hc_id_prueba_id_subprueba ON evaluaciones_neuropsicologicas(codigo_hc, id_prueba, id_subprueba);"))
                connection.execute(text("CREATE INDEX IF NOT EXISTS idx_codigo_hc_historia_clinica ON historias_clinicas(codigo_hc);"))
                logging.info("Índices creados exitosamente.")
        except Exception as e:
            logging.error(f"Error al crear tablas o índices: {e}")

if __name__ == "__main__":
    create_tables_and_indices()