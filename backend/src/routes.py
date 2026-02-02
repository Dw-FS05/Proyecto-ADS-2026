from flask import Blueprint, request, jsonify
from database import db
from src.models import Evento

api_bp = Blueprint('api', __name__)

@api_bp.route('/eventos', methods=['POST'])
def crear_evento():
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

@api_bp.route('/eventos', methods=['GET'])
def listar_eventos():
    eventos = Evento.query.all()
    return jsonify([e.to_dict() for e in eventos]), 200