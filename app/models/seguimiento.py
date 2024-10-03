from app import db

class Seguimiento(db.Model):
    __tablename__ = 'seguimientos'
    
    # Clave primaria compuesta (codigo_hc + num_seccion)
    codigo_hc = db.Column(db.Integer, db.ForeignKey('historias_clinicas.codigo_hc'), primary_key=True, nullable=False)
    num_seccion = db.Column(db.Integer, primary_key=True, nullable=False)
    
    # Otros campos
    fecha = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.String(800), nullable=False)

    def __repr__(self):
        return f'<Seguimiento {self.fecha}, numero seccion {self.num_seccion}>'

# Función para obtener el siguiente número de sección
def get_next_num_seccion(codigo_hc):
    count = Seguimiento.query.filter_by(codigo_hc=codigo_hc).count()
    return count + 1

# Función para crear un nuevo seguimiento
def crear_nuevo_seguimiento(codigo_hc, fecha, descripcion):
    num_seccion = get_next_num_seccion(codigo_hc)
    nuevo_seguimiento = Seguimiento(
        codigo_hc=codigo_hc,
        num_seccion=num_seccion,
        fecha=fecha,
        descripcion=descripcion
    )
    
    db.session.add(nuevo_seguimiento)
    db.session.commit()
    
    return nuevo_seguimiento

