from flask import Blueprint, request, jsonify
from app import db
from app.models.conversion import Conversion

conversiones_bp = Blueprint('conversiones', __name__)

@conversiones_bp.route('/conversiones', methods=['POST'])
def create_conversion():
    data = request.get_json()
    new_conversion = Conversion(
        codigo_hc=data['codigo_hc'],
        id_prueba=data['id_prueba'],
        id_subprueba=data['id_subprueba'],
        suma_puntuacion=data['suma_puntuacion'],
        puntuacion_compuesta=data['puntuacion_compuesta'],
        rango_percentil=data['rango_percentil'],
        intervalo_confianza=data['intervalo_confianza']
    )
    db.session.add(new_conversion)
    db.session.commit()
    return jsonify({'message': 'Conversion created successfully'}), 201

@conversiones_bp.route('/conversiones/<int:codigo_hc>/<int:id_prueba>/<int:id_subprueba>', methods=['GET'])
def get_conversion(codigo_hc, id_prueba, id_subprueba):
    conversion = Conversion.query.get((codigo_hc, id_prueba, id_subprueba))
    if not conversion:
        return jsonify({'message': 'Conversion not found'}), 404
    return jsonify({
        'codigo_hc': conversion.codigo_hc,
        'id_prueba': conversion.id_prueba,
        'id_subprueba': conversion.id_subprueba,
        'suma_puntuacion': conversion.suma_puntuacion,
        'puntuacion_compuesta': conversion.puntuacion_compuesta,
        'rango_percentil': conversion.rango_percentil,
        'intervalo_confianza': conversion.intervalo_confianza
    })
@conversiones_bp.route('/conversiones/<int:codigo_hc>', methods=['GET'])
def get_conversions(codigo_hc):
    # Obtener todas las conversiones asociadas al codigo_hc
    conversiones = Conversion.query.filter_by(codigo_hc=codigo_hc).all()
    if not conversiones:
        return jsonify({'message': 'No se encontraron conversiones para este paciente.'}), 404

    # Crear una lista con los datos de cada conversión
    conversiones_data = [
        {
            'codigo_hc': conversion.codigo_hc,
            'id_prueba': conversion.id_prueba,
            'id_subprueba': conversion.id_subprueba,
            'suma_puntuacion': conversion.suma_puntuacion,
            'puntuacion_compuesta': conversion.puntuacion_compuesta,
            'rango_percentil': conversion.rango_percentil,
            'intervalo_confianza': conversion.intervalo_confianza
        }
        for conversion in conversiones
    ]

    return jsonify(conversiones_data), 200



@conversiones_bp.route('/conversiones/<int:codigo_hc>/<int:id_prueba>/<int:id_subprueba>', methods=['PUT'])
def update_conversion(codigo_hc, id_prueba, id_subprueba):
    data = request.get_json()
    conversion = Conversion.query.get((codigo_hc, id_prueba, id_subprueba))
    if not conversion:
        return jsonify({'message': 'Conversion not found'}), 404
    conversion.suma_puntuacion = data.get('suma_puntacion', conversion.suma_puntacion)
    conversion.puntuacion_compuesta = data.get('puntuacion_compuesta', conversion.puntacion_compuesta)
    conversion.memoria_trabajo = data.get('memoria_trabajo', conversion.memoria_trabajo)
    conversion.rango_percentil = data.get('rango_percentil', conversion.rango_percentil)
    conversion.intervalo_confianza = data.get('intervalo_confianza', conversion.intervalo_confianza)
    db.session.commit()
    return jsonify({'message': 'Conversion updated successfully'})

@conversiones_bp.route('/conversiones/<int:codigo_hc>/<int:id_prueba>/<int:id_subprueba>', methods=['DELETE'])
def delete_conversion(codigo_hc, id_prueba, id_subprueba):
    conversion = Conversion.query.get((codigo_hc, id_prueba, id_subprueba))
    if not conversion:
        return jsonify({'message': 'Conversion not found'}), 404
    db.session.delete(conversion)
    db.session.commit()
    return jsonify({'message': 'Conversion deleted successfully'})

