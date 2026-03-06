from database import db
from werkzeug.security import generate_password_hash, check_password_hash

inscripciones = db.Table('inscripciones',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('evento_id', db.Integer, db.ForeignKey('eventos.id'), primary_key=True)
)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    rol = db.Column(db.String(20), default='asistente') 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Evento(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha = db.Column(db.String(50))
    capacidad_max = db.Column(db.Integer)
    asistentes = db.relationship('Usuario', secondary=inscripciones, backref='eventos_inscritos')

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "capacidad_max": self.capacidad_max,
            "asistentes_actuales": len(self.asistentes)
        }