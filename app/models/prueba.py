from app import db

class Prueba(db.Model):
    __tablename__ = 'pruebas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<pruebas {self.nombre}>'