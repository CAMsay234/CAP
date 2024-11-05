from flask import Blueprint, jsonify, request
from app import db
from app.models.comentarios_clinicos import Comentarios

# Definir el blueprint para las rutas relacionadas con "comentarios_clinicos"
comentarios_bp = Blueprint('comentarios', __name__)

# Crear un nuevo comentario clínico (POST)
@comentarios_bp.route('/comentarios', methods=['POST'])
def crear_comentario():
    data = request.get_json()  # Obtener los datos en formato JSON
    codigo_hc = data.get('codigo_hc')
    id_prueba = data.get('id_prueba')
    tipo_comentario = data.get('tipo_comentario')
    comentario = data.get('comentario', "No aplica")  # Valor por defecto

    if not codigo_hc or not id_prueba or not tipo_comentario:
        return jsonify({"error": "Los campos codigo_hc, id_prueba, y tipo_comentario son obligatorios"}), 400

    nuevo_comentario = Comentarios(
        codigo_hc=codigo_hc,
        id_prueba=id_prueba,
        tipo_comentario=tipo_comentario,
        comentario=comentario
    )

    try:
        db.session.add(nuevo_comentario)
        db.session.commit()
        return jsonify({"message": "Comentario creado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Obtener todos los comentarios (GET)
@comentarios_bp.route('/comentarios', methods=['GET'])
def obtener_comentarios():
    comentarios = Comentarios.query.all()
    comentarios_list = [{
        "codigo_hc": c.codigo_hc, 
        "id_prueba": c.id_prueba, 
        "tipo_comentario": c.tipo_comentario, 
        "comentario": c.comentario
    } for c in comentarios]
    return jsonify(comentarios_list), 200

# Ruta para obtener todos los comentarios de un paciente y una prueba específicos
@comentarios_bp.route('/comentarios/<int:codigo_hc>/<int:id_prueba>', methods=['GET'])
def obtener_comentarios_por_prueba(codigo_hc, id_prueba):
    comentarios = Comentarios.query.filter_by(codigo_hc=codigo_hc, id_prueba=id_prueba).all()
    if not comentarios:
        return jsonify({"error": "No se encontraron comentarios para esta prueba"}), 404
    comentarios_list = [{
        "codigo_hc": c.codigo_hc,
        "id_prueba": c.id_prueba,
        "tipo_comentario": c.tipo_comentario,
        "comentario": c.comentario
    } for c in comentarios]
    return jsonify(comentarios_list), 200


# Obtener un comentario por clave compuesta (GET)
@comentarios_bp.route('/comentarios/<int:codigo_hc>/<int:id_prueba>/<string:tipo_comentario>', methods=['GET'])
def obtener_comentario(codigo_hc, id_prueba, tipo_comentario):
    comentario = Comentarios.query.get((codigo_hc, id_prueba, tipo_comentario))
    if comentario:
        return jsonify({
            "codigo_hc": comentario.codigo_hc,
            "id_prueba": comentario.id_prueba,
            "tipo_comentario": comentario.tipo_comentario,
            "comentario": comentario.comentario
        }), 200
    else:
        return jsonify({"error": "Comentario no encontrado"}), 404

# Actualizar un comentario por clave compuesta (PUT)
@comentarios_bp.route('/comentarios/<int:codigo_hc>/<int:id_prueba>/<string:tipo_comentario>', methods=['PUT'])
def actualizar_comentario(codigo_hc, id_prueba, tipo_comentario):
    comentario = Comentarios.query.get((codigo_hc, id_prueba, tipo_comentario))
    if not comentario:
        return jsonify({"error": "Comentario no encontrado"}), 404

    data = request.get_json()
    comentario_texto = data.get('comentario', "No aplica")

    comentario.comentario = comentario_texto

    try:
        db.session.commit()
        return jsonify({"message": "Comentario actualizado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar un comentario por clave compuesta (DELETE)
@comentarios_bp.route('/comentarios/<int:codigo_hc>/<int:id_prueba>/<string:tipo_comentario>', methods=['DELETE'])
def eliminar_comentario(codigo_hc, id_prueba, tipo_comentario):
    comentario = Comentarios.query.get((codigo_hc, id_prueba, tipo_comentario))
    if not comentario:
        return jsonify({"error": "Comentario no encontrado"}), 404

    try:
        db.session.delete(comentario)
        db.session.commit()
        return jsonify({"message": "Comentario eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
