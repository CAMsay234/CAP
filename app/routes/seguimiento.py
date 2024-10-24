from flask import Blueprint, jsonify, request
from app import db
from app.models.seguimiento import Seguimiento, get_next_num_seccion
from datetime import datetime

# Definir el blueprint para las rutas relacionadas con "seguimientos"
seguimientos_bp = Blueprint('seguimientos', __name__)

# Crear un nuevo seguimiento (POST)
@seguimientos_bp.route('/seguimientos', methods=['POST'])
def crear_seguimiento():
    data = request.get_json()  # Obtener los datos en formato JSON
    codigo_hc = data.get('codigo_hc')
    fecha_str = data.get('fecha')  # La fecha viene como string
    descripcion = data.get('descripcion')

    if not codigo_hc or not fecha_str or not descripcion:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    try:
        # Convertir la fecha de string a datetime.date
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        num_seccion = get_next_num_seccion(codigo_hc)

        nuevo_seguimiento = Seguimiento(
            codigo_hc=codigo_hc,
            num_seccion=num_seccion,
            fecha=fecha,
            descripcion=descripcion
        )

        db.session.add(nuevo_seguimiento)
        db.session.commit()
        return jsonify({"message": "Seguimiento creado exitosamente", "num_seccion": num_seccion}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Obtener todos los seguimientos (GET)
@seguimientos_bp.route('/seguimientos', methods=['GET'])
def obtener_seguimientos():
    seguimientos = Seguimiento.query.all()
    seguimientos_list = [{
        "codigo_hc": s.codigo_hc,
        "num_seccion": s.num_seccion,
        "fecha": s.fecha.strftime('%Y-%m-%d'),  # Convertir fecha a string para el JSON
        "descripcion": s.descripcion
    } for s in seguimientos]
    return jsonify(seguimientos_list), 200

# Obtener un seguimiento por clave compuesta (GET)
@seguimientos_bp.route('/seguimientos/<int:codigo_hc>/<int:num_seccion>', methods=['GET'])
def obtener_seguimiento(codigo_hc, num_seccion):
    seguimiento = Seguimiento.query.get((codigo_hc, num_seccion))
    if seguimiento:
        return jsonify({
            "codigo_hc": seguimiento.codigo_hc,
            "num_seccion": seguimiento.num_seccion,
            "fecha": seguimiento.fecha.strftime('%Y-%m-%d'),  # Convertir fecha a string
            "descripcion": seguimiento.descripcion
        }), 200
    else:
        return jsonify({"error": "Seguimiento no encontrado"}), 404

# Actualizar un seguimiento por clave compuesta (PUT)
@seguimientos_bp.route('/seguimientos/<int:codigo_hc>/<int:num_seccion>', methods=['PUT'])
def actualizar_seguimiento(codigo_hc, num_seccion):
    seguimiento = Seguimiento.query.get((codigo_hc, num_seccion))
    if not seguimiento:
        return jsonify({"error": "Seguimiento no encontrado"}), 404

    data = request.get_json()

    # Validar y convertir la fecha solo si está presente en el request
    fecha_str = data.get('fecha')
    if fecha_str:
        try:
            seguimiento.fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido"}), 400

    seguimiento.descripcion = data.get('descripcion', seguimiento.descripcion)

    try:
        db.session.commit()
        return jsonify({"message": "Seguimiento actualizado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar un seguimiento por clave compuesta (DELETE)
@seguimientos_bp.route('/seguimientos/<int:codigo_hc>/<int:num_seccion>', methods=['DELETE'])
def eliminar_seguimiento(codigo_hc, num_seccion):
    seguimiento = Seguimiento.query.get((codigo_hc, num_seccion))
    if not seguimiento:
        return jsonify({"error": "Seguimiento no encontrado"}), 404

    try:
        db.session.delete(seguimiento)
        db.session.commit()
        return jsonify({"message": "Seguimiento eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
