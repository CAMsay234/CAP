from flask import Blueprint, request, jsonify
from app import db
from app.models.paciente import Paciente
from datetime import datetime

pacientes_bp = Blueprint('pacientes', __name__)

# Ruta para listar todos los pacientes
@pacientes_bp.route('/pacientes/listar', methods=['GET'])
def listar_pacientes():
    pacientes = Paciente.query.all()
    pacientes_data = [{
        'codigo_hc': p.codigo_hc,
        'documento': p.documento,
        'nombre': p.nombre,
        'edad': p.edad,
        'fecha_nacimiento': p.fecha_nacimiento.strftime('%Y-%m-%d'),
        'telefono': p.telefono,
        'celular': p.celular,
        'id_escolaridad': p.id_escolaridad  # Corregido de id:escolaridad a id_escolaridad
    } for p in pacientes]
    return jsonify(pacientes_data)

@pacientes_bp.route('/paciente/buscar', methods=['GET'])
def buscar_paciente():
    documento = request.args.get('documento', None)
    
    if documento:
        paciente = Paciente.query.filter_by(documento=documento).first()
        if paciente:
            paciente_data = {
                'codigo_hc': paciente.codigo_hc,
                'documento': paciente.documento,
                'nombre': paciente.nombre,
                'edad': paciente.edad,
                'fecha_nacimiento': paciente.fecha_nacimiento.strftime('%Y-%m-%d'),
                'telefono': paciente.telefono,
                'celular': paciente.celular,
                'id_escolaridad': paciente.id_escolaridad,
                'remision': paciente.remision
            }
            return jsonify(paciente_data), 200
        else:
            return jsonify({'error': 'Paciente no encontrado'}), 404
    else:
        return jsonify({'error': 'Falta el parámetro documento'}), 400



# Ruta para crear un nuevo paciente
@pacientes_bp.route('/paciente/nuevo', methods=['POST'])
def crear_paciente():
    data = request.json  # Supone que los datos vienen en formato JSON
    
    # Convertir la fecha de nacimiento a un objeto date de Python
    fecha_nacimiento = datetime.strptime(data['fecha_nacimiento'], '%Y-%m-%d').date()

    nuevo_paciente = Paciente(
        documento=data['documento'],
        nombre=data['nombre'],
        edad=data['edad'],
        fecha_nacimiento=fecha_nacimiento,  # Pasar la fecha como objeto date
        id_escolaridad=data['id_escolaridad'],
        profesion=data['profesion'],
        telefono=data['telefono'],
        celular=data['celular'],
        remision=data['remision']
    )

    db.session.add(nuevo_paciente)
    db.session.commit()

    return jsonify({"mensaje": "Paciente creado exitosamente."}), 201

# Ruta para obtener los detalles de un paciente específico
@pacientes_bp.route('/paciente', methods=['GET'])
def obtener_paciente(documento):
    paciente = Paciente.query.get_or_404(documento)
    paciente_data = {
        'codigo_hc': paciente.codigo_hc,
        'documento': paciente.documento,
        'nombre': paciente.nombre,
        'edad': paciente.edad,
        'fecha_nacimiento': paciente.fecha_nacimiento.strftime('%Y-%m-%d'),
        'telefono': paciente.telefono,
        'celular': paciente.celular,
        'id_escolaridad': paciente.id_escolaridad,  # Se incluye el id de escolaridad
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
    paciente.id_escolaridad = data.get('id_escolaridad', paciente.id_escolaridad)  # Actualizar id escolaridad
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

# Ruta para contar el número de pacientes
@pacientes_bp.route('/pacientes/count', methods=['GET'])
def contar_pacientes():
    count = Paciente.query.count()  # Contar el número de pacientes en la base de datos
    return jsonify({'count': count})
