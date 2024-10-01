from flask import Blueprint, jsonify, request
from app import db
from app.models.estado_mental import EstadoMental

# Definir el blueprint para las rutas relacionadas con "estado_mental"
estado_mental_bp = Blueprint('estado_mental', __name__)

# Crear un nuevo registro de estado mental (POST)
@estado_mental_bp.route('/estado_mental', methods=['POST'])
def crear_estado_mental():
    data = request.get_json()  # Obtener los datos en formato JSON
    codigo_hc = data.get('codigo_hc')
    atencion = data.get('atencion', "no aplica")
    memoria = data.get('memoria', "no aplica")
    lenguaje = data.get('lenguaje', "no aplica")
    pensamiento = data.get('pensamiento', "no aplica")
    introspeccion = data.get('introspeccion', "no aplica")

    if not codigo_hc:
        return jsonify({"error": "El código de historia clínica es obligatorio"}), 400

    nuevo_estado_mental = EstadoMental(
        codigo_hc=codigo_hc,
        atencion=atencion,
        memoria=memoria,
        lenguaje=lenguaje,
        pensamiento=pensamiento,
        introspeccion=introspeccion
    )

    try:
        db.session.add(nuevo_estado_mental)
        db.session.commit()
        return jsonify({"message": "Estado mental creado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Obtener todos los registros de estado mental (GET)
@estado_mental_bp.route('/estado_mental', methods=['GET'])
def obtener_estados_mentales():
    estados = EstadoMental.query.all()
    estados_list = [{
        "codigo_hc": e.codigo_hc,
        "atencion": e.atencion,
        "memoria": e.memoria,
        "lenguaje": e.lenguaje,
        "pensamiento": e.pensamiento,
        "introspeccion": e.introspeccion
    } for e in estados]
    return jsonify(estados_list), 200

# Obtener un estado mental por codigo_hc (GET)
@estado_mental_bp.route('/estado_mental/<int:codigo_hc>', methods=['GET'])
def obtener_estado_mental(codigo_hc):
    estado = EstadoMental.query.get(codigo_hc)
    if estado:
        return jsonify({
            "codigo_hc": estado.codigo_hc,
            "atencion": estado.atencion,
            "memoria": estado.memoria,
            "lenguaje": estado.lenguaje,
            "pensamiento": estado.pensamiento,
            "introspeccion": estado.introspeccion
        }), 200
    else:
        return jsonify({"error": "Estado mental no encontrado"}), 404

# Actualizar un estado mental por codigo_hc (PUT)
@estado_mental_bp.route('/estado_mental/<int:codigo_hc>', methods=['PUT'])
def actualizar_estado_mental(codigo_hc):
    estado = EstadoMental.query.get(codigo_hc)
    if not estado:
        return jsonify({"error": "Estado mental no encontrado"}), 404

    data = request.get_json()
    estado.atencion = data.get('atencion', estado.atencion)
    estado.memoria = data.get('memoria', estado.memoria)
    estado.lenguaje = data.get('lenguaje', estado.lenguaje)
    estado.pensamiento = data.get('pensamiento', estado.pensamiento)
    estado.introspeccion = data.get('introspeccion', estado.introspeccion)

    try:
        db.session.commit()
        return jsonify({"message": "Estado mental actualizado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar un estado mental por codigo_hc (DELETE)
@estado_mental_bp.route('/estado_mental/<int:codigo_hc>', methods=['DELETE'])
def eliminar_estado_mental(codigo_hc):
    estado = EstadoMental.query.get(codigo_hc)
    if not estado:
        return jsonify({"error": "Estado mental no encontrado"}), 404

    try:
        db.session.delete(estado)
        db.session.commit()
        return jsonify({"message": "Estado mental eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
