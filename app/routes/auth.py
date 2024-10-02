from flask import Blueprint, request, jsonify
from app import db
from app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    if Usuario.query.filter_by(username=username).first() or Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "El nombre de usuario o email ya existe"}), 400

    nuevo_usuario = Usuario(username=username, email=email)
    nuevo_usuario.set_password(password)

    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"message": "Usuario registrado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    usuario = Usuario.query.filter_by(username=username).first()

    if not usuario or not usuario.check_password(password):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    return jsonify({"message": f"Bienvenido {usuario.username}"}), 200
