from flask import Blueprint, jsonify, request
from app import db
from app.models.historia_clinica import Historia_Clinica

# Definir el blueprint para las rutas relacionadas con "historias_clinicas"
historias_bp = Blueprint('historias', __name__)

# Crear una nueva historia clínica (POST)
@historias_bp.route('/historias', methods=['POST'])
def crear_historia_clinica():
    data = request.get_json()  # Obtener los datos en formato JSON
    codigo_hc = data.get('codigo_hc')
    documento_paciente = data.get('documento_paciente')
    motivo_consulta = data.get('motivo_consulta')
    estado_actual = data.get('estado_actual')
    antecedentes = data.get('antecedentes')
    historial_personal = data.get('historial_personal')
    historial_familiar = data.get('historial_familiar')

    if not codigo_hc or not documento_paciente or not motivo_consulta or not estado_actual or not antecedentes or not historial_personal or not historial_familiar:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    nueva_historia = Historia_Clinica(
        codigo_hc=codigo_hc,
        documento_paciente=documento_paciente,
        motivo_consulta=motivo_consulta,
        estado_actual=estado_actual,
        antecedentes=antecedentes,
        historial_personal=historial_personal,
        historial_familiar=historial_familiar
    )

    try:
        db.session.add(nueva_historia)
        db.session.commit()
        return jsonify({"message": "Historia Clínica creada exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Obtener todas las historias clínicas (GET)
@historias_bp.route('/historias', methods=['GET'])
def obtener_historias_clinicas():
    historias = Historia_Clinica.query.all()
    historias_list = [{
        "codigo_hc": h.codigo_hc, 
        "documento_paciente": h.documento_paciente,
        "motivo_consulta": h.motivo_consulta, 
        "estado_actual": h.estado_actual, 
        "antecedentes": h.antecedentes, 
        "historial_personal": h.historial_personal,
        "historial_familiar": h.historial_familiar
    } for h in historias]
    return jsonify(historias_list), 200

# Obtener una historia clínica por codigo_hc (GET)
@historias_bp.route('/historias/<int:codigo_hc>', methods=['GET'])
def obtener_historia_clinica(codigo_hc):
    historia = Historia_Clinica.query.get(codigo_hc)
    if historia:
        return jsonify({
            "codigo_hc": historia.codigo_hc,
            "documento_paciente": historia.documento_paciente,
            "motivo_consulta": historia.motivo_consulta,
            "estado_actual": historia.estado_actual,
            "antecedentes": historia.antecedentes,
            "historial_personal": historia.historial_personal,
            "historial_familiar": historia.historial_familiar
        }), 200
    else:
        return jsonify({"error": "Historia Clínica no encontrada"}), 404

# Actualizar una historia clínica por codigo_hc (PUT)
@historias_bp.route('/historias/<int:codigo_hc>', methods=['PUT'])
def actualizar_historia_clinica(codigo_hc):
    historia = Historia_Clinica.query.get(codigo_hc)
    if not historia:
        return jsonify({"error": "Historia Clínica no encontrada"}), 404

    data = request.get_json()
    historia.motivo_consulta = data.get('motivo_consulta', historia.motivo_consulta)
    historia.estado_actual = data.get('estado_actual', historia.estado_actual)
    historia.antecedentes = data.get('antecedentes', historia.antecedentes)
    historia.historial_personal = data.get('historial_personal', historia.historial_personal)
    historia.historial_familiar = data.get('historial_familiar', historia.historial_familiar)

    try:
        db.session.commit()
        return jsonify({"message": "Historia Clínica actualizada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar una historia clínica por codigo_hc (DELETE)
@historias_bp.route('/historias/<int:codigo_hc>', methods=['DELETE'])
def eliminar_historia_clinica(codigo_hc):
    historia = Historia_Clinica.query.get(codigo_hc)
    if not historia:
        return jsonify({"error": "Historia Clínica no encontrada"}), 404

    try:
        db.session.delete(historia)
        db.session.commit()
        return jsonify({"message": "Historia Clínica eliminada exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
