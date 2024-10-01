from flask import Blueprint, jsonify, request
from app import db
from app.models.area import Area

# Definir el blueprint para las rutas relacionadas con "areas"
areas_bp = Blueprint('areas', __name__)

# Crear un nuevo registro de área (POST)
@areas_bp.route('/areas', methods=['POST'])
def crear_area():
    data = request.get_json()  # Obtener los datos en formato JSON
    codigo_hc = data.get('codigo_hc')
    familiar = data.get('familiar')
    pareja = data.get('pareja')
    social = data.get('social')
    laboral = data.get('laboral')

    if not codigo_hc or not familiar or not pareja or not social or not laboral:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    nueva_area = Area(
        codigo_hc=codigo_hc,
        familiar=familiar,
        pareja=pareja,
        social=social,
        laboral=laboral
    )

    try:
        db.session.add(nueva_area)
        db.session.commit()
        return jsonify({"message": "Área creada exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Obtener todas las áreas (GET)
@areas_bp.route('/areas', methods=['GET'])
def obtener_areas():
    areas = Area.query.all()
    areas_list = [{"codigo_hc": a.codigo_hc, "familiar": a.familiar, "pareja": a.pareja, "social": a.social, "laboral": a.laboral} for a in areas]
    return jsonify(areas_list), 200

# Obtener una área por código_hc (GET)
@areas_bp.route('/areas/<int:codigo_hc>', methods=['GET'])
def obtener_area(codigo_hc):
    area = Area.query.get(codigo_hc)
    if area:
        return jsonify({
            "codigo_hc": area.codigo_hc,
            "familiar": area.familiar,
            "pareja": area.pareja,
            "social": area.social,
            "laboral": area.laboral
        }), 200
    else:
        return jsonify({"error": "Área no encontrada"}), 404

# Actualizar una área por código_hc (PUT)
@areas_bp.route('/areas/<int:codigo_hc>', methods=['PUT'])
def actualizar_area(codigo_hc):
    area = Area.query.get(codigo_hc)
    if not area:
        return jsonify({"error": "Área no encontrada"}), 404

    data = request.get_json()
    familiar = data.get('familiar')
    pareja = data.get('pareja')
    social = data.get('social')
    laboral = data.get('laboral')

    if not familiar or not pareja or not social or not laboral:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    area.familiar = familiar
    area.pareja = pareja
    area.social = social
    area.laboral = laboral

    try:
        db.session.commit()
        return jsonify({"message": "Área actualizada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar una área por código_hc (DELETE)
@areas_bp.route('/areas/<int:codigo_hc>', methods=['DELETE'])
def eliminar_area(codigo_hc):
    area = Area.query.get(codigo_hc)
    if not area:
        return jsonify({"error": "Área no encontrada"}), 404

    try:
        db.session.delete(area)
        db.session.commit()
        return jsonify({"message": "Área eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500