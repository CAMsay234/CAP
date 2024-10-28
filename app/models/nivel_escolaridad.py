from app import db

class NivelEscolaridad(db.Model):
    __tablename__ = 'nivel_escolaridad'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<NivelEscolaridad {self.descripcion}>'
    
    @classmethod
    def insertar_valores_por_defecto(cls):
        niveles = ["Primaria", "Secundaria", "Técnico/Tecnológico", "Universitaria", "Posgrado", "No aplica"]
        for nivel in niveles:
            if not cls.query.filter_by(descripcion=nivel).first():
                nuevo_nivel = cls(descripcion=nivel)
                db.session.add(nuevo_nivel)
        db.session.commit()