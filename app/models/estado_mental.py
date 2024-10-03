from app import db

class EstadoMental(db.Model):
    __tablename__ = 'estado_mental'
    codigo_hc = db.Column(db.Integer, db.ForeignKey('historias_clinicas.codigo_hc'), primary_key=True, nullable=False)
    atencion = db.Column(db.String(400), default = "no aplica",nullable=False)
    memoria = db.Column(db.String(400), default = "no aplica",nullable=False)
    lenguaje = db.Column(db.String(400), default = "no aplica",nullable=False)
    pensamiento = db.Column(db.String(400), default = "no aplica",nullable=False)
    introspeccion = db.Column(db.String(400), default = "no aplica",nullable=False)

    def __repr__(self):
        return f'<estado_mental {self.codigo_hc}>'