from app import db

class Comentarios(db.Model):
    __tablename__ = 'comentarios_clinicos'
    
    # Clave primaria compuesta
    codigo_hc = db.Column(db.Integer, db.ForeignKey('historias_clinicas.codigo_hc'), primary_key=True, nullable=False)
    id_prueba = db.Column(db.Integer, db.ForeignKey('pruebas.id'), primary_key=True, nullable=False)
    tipo_comentario = db.Column(db.String(100),primary_key = True, nullable=False)
    comentario = db.Column(db.String(700), default="No aplica", nullable=False)

    def __repr__(self):
        return f'<Comentarios codigo_hc={self.codigo_hc}, id_prueba={self.id_prueba}, tipo {self.tipo_comentario}>'
