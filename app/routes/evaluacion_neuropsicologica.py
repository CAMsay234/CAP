from flask import Blueprint, jsonify, request
from app import db
from app.models.evaluacion_neuropsicologica import EvaluacionNeuropsicologica

# Definir el blueprint para las rutas relacionadas con "evaluaciones_neuropsicologicas"
evaluaciones_bp = Blueprint('evaluaciones', __name__)

# Crear una nueva evaluación neuropsicológica (POST)
@evaluaciones_bp.route('/evaluaciones', methods=['POST'])
def crear_evaluacion():
    data = request.get_json()  # Obtener los datos en formato JSON
    codigo_hc = data.get('codigo_hc')
    id_prueba = data.get('id_prueba')
    id_subprueba = data.get('id_subprueba')
    puntaje = data.get('puntaje')
    media = data.get('media')
    desviacion_estandar = data.get('desviacion_estandar')
    interpretacion = data.get('interpretacion')

    if not codigo_hc or not id_prueba or not id_subprueba or not puntaje or not media or not desviacion_estandar or not interpretacion:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    nueva_evaluacion = EvaluacionNeuropsicologica(
        codigo_hc=codigo_hc,
        id_prueba=id_prueba,
        id_subprueba=id_subprueba,
        puntaje=puntaje,
        media=media,
        desviacion_estandar=desviacion_estandar,
        interpretacion=interpretacion
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
