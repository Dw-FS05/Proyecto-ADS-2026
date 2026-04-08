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
    """El rol por defecto definido en el modelo debe ser 'asistente'."""
    col = Usuario.__table__.c['rol']
    assert str(col.default.arg) == 'asistente'


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
