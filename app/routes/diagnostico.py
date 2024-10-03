from flask import Blueprint, jsonify, request
from app import db
from app.models.diagnostico import Diagnostico
from app.models.hipotesis import Hipotesis

# Definir el blueprint para las rutas relacionadas con "diagnosticos"
diagnosticos_bp = Blueprint('diagnosticos', __name__)

# Crear un nuevo diagnóstico (POST)
@diagnosticos_bp.route('/diagnosticos', methods=['POST'])
def crear_diagnostico():
    data = request.get_json()  # Obtener los datos en formato JSON
    codigo_hc = data.get('codigo_hc')
    plan_tratamiento = data.get('plan_Tratamiento')
    fecha = data.get('fecha')
    conclusion = data.get('conclusion')
    hipotesis_ids = data.get('hipotesis_ids')  # Lista de IDs de hipótesis

    if not codigo_hc or not plan_tratamiento or not fecha or not conclusion:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    # Crear el diagnóstico
    nuevo_diagnostico = Diagnostico(
        codigo_hc=codigo_hc,
        plan_Tratamiento=plan_tratamiento,
        fecha=fecha,
        conclusion=conclusion
    )

    # Asignar hipótesis relacionadas
    if hipotesis_ids:
        for hip_id in hipotesis_ids:
            hipotesis = Hipotesis.query.get(hip_id)
            if hipotesis:
                nuevo_diagnostico.hipotesis.append(hipotesis)

    try:
        db.session.add(nuevo_diagnostico)
        db.session.commit()
        return jsonify({"message": "Diagnóstico creado exitosamente"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Obtener todos los diagnósticos (GET)
@diagnosticos_bp.route('/diagnosticos', methods=['GET'])
def obtener_diagnosticos():
    diagnosticos = Diagnostico.query.all()
    diagnosticos_list = [{
        "codigo_hc": d.codigo_hc,
        "plan_tratamiento": d.plan_Tratamiento,
        "fecha": d.fecha,
        "conclusion": d.conclusion,
        "hipotesis": [{"id": h.id, "descripcion": h.descripcion} for h in d.hipotesis]
    } for d in diagnosticos]
    return jsonify(diagnosticos_list), 200

# Obtener un diagnóstico por codigo_hc (GET)
@diagnosticos_bp.route('/diagnosticos/<int:codigo_hc>', methods=['GET'])
def obtener_diagnostico(codigo_hc):
    diagnostico = Diagnostico.query.get(codigo_hc)
    if diagnostico:
        return jsonify({
            "codigo_hc": diagnostico.codigo_hc,
            "plan_tratamiento": diagnostico.plan_Tratamiento,
            "fecha": diagnostico.fecha,
            "conclusion": diagnostico.conclusion,
            "hipotesis": [{"id": h.id, "descripcion": h.descripcion} for h in diagnostico.hipotesis]
        }), 200
    else:
        return jsonify({"error": "Diagnóstico no encontrado"}), 404

# Actualizar un diagnóstico por codigo_hc (PUT)
@diagnosticos_bp.route('/diagnosticos/<int:codigo_hc>', methods=['PUT'])
def actualizar_diagnostico(codigo_hc):
    diagnostico = Diagnostico.query.get(codigo_hc)
    if not diagnostico:
        return jsonify({"error": "Diagnóstico no encontrado"}), 404

    data = request.get_json()
    diagnostico.plan_Tratamiento = data.get('plan_Tratamiento', diagnostico.plan_Tratamiento)
    diagnostico.fecha = data.get('fecha', diagnostico.fecha)
    diagnostico.conclusion = data.get('conclusion', diagnostico.conclusion)

    # Actualizar hipótesis relacionadas
    hipotesis_ids = data.get('hipotesis_ids')
    if hipotesis_ids:
        diagnostico.hipotesis.clear()  # Eliminar las hipótesis actuales
        for hip_id in hipotesis_ids:
            hipotesis = Hipotesis.query.get(hip_id)
            if hipotesis:
                diagnostico.hipotesis.append(hipotesis)

    try:
        db.session.commit()
        return jsonify({"message": "Diagnóstico actualizado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar un diagnóstico por codigo_hc (DELETE)
@diagnosticos_bp.route('/diagnosticos/<int:codigo_hc>', methods=['DELETE'])
def eliminar_diagnostico(codigo_hc):
    diagnostico = Diagnostico.query.get(codigo_hc)
    if not diagnostico:
        return jsonify({"error": "Diagnóstico no encontrado"}), 404

    try:
        db.session.delete(diagnostico)
        db.session.commit()
        return jsonify({"message": "Diagnóstico eliminado exitosamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
