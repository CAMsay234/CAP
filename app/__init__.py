from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar la base de datos
    db.init_app(app)

    # Importar los modelos para que SQLAlchemy los registre
    from app.models.nivel_escolaridad import NivelEscolaridad
    from app.models.prueba import Prueba
    from app.models.sub_prueba import SubPrueba
    from app.models.paciente import Paciente
    from app.models.historia_clinica import Historia_Clinica
    from app.models.evaluacion_neuropsicologica import EvaluacionNeuropsicologica
    from app.models.area import Area
    from app.models.estado_mental import EstadoMental
    from app.models.comentarios_clinicos import Comentarios
    from app.models.hipotesis import Hipotesis
    from app.models.diagnostico import Diagnostico
    from app.models.seguimiento import Seguimiento
    # Agrega todas las importaciones de modelos necesarias

    # Registrar los blueprints de las rutas
    from app.routes.paciente import pacientes_bp
    app.register_blueprint(pacientes_bp)
    from app.routes.pruebas import pruebas_bp
    app.register_blueprint(pruebas_bp)
    from app.routes.sub_pruebas import subpruebas_bp
    app.register_blueprint(subpruebas_bp)

    return app


