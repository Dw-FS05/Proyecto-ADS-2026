#!/usr/bin/env python3
"""
setup_tests.py
Ejecuta este script UNA SOLA VEZ desde la carpeta backend/ para crear
todos los archivos necesarios para las pruebas.

Uso:
    cd backend
    python setup_tests.py

Luego instala dependencias y corre los tests:
    pip install -r requirements.txt
    pytest
"""
import os, sys

BASE  = os.path.dirname(os.path.abspath(__file__))
SRC   = os.path.join(BASE, 'src')
TESTS = os.path.join(BASE, 'tests')

os.makedirs(SRC,   exist_ok=True)
os.makedirs(TESTS, exist_ok=True)

FILES = {}

# ── pytest.ini ───────────────────────────────────────────────────────────────
FILES['pytest.ini'] = """\
[pytest]
testpaths = tests
addopts = -v --tb=short
"""

# ── requirements.txt ─────────────────────────────────────────────────────────
FILES['requirements.txt'] = """\
blinker==1.9.0
click==8.3.1
colorama==0.4.6
Flask==3.1.2
Flask-SQLAlchemy==3.1.1
greenlet==3.3.1
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
psycopg2-binary==2.9.11
SQLAlchemy==2.0.46
typing_extensions==4.15.0
Werkzeug==3.1.5
PyJWT==2.8.0
Flask-Cors==6.0.1
python-dotenv==1.1.1
gunicorn==23.0.0
pytest==8.3.4
pytest-cov==6.1.0
"""

# ── src/__init__.py ──────────────────────────────────────────────────────────
FILES['src/__init__.py'] = ""

# ── src/services.py ──────────────────────────────────────────────────────────
FILES['src/services.py'] = ""

# ── src/models.py ────────────────────────────────────────────────────────────
FILES['src/models.py'] = """\
from database import db
from werkzeug.security import generate_password_hash, check_password_hash

inscripciones = db.Table(
    'inscripciones',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True),
    db.Column('evento_id',  db.Integer, db.ForeignKey('eventos.id'),  primary_key=True),
)


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id            = db.Column(db.Integer, primary_key=True)
    nombre        = db.Column(db.String(100), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    rol           = db.Column(db.String(20), default='asistente')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id':     self.id,
            'nombre': self.nombre,
            'email':  self.email,
            'rol':    self.rol,
        }


class Evento(db.Model):
    __tablename__ = 'eventos'
    id           = db.Column(db.Integer, primary_key=True)
    nombre       = db.Column(db.String(100), nullable=False)
    descripcion  = db.Column(db.Text)
    fecha        = db.Column(db.String(50))
    capacidad_max = db.Column(db.Integer)
    asistentes   = db.relationship(
        'Usuario', secondary=inscripciones, backref='eventos_inscritos'
    )

    def to_dict(self, include_asistentes=False):
        data = {
            'id':                 self.id,
            'nombre':             self.nombre,
            'descripcion':        self.descripcion,
            'fecha':              self.fecha,
            'capacidad_max':      self.capacidad_max,
            'asistentes_actuales': len(self.asistentes),
        }
        if include_asistentes:
            data['asistentes'] = [a.to_dict() for a in self.asistentes]
        return data
"""

# ── src/routes.py ────────────────────────────────────────────────────────────
FILES['src/routes.py'] = """\
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
"""

# ── tests/conftest.py ────────────────────────────────────────────────────────
FILES['tests/conftest.py'] = """\
import os

os.environ.setdefault('SECRET_KEY',    'test-secret-key-pytest')
os.environ.setdefault('DATABASE_URL',  'sqlite:///:memory:')

import pytest
from app import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
"""

# ── tests/test_smoke.py ──────────────────────────────────────────────────────
FILES['tests/test_smoke.py'] = """\
from app import app


def test_app_carga():
    assert app is not None
    assert app.name == 'app'


def test_get_eventos_responde_200(client):
    r = client.get('/api/eventos')
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)


def test_login_endpoint_responde(client):
    r = client.post('/api/login', json={'email': 'noexiste@x.com', 'password': 'x'})
    assert r.status_code == 401


def test_listar_usuarios_responde(client):
    r = client.get('/api/admin/usuarios')
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)


def test_endpoint_inexistente_retorna_404(client):
    r = client.get('/api/ruta_que_no_existe')
    assert r.status_code == 404


def test_respuesta_eventos_es_json(client):
    r = client.get('/api/eventos')
    assert 'application/json' in r.content_type


def test_respuesta_usuarios_es_json(client):
    r = client.get('/api/admin/usuarios')
    assert 'application/json' in r.content_type


def test_evento_inexistente_retorna_404(client):
    r = client.get('/api/eventos/9999')
    assert r.status_code == 404


def test_login_sin_body_retorna_error(client):
    r = client.post('/api/login', json={})
    assert r.status_code == 401


def test_modo_testing_activo(client):
    assert app.config['TESTING'] is True
"""

# ── tests/test_unit.py ───────────────────────────────────────────────────────
FILES['tests/test_unit.py'] = """\
import pytest
from app import app
from src.models import Usuario, Evento


@pytest.fixture
def ctx():
    with app.app_context():
        yield


def test_usuario_to_dict(ctx):
    u = Usuario(nombre='Ana', email='ana@test.com', rol='organizador')
    u.id = 12
    assert u.to_dict() == {'id': 12, 'nombre': 'Ana', 'email': 'ana@test.com', 'rol': 'organizador'}


def test_usuario_password_set_and_check(ctx):
    u = Usuario(nombre='B', email='b@test.com')
    u.set_password('clave123')
    assert u.check_password('clave123') is True
    assert u.check_password('otra') is False


def test_evento_to_dict_sin_asistentes(ctx):
    e = Evento(nombre='Summit', descripcion='Desc', fecha='2026-01-01', capacidad_max=100)
    e.id = 3
    d = e.to_dict()
    assert d['id'] == 3
    assert d['nombre'] == 'Summit'
    assert d['asistentes_actuales'] == 0
    assert 'asistentes' not in d


def test_evento_to_dict_con_asistentes(ctx):
    e = Evento(nombre='Meet', capacidad_max=10)
    e.id = 1
    a = Usuario(nombre='C', email='c@test.com', rol='asistente')
    a.id = 7
    e.asistentes.append(a)
    d = e.to_dict(include_asistentes=True)
    assert d['asistentes_actuales'] == 1
    assert d['asistentes'][0]['email'] == 'c@test.com'


def test_usuario_rol_por_defecto(ctx):
    u = Usuario(nombre='Default', email='def@test.com')
    assert u.rol == 'asistente'


def test_usuario_to_dict_tiene_claves_correctas(ctx):
    u = Usuario(nombre='X', email='x@test.com', rol='admin')
    u.id = 1
    assert set(u.to_dict().keys()) == {'id', 'nombre', 'email', 'rol'}


def test_usuario_password_incorrecto_retorna_false(ctx):
    u = Usuario(nombre='Z', email='z@test.com')
    u.set_password('correcta')
    assert u.check_password('incorrecta') is False


def test_usuario_password_hash_no_es_texto_plano(ctx):
    u = Usuario(nombre='H', email='h@test.com')
    u.set_password('mipassword')
    assert u.password_hash != 'mipassword'
    assert u.password_hash is not None


def test_evento_to_dict_claves_base(ctx):
    e = Evento(nombre='Base', capacidad_max=20)
    e.id = 5
    assert set(e.to_dict().keys()) == {
        'id', 'nombre', 'descripcion', 'fecha', 'capacidad_max', 'asistentes_actuales'
    }


def test_evento_to_dict_include_asistentes_agrega_clave(ctx):
    e = Evento(nombre='Conv', capacidad_max=5)
    e.id = 2
    d = e.to_dict(include_asistentes=True)
    assert 'asistentes' in d
    assert isinstance(d['asistentes'], list)


def test_evento_capacidad_max_none(ctx):
    e = Evento(nombre='SinLimite')
    e.id = 9
    d = e.to_dict()
    assert d['capacidad_max'] is None
    assert d['asistentes_actuales'] == 0


def test_evento_multiples_asistentes(ctx):
    e = Evento(nombre='Grande', capacidad_max=100)
    e.id = 10
    for i in range(3):
        u = Usuario(nombre=f'U{i}', email=f'u{i}@g.com', rol='asistente')
        u.id = i + 1
        e.asistentes.append(u)
    d = e.to_dict(include_asistentes=True)
    assert d['asistentes_actuales'] == 3
    assert len(d['asistentes']) == 3
"""

# ── tests/test_integration.py ────────────────────────────────────────────────
FILES['tests/test_integration.py'] = """\
import json


def _post_usuario(client, nombre, email, password='pass', rol='asistente'):
    return client.post('/api/admin/usuarios', data=json.dumps(
        {'nombre': nombre, 'email': email, 'password': password, 'rol': rol}
    ), content_type='application/json')


def _post_evento(client, nombre, capacidad=10, descripcion=None, fecha=None):
    return client.post('/api/eventos', data=json.dumps(
        {'nombre': nombre, 'capacidad_max': capacidad, 'descripcion': descripcion, 'fecha': fecha}
    ), content_type='application/json')


def _registrar(client, evento_id, usuario_id):
    return client.post(f'/api/eventos/{evento_id}/registrar',
                       data=json.dumps({'usuario_id': usuario_id}),
                       content_type='application/json')


# ── Tests originales ─────────────────────────────────────────────────────────

def test_listar_eventos_vacio(client):
    assert client.get('/api/eventos').get_json() == []


def test_crear_usuario_y_login(client):
    assert _post_usuario(client, 'Test', 'test@test.com', 'secret123').status_code == 201
    r = client.post('/api/login',
                    data=json.dumps({'email': 'test@test.com', 'password': 'secret123'}),
                    content_type='application/json')
    assert r.status_code == 200
    data = r.get_json()
    assert 'token' in data
    assert data['rol'] == 'asistente'


def test_login_credenciales_invalidas(client):
    r = client.post('/api/login',
                    data=json.dumps({'email': 'nada@x.com', 'password': 'x'}),
                    content_type='application/json')
    assert r.status_code == 401


def test_crear_evento_y_listar(client):
    r = _post_evento(client, 'Conferencia', capacidad=50,
                     descripcion='Desc', fecha='2026-06-01')
    assert r.status_code == 201
    eid = r.get_json()['id']
    lista = client.get('/api/eventos').get_json()
    assert len(lista) == 1 and lista[0]['id'] == eid


def test_obtener_evento(client):
    _post_evento(client, 'E1')
    r = client.get('/api/eventos/1')
    assert r.status_code == 200
    assert r.get_json()['nombre'] == 'E1'


def test_registrar_asistente(client):
    _post_usuario(client, 'As', 'as@a.com', 'p')
    _post_evento(client, 'Meetup', capacidad=5)
    assert _registrar(client, 1, 1).status_code == 201
    assert len(client.get('/api/eventos/1').get_json()['asistentes']) == 1


def test_listar_usuarios(client):
    _post_usuario(client, 'U1', 'u1@u.com')
    r = client.get('/api/admin/usuarios')
    assert r.status_code == 200 and len(r.get_json()) == 1


def test_evento_lleno_rechaza_registro(client):
    _post_usuario(client, 'P1', 'p1@t.com')
    _post_usuario(client, 'P2', 'p2@t.com')
    _post_evento(client, 'Mini', capacidad=1)
    assert _registrar(client, 1, 1).status_code == 201
    assert _registrar(client, 1, 2).status_code == 400


def test_registro_duplicado_rechaza(client):
    _post_usuario(client, 'Solo', 'solo@t.com')
    _post_evento(client, 'Ev')
    assert _registrar(client, 1, 1).status_code == 201
    assert _registrar(client, 1, 1).status_code == 400


# ── Tests nuevos ─────────────────────────────────────────────────────────────

def test_email_duplicado_rechaza(client):
    payload = json.dumps({'nombre': 'D', 'email': 'dup@t.com', 'password': 'p', 'rol': 'asistente'})
    assert client.post('/api/admin/usuarios', data=payload,
                       content_type='application/json').status_code == 201
    assert client.post('/api/admin/usuarios', data=payload,
                       content_type='application/json').status_code == 400


def test_evento_inexistente_404(client):
    assert client.get('/api/eventos/9999').status_code == 404


def test_multiples_eventos_listados(client):
    for n in ['Alpha', 'Beta', 'Gamma']:
        _post_evento(client, n)
    lista = client.get('/api/eventos').get_json()
    assert len(lista) == 3
    assert {e['nombre'] for e in lista} == {'Alpha', 'Beta', 'Gamma'}


def test_asistentes_actuales_incrementa(client):
    for i in range(3):
        _post_usuario(client, f'U{i}', f'u{i}@i.com')
    _post_evento(client, 'Incr', capacidad=10)
    for uid in [1, 2, 3]:
        _registrar(client, 1, uid)
    data = client.get('/api/eventos/1').get_json()
    assert data['asistentes_actuales'] == 3
    assert len(data['asistentes']) == 3


def test_token_jwt_formato_valido(client):
    _post_usuario(client, 'J', 'j@j.com', 'pass123')
    r = client.post('/api/login',
                    data=json.dumps({'email': 'j@j.com', 'password': 'pass123'}),
                    content_type='application/json')
    assert len(r.get_json()['token'].split('.')) == 3


def test_login_retorna_rol_correcto(client):
    _post_usuario(client, 'Org', 'org@t.com', 'org123', rol='organizador')
    r = client.post('/api/login',
                    data=json.dumps({'email': 'org@t.com', 'password': 'org123'}),
                    content_type='application/json')
    assert r.get_json()['rol'] == 'organizador'


def test_datos_evento_persisten(client):
    _post_evento(client, 'Tech Summit', capacidad=200,
                 descripcion='Evento de tecnologia', fecha='2026-09-15')
    d = client.get('/api/eventos/1').get_json()
    assert d['nombre'] == 'Tech Summit'
    assert d['descripcion'] == 'Evento de tecnologia'
    assert d['fecha'] == '2026-09-15'
    assert d['capacidad_max'] == 200


def test_registrar_en_evento_inexistente_404(client):
    _post_usuario(client, 'X', 'x@t.com')
    assert _registrar(client, 9999, 1).status_code == 404


def test_registrar_usuario_inexistente_404(client):
    _post_evento(client, 'Ev')
    assert _registrar(client, 1, 9999).status_code == 404


def test_listar_usuarios_vacio(client):
    r = client.get('/api/admin/usuarios')
    assert r.status_code == 200 and r.get_json() == []


def test_crear_evento_retorna_id(client):
    r = _post_evento(client, 'ConID')
    assert r.status_code == 201
    data = r.get_json()
    assert 'id' in data and isinstance(data['id'], int)
"""

# ── Write files ───────────────────────────────────────────────────────────────
created, skipped, failed = [], [], []

for rel_path, content in FILES.items():
    full_path = os.path.join(BASE, rel_path)
    action = 'created'
    try:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        created.append(rel_path)
    except Exception as e:
        failed.append((rel_path, str(e)))

print()
print('=' * 50)
print(' setup_tests.py - Resultado ')
print('=' * 50)
if created:
    print(f'\n Archivos creados/actualizados ({len(created)}):')
    for p in created:
        print(f'   {p}')
if failed:
    print(f'\n Fallos ({len(failed)}):')
    for p, e in failed:
        print(f'   {p}: {e}')
print()
print(' Siguiente paso:')
print('   pip install -r requirements.txt')
print('   pytest')
print('=' * 50)
