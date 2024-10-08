from app import db
from sqlalchemy import CheckConstraint


class Paciente(db.Model):
    __tablename__ = 'pacientes'
    codigo_hc = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Autonumérico
    documento = db.Column(db.String(20), nullable=False, unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    id_escolaridad = db.Column(db.Integer, db.ForeignKey('nivel_escolaridad.id'), nullable=False)
    escolaridad = db.relationship('NivelEscolaridad', backref='pacientes')
    profesion = db.Column(db.String(50), nullable=True)
    telefono = db.Column(db.String(15), nullable=False)
    celular = db.Column(db.String(15), nullable=False)
    remision = db.Column(db.String(100), nullable=True)

    # Restricciones adicionales:
    __table_args__ = (
        CheckConstraint('edad >= 0', name='check_edad_positiva'),  # Asegura que la edad sea positiva
        # CheckConstraint para números solo se puede manejar en la capa de aplicación, no en SQLite
    )

    def __repr__(self):
        return f'<Paciente {self.nombre}>'
    
def es_numerico(valor):
    return valor.isdigit()  # Retorna True si el valor contiene solo dígitos




