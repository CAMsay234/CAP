from flask import Blueprint, jsonify, request
from app import db
from app.models.hipotesis import Hipotesis

# Definir el blueprint para las rutas relacionadas con "hipotesis"
hipotesis_bp = Blueprint('hipotesis', __name__)

# Crear una nueva hipótesis (POST)
@hipotesis_bp.route('/hipotesis', methods=['POST'])
def crear_nueva_hipotesis():
    data = request.get_json()
    descripcion = data.get('descripcion')

    if not descripcion:
        return jsonify({"error": "La descripción es obligatoria"}), 400

    nueva_hipotesis = Hipotesis(descripcion=descripcion)

    try:
        db.session.add(nueva_hipotesis)
        db.session.commit()
        return jsonify({"message": "Hipótesis creada exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Obtener todas las hipótesis (GET)
@hipotesis_bp.route('/hipotesis', methods=['GET'])
def obtener_todas_las_hipotesis():
    hipotesis_list = Hipotesis.query.all()
    return jsonify([{"id": h.id, "descripcion": h.descripcion} for h in hipotesis_list]), 200

# Obtener una hipótesis por ID (GET)
@hipotesis_bp.route('/hipotesis/<int:id>', methods=['GET'])
def obtener_hipotesis_por_id(id):  # Pasar el ID como parámetro
    hipotesis = Hipotesis.query.get(id)
    if hipotesis:
        return jsonify({"id": hipotesis.id, "descripcion": hipotesis.descripcion}), 200
    else:
        return jsonify({"error": "Hipótesis no encontrada"}), 404

# Actualizar una hipótesis por ID (PUT)
@hipotesis_bp.route('/hipotesis/<int:id>', methods=['PUT'])
def actualizar_hipotesis(id):
    hipotesis = Hipotesis.query.get(id)
    if not hipotesis:
        return jsonify({"error": "Hipótesis no encontrada"}), 404

    data = request.get_json()
    nueva_descripcion = data.get('descripcion')

    if not nueva_descripcion:
        return jsonify({"error": "La descripción es obligatoria"}), 400

    hipotesis.descripcion = nueva_descripcion

    try:
        db.session.commit()
        return jsonify({"message": "Hipótesis actualizada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar una hipótesis por ID (DELETE)
@hipotesis_bp.route('/hipotesis/<int:id>', methods=['DELETE'])
def eliminar_hipotesis(id):
    hipotesis = Hipotesis.query.get(id)
    if not hipotesis:
        return jsonify({"error": "Hipótesis no encontrada"}), 404

    try:
        db.session.delete(hipotesis)
        db.session.commit()
        return jsonify({"message": "Hipótesis eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

