from app import db

class Conversion(db.Model):
    __tablename__ = 'conversiones'
    
    # Clave primaria compuesta
    codigo_hc = db.Column(db.Integer, db.ForeignKey('pacientes.codigo_hc'), primary_key=True, nullable=False)
    id_prueba = db.Column(db.Integer, db.ForeignKey('pruebas.id'), primary_key=True, nullable=False)
    id_subprueba = db.Column(db.Integer, db.ForeignKey('sub_pruebas.id'), primary_key=True, nullable=False)
    suma_puntacion = db.Column(db.Float, nullable=False)
    puntacion_compuesta = db.Column(db.Float, nullable=False)
    memoria_trabajo = db.Column(db.Float, nullable=False)
    rango_percentil = db.Column(db.Float, nullable=False)
    intervalo_confianza = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Conversion codigo_hc={self.codigo_hc}, id_prueba={self.id_prueba}, id_subprueba={self.id_subprueba}>'