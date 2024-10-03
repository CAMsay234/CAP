from flask import Blueprint, jsonify, request
from app import db
from app.models.nivel_escolaridad import NivelEscolaridad

# Definir el blueprint para las rutas relacionadas con "nivel_escolaridad"
nivel_escolaridad_bp = Blueprint('nivel_escolaridad', __name__)

# Crear un nuevo nivel de escolaridad (POST)
@nivel_escolaridad_bp.route('/niveles_escolaridad', methods=['POST'])
def crear_nivel_escolaridad():
    data = request.get_json()  # Obtener los datos en formato JSON
    descripcion = data.get('descripcion')

    if not descripcion:
        return jsonify({"error": "La descripción es obligatoria"}), 400

    nuevo_nivel = NivelEscolaridad(descripcion=descripcion)

    try:
        db.session.add(nuevo_nivel)
        db.session.commit()
        return jsonify({"message": "Nivel de escolaridad creado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Obtener todos los niveles de escolaridad (GET)
@nivel_escolaridad_bp.route('/niveles_escolaridad', methods=['GET'])
def obtener_niveles_escolaridad():
    niveles = NivelEscolaridad.query.all()
    niveles_list = [{"id": n.id, "descripcion": n.descripcion} for n in niveles]
    return jsonify(niveles_list), 200

# Obtener un nivel de escolaridad por ID (GET)
@nivel_escolaridad_bp.route('/niveles_escolaridad/<int:id>', methods=['GET'])
def obtener_nivel_escolaridad(id):
    nivel = NivelEscolaridad.query.get(id)
    if nivel:
        return jsonify({"id": nivel.id, "descripcion": nivel.descripcion}), 200
    else:
        return jsonify({"error": "Nivel de escolaridad no encontrado"}), 404

# Actualizar un nivel de escolaridad por ID (PUT)
@nivel_escolaridad_bp.route('/niveles_escolaridad/<int:id>', methods=['PUT'])
def actualizar_nivel_escolaridad(id):
    nivel = NivelEscolaridad.query.get(id)
    if not nivel:
        return jsonify({"error": "Nivel de escolaridad no encontrado"}), 404

    data = request.get_json()
    descripcion = data.get('descripcion')

    if not descripcion:
        return jsonify({"error": "La descripción es obligatoria"}), 400

    nivel.descripcion = descripcion
    try:
        db.session.commit()
        return jsonify({"message": "Nivel de escolaridad actualizado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar un nivel de escolaridad por ID (DELETE)
@nivel_escolaridad_bp.route('/niveles_escolaridad/<int:id>', methods=['DELETE'])
def eliminar_nivel_escolaridad(id):
    nivel = NivelEscolaridad.query.get(id)
    if not nivel:
        return jsonify({"error": "Nivel de escolaridad no encontrado"}), 404

    try:
        db.session.delete(nivel)
        db.session.commit()
        return jsonify({"message": "Nivel de escolaridad eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500