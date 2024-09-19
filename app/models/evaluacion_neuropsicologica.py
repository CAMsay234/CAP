from app import db


class EvaluacionNeuropsicologica(db.Model):
    __tablename__ = 'evaluaciones_neuropsicologicas'  # Nombre de la tabla en la base de datos

    # Clave primaria compuesta
    codigo_hc = db.Column(db.Integer, db.ForeignKey('historias_clinicas.codigo_hc'), primary_key=True, nullable=False)
    id_prueba = db.Column(db.Integer, db.ForeignKey('pruebas.id'), primary_key=True, nullable=False)
    id_subprueba = db.Column(db.Integer, db.ForeignKey('sub_pruebas.id'), primary_key=True, nullable=False)
    puntaje = db.Column(db.Float, nullable=False)
    media = db.Column(db.Float, nullable=False)
    desviacion_estandar = db.Column(db.Float, nullable=False)
    interpretacion = db.Column(db.Text, nullable=False)


    def __repr__(self):
        return f'<EvaluacionNeuropsicologica {self.codigo_hc}, {self.id_prueba}, {self.id_subprueba}>'


