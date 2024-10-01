from app import create_app, db
from sqlalchemy import inspect

app = create_app()

def create_tables_if_needed():
    """Crea las tablas solo si no existen."""
    inspector = inspect(db.engine)
    existing_tables = inspector.get_table_names()  # Obtiene la lista de tablas existentes en la base de datos

    # Lista de todas las tablas que deberían existir según los modelos definidos
    required_tables = ['nivel_escolaridad', 'pruebas', 'sub_pruebas', 'pacientes', 'historias_clinicas', 'estado_mental', 
                       'areas', 'evaluaciones_neuropsicologicas', 'hipotesis', 'diagnosticos', 'seguimientos']

    missing_tables = [table for table in required_tables if table not in existing_tables]

    if missing_tables:
        print(f"Creando las siguientes tablas: {', '.join(missing_tables)}")
        db.create_all()  # Esto intentará crear todas las tablas faltantes
    else:
        print("La base de datos ya tiene todas las tablas.")

if __name__ == '__main__':
    with app.app_context():
        create_tables_if_needed()  # Verifica si es necesario crear las tablas
    app.run(debug=True)


