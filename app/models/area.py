from app import db

class Area(db.Model):
    __tablename__ = 'areas'
    codigo_hc = db.Column(db.Integer, db.ForeignKey('historias_clinicas.codigo_hc'), primary_key=True, nullable=False)
    familiar = db.Column(db.String(500), nullable=False)
    pareja = db.Column(db.String(500), nullable=False)
    social = db.Column(db.String(500), nullable=False)
    laboral = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'<Area {self.codigo_hc}>'