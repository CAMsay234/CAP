from flask import Blueprint, request, jsonify
from app import db
from app.models.paciente import Paciente

pacientes_bp = Blueprint('pacientes', __name__)

# Ruta para listar todos los pacientes
@pacientes_bp.route('/pacientes', methods=['GET'])
def listar_pacientes():
    pacientes = Paciente.query.all()
    pacientes_data = [{'codigo_hc': p.codigo_hc, 'nombre': p.nombre, 'edad': p.edad, 'fecha_nacimiento': p.fecha_nacimiento.strftime('%Y-%m-%d'), 'telefono': p.telefono, 'celular': p.celular} for p in pacientes]
    return jsonify(pacientes_data)

# Ruta para crear un nuevo paciente
@pacientes_bp.route('/paciente/nuevo', methods=['POST'])
def crear_paciente():
    data = request.json  # Supone que los datos vienen en formato JSON

    nuevo_paciente = Paciente(
        documento=data['documento'],
        nombre=data['nombre'],
        edad=data['edad'],
        fecha_nacimiento=data['fecha_nacimiento'],  # Asegúrate de que la fecha esté en formato correcto (YYYY-MM-DD)
        escolaridad=data['escolaridad'],
        profesion=data['profesion'],
        telefono=data['telefono'],
        celular=data['celular'],
        remision=data['remision']
    )

    db.session.add(nuevo_paciente)
    db.session.commit()

    return jsonify({"mensaje": "Paciente creado exitosamente."}), 201

# Ruta para obtener los detalles de un paciente específico
@pacientes_bp.route('/paciente/<int:codigo_hc>', methods=['GET'])
def obtener_paciente(codigo_hc):
    paciente = Paciente.query.get_or_404(codigo_hc)
    paciente_data = {
        'codigo_hc': paciente.codigo_hc,
        'documento': paciente.documento,
        'nombre': paciente.nombre,
        'edad': paciente.edad,
        'fecha_nacimiento': paciente.fecha_nacimiento.strftime('%Y-%m-%d'),
        'telefono': paciente.telefono,
        'celular': paciente.celular,
        'remision': paciente.remision
    }
    return jsonify(paciente_data)

# Ruta para actualizar un paciente
@pacientes_bp.route('/paciente/<int:codigo_hc>', methods=['PUT'])
def actualizar_paciente(codigo_hc):
    paciente = Paciente.query.get_or_404(codigo_hc)
    data = request.json  # Supone que los datos vienen en formato JSON

    paciente.documento = data.get('documento', paciente.documento)
    paciente.nombre = data.get('nombre', paciente.nombre)
    paciente.edad = data.get('edad', paciente.edad)
    paciente.fecha_nacimiento = data.get('fecha_nacimiento', paciente.fecha_nacimiento)
    paciente.escolaridad = data.get('escolaridad', paciente.escolaridad)
    paciente.profesion = data.get('profesion', paciente.profesion)
    paciente.telefono = data.get('telefono', paciente.telefono)
    paciente.celular = data.get('celular', paciente.celular)
    paciente.remision = data.get('remision', paciente.remision)

    db.session.commit()

    return jsonify({"mensaje": "Paciente actualizado exitosamente."})

# Ruta para eliminar un paciente
@pacientes_bp.route('/paciente/<int:codigo_hc>', methods=['DELETE'])
def eliminar_paciente(codigo_hc):
    paciente = Paciente.query.get_or_404(codigo_hc)
    db.session.delete(paciente)
    db.session.commit()

    return jsonify({"mensaje": "Paciente eliminado exitosamente."})

