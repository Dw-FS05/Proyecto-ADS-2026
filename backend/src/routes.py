from flask import Blueprint, request, jsonify, current_app
from database import db
from src.models import Evento, Usuario
import jwt
import datetime

api_bp = Blueprint('api', __name__)


@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user = Usuario.query.filter_by(email=data.get('email')).first()
    if user and user.check_password(data.get('password')):
        token = jwt.encode(
            {
                'user_id': user.id,
                'rol':     user.rol,
                'exp':     datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256',
        )
        return jsonify({'token': token, 'rol': user.rol})
    return jsonify({'mensaje': 'Credenciales invalidas'}), 401


@api_bp.route('/eventos', methods=['POST'])
def crear_evento():
    try:
        data = request.get_json() or {}
        nuevo = Evento(
            nombre=data['nombre'],
            descripcion=data.get('descripcion'),
            fecha=data.get('fecha'),
            capacidad_max=data.get('capacidad_max'),
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({'mensaje': 'Evento creado exitosamente', 'id': nuevo.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@api_bp.route('/eventos', methods=['GET'])
def listar_eventos():
    return jsonify([e.to_dict() for e in Evento.query.all()]), 200


@api_bp.route('/eventos/<int:evento_id>', methods=['GET'])
def obtener_evento(evento_id):
    evento = Evento.query.get_or_404(evento_id)
    return jsonify(evento.to_dict(include_asistentes=True)), 200


@api_bp.route('/eventos/<int:evento_id>/registrar', methods=['POST'])
def registrar_asistente(evento_id):
    data      = request.get_json() or {}
    evento    = Evento.query.get_or_404(evento_id)
    usuario   = Usuario.query.get_or_404(data.get('usuario_id'))
    if usuario in evento.asistentes:
        return jsonify({'mensaje': 'Ya estas registrado en este evento'}), 400
    if evento.capacidad_max is not None and len(evento.asistentes) >= evento.capacidad_max:
        return jsonify({'error': 'Evento lleno. No hay cupos disponibles'}), 400
    evento.asistentes.append(usuario)
    db.session.commit()
    return jsonify({'mensaje': 'Registro exitoso'}), 201


@api_bp.route('/admin/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify([u.to_dict() for u in Usuario.query.all()]), 200


@api_bp.route('/admin/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json() or {}
    if Usuario.query.filter_by(email=data.get('email')).first():
        return jsonify({'error': 'Ya existe un usuario con ese email'}), 400
    nuevo = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        rol=data.get('rol', 'asistente'),
    )
    nuevo.set_password(data['password'])
    try:
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({'mensaje': 'Usuario creado'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
