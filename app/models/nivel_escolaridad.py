from app import db

class NivelEscolaridad(db.Model):
    __tablename__ = 'nivel_escolaridad'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<NivelEscolaridad {self.descripcion}>'
