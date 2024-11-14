import logging
from app import create_app, db  # Asegúrate de importar db correctamente
from app.config.setup_db import create_tables_and_indices  # Asegúrate de importar correctamente
from flask import session, request, current_app, make_response, jsonify
from datetime import timedelta
 
# Configuración de logging para registrar eventos
logging.basicConfig(level=logging.INFO)
 
app = create_app()
 
# Ruta de login para iniciar sesión y generar una cookie de sesión
@app.route('/login', methods=['POST'])
def login():
    data = request.json  # Capturar los datos enviados en la solicitud POST
    username = data.get('username')
    password = data.get('password')
 
    # Validación simple de credenciales (puedes reemplazar esto con tu lógica)
    if username == 'luisaflorezm' and password == '1000413791':
        session['user'] = username  # Guardar el usuario en la sesión
        session.permanent = True  # Hacer la sesión permanente
 
        response = jsonify({"message": "Login exitoso"})
        response.status_code = 200
        return response
    else:
        return jsonify({"message": "Usuario o contraseña incorrectos"}), 401
 
# Configurar la seguridad de las cookies de sesión
@app.after_request
def aplicar_seguridad(response):
    """Configura las cookies de sesión como seguras y HTTPOnly."""
    session_cookie_name = current_app.config.get('SESSION_COOKIE_NAME', 'session')  # Obtener el nombre de la cookie
    session_cookie = request.cookies.get(session_cookie_name)
 
    if session_cookie:
        response.set_cookie(
            session_cookie_name,
            session_cookie,
            secure=False,  # Cambia a True si usas HTTPS en producción
            httponly=True,  # Evita que JavaScript acceda a las cookies
            samesite='Strict'  # Protege contra ataques CSRF
        )
    return response
 
# Garantizar que se elimine la sesión de base de datos al final de cada solicitud
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()
   
if __name__ == "__main__":
    # Crear las tablas e índices necesarios en la base de datos
    create_tables_and_indices()
 
    # Configuración de la sesión
    app.secret_key = 'mi_clave_secreta'  # Clave secreta para la sesión
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)  # La sesión expira en 10 minutos
    app.config['SESSION_COOKIE_NAME'] = 'session'  # Establece el nombre de la cookie de sesión
 
    # Iniciar la aplicación
    app.run(host='127.0.0.1', port=5000, debug=True)