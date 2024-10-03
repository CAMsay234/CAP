from app import db

# Definir la tabla intermedia
diagnostico_hipotesis = db.Table('diagnostico_hipotesis',
    db.Column('codigo_hc', db.Integer, db.ForeignKey('diagnosticos.codigo_hc'), primary_key=True),
    db.Column('codigo_hipotesis', db.Integer, db.ForeignKey('hipotesis.id'), primary_key=True)
)

# Modelo Diagnostico
class Diagnostico(db.Model):
    __tablename__ = 'diagnosticos'
    
    codigo_hc = db.Column(db.Integer, db.ForeignKey('historias_clinicas.codigo_hc'), primary_key=True, nullable=False)
    plan_Tratamiento = db.Column(db.String(700), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    conclusion = db.Column(db.String(700), nullable=False)

    # Relación muchos a muchos con hipotesis a través de la tabla intermedia
    hipotesis = db.relationship('Hipotesis', secondary=diagnostico_hipotesis, backref=db.backref('diagnosticos'))

    def __repr__(self):
        return f'<Diagnostico {self.codigo_hc}>'