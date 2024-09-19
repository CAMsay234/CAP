from app import db


class Historia_Clinica(db.Model):
    __tablename__ = 'historias_clinicas'
    codigo_hc = db.Column(db.Integer, db.ForeignKey('pacientes.codigo_hc'), primary_key=True, nullable=False)
    documento_paciente = db.Column(db.String(20), db.ForeignKey('pacientes.documento'), nullable=False)
    motivo_consulta = db.Column(db.String(1000), nullable=False)
    estado_actual = db.Column(db.String(1000), nullable=False)
    antecedentes = db.Column(db.String(1000), nullable=False)
    historial_personal = db.Column(db.String(1000), nullable=False)
    historial_familiar = db.Column(db.String(1000), nullable=False)




    def __repr__(self):
        return f'<historia_clinica {self.codigo_HC}>'
