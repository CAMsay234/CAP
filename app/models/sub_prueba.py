from app import db

class SubPrueba(db.Model):
    __tablename__ = 'sub_pruebas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_prueba = db.Column(db.Integer, db.ForeignKey('pruebas.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<SubPrueba {self.nombre}>'