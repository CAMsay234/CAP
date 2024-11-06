from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
import threading

db = SQLAlchemy()

# Bandera de control para detener el servidor Flask
stop_event = threading.Event()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Definir una ruta de prueba
    @app.route('/')
    def home():
        return "¡Bienvenido a la API!"

    # Ruta para cerrar el servidor
    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        func = request.environ.get('werkzeug.server.shutdown')
        if func:
            func()
        return 'Servidor cerrándose...'

    # Inicializar la base de datos
    db.init_app(app)

    # Importar los modelos para que SQLAlchemy los registre
    with app.app_context():
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
        from app.models.usuario import Usuario
        from app.models.conversion import Conversion
        # Agrega todas las importaciones de modelos necesarias

    # Registrar los blueprints de las rutas
    from app.routes.paciente import pacientes_bp
    app.register_blueprint(pacientes_bp)
    from app.routes.pruebas import pruebas_bp
    app.register_blueprint(pruebas_bp)
    from app.routes.sub_pruebas import subpruebas_bp
    app.register_blueprint(subpruebas_bp)
    from app.routes.areas import areas_bp
    app.register_blueprint(areas_bp)
    from app.routes.comentarios_clinicos import comentarios_bp
    app.register_blueprint(comentarios_bp)
    from app.routes.historia_clinica import historias_bp
    app.register_blueprint(historias_bp)
    from app.routes.nivel_escolaridad import nivel_escolaridad_bp
    app.register_blueprint(nivel_escolaridad_bp)
    from app.routes.estado_mental import estado_mental_bp
    app.register_blueprint(estado_mental_bp)
    from app.routes.evaluacion_neuropsicologica import evaluaciones_bp
    app.register_blueprint(evaluaciones_bp)
    from app.routes.hipotesis import hipotesis_bp
    app.register_blueprint(hipotesis_bp)
    from app.routes.diagnostico import diagnosticos_bp
    app.register_blueprint(diagnosticos_bp)
    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from app.routes.seguimiento import seguimientos_bp
    app.register_blueprint(seguimientos_bp)
    from app.routes.conversion import conversiones_bp
    app.register_blueprint(conversiones_bp)

    return app