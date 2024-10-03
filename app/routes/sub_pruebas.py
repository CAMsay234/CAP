from flask import Blueprint, jsonify, request
from app import db
from app.models.sub_prueba import SubPrueba

# Definir el blueprint para las rutas relacionadas con "sub_pruebas"
subpruebas_bp = Blueprint('subpruebas', __name__)

# Crear una nueva sub_prueba (POST)
@subpruebas_bp.route('/subpruebas', methods=['POST'])
def crear_subprueba():
    data = request.get_json()  # Obtener los datos en formato JSON
    nombre = data.get('nombre')
    id_prueba = data.get('id_prueba')

    if not nombre or not id_prueba:
        return jsonify({"error": "El nombre y id_prueba son obligatorios"}), 400

    nueva_subprueba = SubPrueba(nombre=nombre, id_prueba=id_prueba)

    try:
        db.session.add(nueva_subprueba)
        db.session.commit()
        return jsonify({"message": "SubPrueba creada exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Obtener todas las sub_pruebas (GET)
@subpruebas_bp.route('/subpruebas', methods=['GET'])
def obtener_subpruebas():
    subpruebas = SubPrueba.query.all()
    subpruebas_list = [{"id": sp.id, "id_prueba": sp.id_prueba, "nombre": sp.nombre} for sp in subpruebas]
    return jsonify(subpruebas_list), 200

# Obtener una sub_prueba por ID (GET)
@subpruebas_bp.route('/subpruebas/<int:id>', methods=['GET'])
def obtener_subprueba(id):
    subprueba = SubPrueba.query.get(id)
    if subprueba:
        return jsonify({"id": subprueba.id, "id_prueba": subprueba.id_prueba, "nombre": subprueba.nombre}), 200
    else:
        return jsonify({"error": "SubPrueba no encontrada"}), 404

# Actualizar una sub_prueba por ID (PUT)
@subpruebas_bp.route('/subpruebas/<int:id>', methods=['PUT'])
def actualizar_subprueba(id):
    subprueba = SubPrueba.query.get(id)
    if not subprueba:
        return jsonify({"error": "SubPrueba no encontrada"}), 404

    data = request.get_json()
    nombre = data.get('nombre')
    id_prueba = data.get('id_prueba')

    if not nombre or not id_prueba:
        return jsonify({"error": "El nombre y id_prueba son obligatorios"}), 400

    subprueba.nombre = nombre
    subprueba.id_prueba = id_prueba
    try:
        db.session.commit()
        return jsonify({"message": "SubPrueba actualizada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar una sub_prueba por ID (DELETE)
@subpruebas_bp.route('/subpruebas/<int:id>', methods=['DELETE'])
def eliminar_subprueba(id):
    subprueba = SubPrueba.query.get(id)
    if not subprueba:
        return jsonify({"error": "SubPrueba no encontrada"}), 404

    try:
        db.session.delete(subprueba)
        db.session.commit()
        return jsonify({"message": "SubPrueba eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
