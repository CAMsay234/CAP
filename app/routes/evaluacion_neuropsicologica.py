from flask import Blueprint, jsonify, request
from app import db
from app.models.evaluacion_neuropsicologica import EvaluacionNeuropsicologica

# Definir el blueprint para las rutas relacionadas con "evaluaciones_neuropsicologicas"
evaluaciones_bp = Blueprint('evaluaciones', __name__)

# Crear una nueva evaluación neuropsicológica (POST)
@evaluaciones_bp.route('/evaluaciones', methods=['POST'])
def crear_evaluacion():
    data = request.get_json()  # Obtener los datos en formato JSON
    if not data["codigo_hc"] or not data["id_prueba"] or not data["id_subprueba"] or not data["puntaje"] or not data["media"] or not data["desviacion_estandar"] or not data["interpretacion"]:
            return jsonify({"error": "Todos los campos son obligatorios"}), 400
    nueva_evaluacion = EvaluacionNeuropsicologica(
        codigo_hc=data["codigo_hc"],
        id_prueba=data["id_prueba"],
        id_subprueba=data["id_subprueba"],
        puntaje=data["puntaje"],
        media=data["media"],
        desviacion_estandar=data["desviacion_estandar"],
        interpretacion=data["interpretacion"]
    )
    
    
    try:
        db.session.add(nueva_evaluacion)
        db.session.commit()
        return jsonify({"message": "Evaluación neuropsicológica creada exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Obtener todas las evaluaciones neuropsicológicas (GET)
@evaluaciones_bp.route('/evaluaciones', methods=['GET'])
def obtener_evaluaciones():
    evaluaciones = EvaluacionNeuropsicologica.query.all()
    evaluaciones_list = [{
        "codigo_hc": e.codigo_hc,
        "id_prueba": e.id_prueba,
        "id_subprueba": e.id_subprueba,
        "puntaje": e.puntaje,
        "media": e.media,
        "desviacion_estandar": e.desviacion_estandar,
        "interpretacion": e.interpretacion
    } for e in evaluaciones]
    return jsonify(evaluaciones_list), 200

# Obtener una evaluación neuropsicológica por clave primaria compuesta (GET)
@evaluaciones_bp.route('/evaluaciones/<int:codigo_hc>/<int:id_prueba>/<int:id_subprueba>', methods=['GET'])
def obtener_evaluacion(codigo_hc, id_prueba, id_subprueba):
    evaluacion = EvaluacionNeuropsicologica.query.get((codigo_hc, id_prueba, id_subprueba))
    if evaluacion:
        return jsonify({
            "codigo_hc": evaluacion.codigo_hc,
            "id_prueba": evaluacion.id_prueba,
            "id_subprueba": evaluacion.id_subprueba,
            "puntaje": evaluacion.puntaje,
            "media": evaluacion.media,
            "desviacion_estandar": evaluacion.desviacion_estandar,
            "escalar": evaluacion.escalar,
            "interpretacion": evaluacion.interpretacion
        }), 200
    else:
        return jsonify({"error": "Evaluación neuropsicológica no encontrada"}), 404

# Actualizar una evaluación neuropsicológica por clave primaria compuesta (PUT)
@evaluaciones_bp.route('/evaluaciones/<int:codigo_hc>/<int:id_prueba>/<int:id_subprueba>', methods=['PUT'])
def actualizar_evaluacion(codigo_hc, id_prueba, id_subprueba):
    evaluacion = EvaluacionNeuropsicologica.query.get((codigo_hc, id_prueba, id_subprueba))
    if not evaluacion:
        return jsonify({"error": "Evaluación neuropsicológica no encontrada"}), 404

    data = request.get_json()
    evaluacion.puntaje = data.get('puntaje', evaluacion.puntaje)
    evaluacion.media = data.get('media', evaluacion.media)
    evaluacion.desviacion_estandar = data.get('desviacion_estandar', evaluacion.desviacion_estandar)
    evaluacion.escalar = data.get('escalar', evaluacion.escalar)
    evaluacion.interpretacion = data.get('interpretacion', evaluacion.interpretacion)

    try:
        db.session.commit()
        return jsonify({"message": "Evaluación neuropsicológica actualizada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar una evaluación neuropsicológica por clave primaria compuesta (DELETE)
@evaluaciones_bp.route('/evaluaciones/<int:codigo_hc>/<int:id_prueba>/<int:id_subprueba>', methods=['DELETE'])
def eliminar_evaluacion(codigo_hc, id_prueba, id_subprueba):
    evaluacion = EvaluacionNeuropsicologica.query.get((codigo_hc, id_prueba, id_subprueba))
    if not evaluacion:
        return jsonify({"error": "Evaluación neuropsicológica no encontrada"}), 404

    try:
        db.session.delete(evaluacion)
        db.session.commit()
        return jsonify({"message": "Evaluación neuropsicológica eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Obtener evaluaciones específicas por codigo_hc y id_prueba (GET)
@evaluaciones_bp.route('/evaluaciones/<codigo_hc>/<id_prueba>', methods=['GET'])
def obtener_evaluaciones_por_codigo_y_prueba(codigo_hc, id_prueba):
    evaluaciones = EvaluacionNeuropsicologica.query.filter_by(codigo_hc=codigo_hc, id_prueba=id_prueba).all()
    if not evaluaciones:
        return jsonify({"message": "No se encontraron evaluaciones para este paciente y prueba."}), 404

    evaluaciones_list = [{
        "codigo_hc": e.codigo_hc,
        "id_prueba": e.id_prueba,
        "id_subprueba": e.id_subprueba,
        "puntaje": e.puntaje,
        "media": e.media,
        "desviacion_estandar": e.desviacion_estandar,
        "interpretacion": e.interpretacion
    } for e in evaluaciones]

    return jsonify(evaluaciones_list), 200