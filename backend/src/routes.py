from flask import Blueprint, request, jsonify
from database import db
from src.models import Evento, Usuario
import jwt
import datetime

api_bp = Blueprint('api', __name__)
SECRET_KEY = "tu_clave_secreta_provisional"

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Usuario.query.filter_by(email=data.get('email')).first()
    if user and user.check_password(data.get('password')):
        token = jwt.encode({'user_id': user.id, 'rol': user.rol, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token, "rol": user.rol})
    return jsonify({"mensaje": "Credenciales inválidas"}), 401

@api_bp.route('/eventos', methods=['POST'])
def crear_evento():
    try:
        data = request.get_json()
        nuevo_evento = Evento(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            fecha=data.get('fecha'),
            capacidad_max=data.get('capacidad_max')
        )
        db.session.add(nuevo_evento)
        db.session.commit()
        return jsonify({"mensaje": "Evento creado exitosamente", "id": nuevo_evento.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@api_bp.route('/eventos/<int:evento_id>/registrar', methods=['POST'])
def registrar_asistente(evento_id):
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    
    evento = Evento.query.get_or_404(evento_id)
    usuario = Usuario.query.get_or_404(usuario_id)

    if len(evento.asistentes) >= evento.capacidad_max:
        return jsonify({"error": "Evento lleno. No hay cupos disponibles"}), 400
    
    if usuario in evento.asistentes:
        return jsonify({"mensaje": "Ya estás registrado en este evento"}), 400

    evento.asistentes.append(usuario)
    db.session.commit()
    return jsonify({"mensaje": "Registro exitoso"}), 201

@api_bp.route('/admin/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nuevo = Usuario(nombre=data['nombre'], email=data['email'], rol=data.get('rol', 'asistente'))
    nuevo.set_password(data['password'])
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Usuario creado"}), 201

@api_bp.route('/eventos', methods=['GET'])
def listar_eventos():
    eventos = Evento.query.all()
    return jsonify([e.to_dict() for e in eventos]), 200
