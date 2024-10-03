from flask import Blueprint, jsonify, request
from app import db
from app.models.prueba import Prueba

# Definir el blueprint para las rutas relacionadas con "pruebas"
pruebas_bp = Blueprint('pruebas', __name__)

# Crear una nueva prueba (POST)
@pruebas_bp.route('/pruebas', methods=['POST'])
def crear_prueba():
    data = request.get_json()  # Obtener los datos en formato JSON
    nombre = data.get('nombre')

    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    nueva_prueba = Prueba(nombre=nombre)

    try:
        db.session.add(nueva_prueba)
        db.session.commit()
        return jsonify({"message": "Prueba creada exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Obtener todas las pruebas (GET)
@pruebas_bp.route('/pruebas', methods=['GET'])
def obtener_pruebas():
    pruebas = Prueba.query.all()
    pruebas_list = [{"id": p.id, "nombre": p.nombre} for p in pruebas]
    return jsonify(pruebas_list), 200

# Obtener una prueba por ID (GET)
@pruebas_bp.route('/pruebas/<int:id>', methods=['GET'])
def obtener_prueba(id):
    prueba = Prueba.query.get(id)
    if prueba:
        return jsonify({"id": prueba.id, "nombre": prueba.nombre}), 200
    else:
        return jsonify({"error": "Prueba no encontrada"}), 404

# Actualizar una prueba por ID (PUT)
@pruebas_bp.route('/pruebas/<int:id>', methods=['PUT'])
def actualizar_prueba(id):
    prueba = Prueba.query.get(id)
    if not prueba:
        return jsonify({"error": "Prueba no encontrada"}), 404

    data = request.get_json()
    nombre = data.get('nombre')

    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    prueba.nombre = nombre
    try:
        db.session.commit()
        return jsonify({"message": "Prueba actualizada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar una prueba por ID (DELETE)
@pruebas_bp.route('/pruebas/<int:id>', methods=['DELETE'])
def eliminar_prueba(id):
    prueba = Prueba.query.get(id)
    if not prueba:
        return jsonify({"error": "Prueba no encontrada"}), 404

    try:
        db.session.delete(prueba)
        db.session.commit()
        return jsonify({"message": "Prueba eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
