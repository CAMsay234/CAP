from app import db

class Prueba(db.Model):
    __tablename__ = 'pruebas'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<pruebas {self.nombre}>'

    @classmethod
    def insertar_valores_por_defecto(cls):
        nombres = [
            "Atención y concentración", "Procesos perceptuales", "Funciones neurocognitivas", 
            "Lenguaje", "Procesos de memoria", "Función ejecutiva", "Capacidad intelectual"
        ]
        for nombre in nombres:
            if not cls.query.filter_by(nombre=nombre).first():
                nueva_prueba = cls(nombre=nombre)
                db.session.add(nueva_prueba)
        db.session.commit()