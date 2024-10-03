from app import db 

class Hipotesis(db.Model):
    __tablename__ = 'hipotesis'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descripcion = db.Column(db.String(100), nullable=False, unique=True)


    def __repr__(self):
        return f'<Hipotesis {self.descripcion}>'