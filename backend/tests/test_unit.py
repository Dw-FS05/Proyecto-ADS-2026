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
    d = u.to_dict()
    assert d == {
        'id': 12,
        'nombre': 'Ana',
        'email': 'ana@test.com',
        'rol': 'organizador',
    }


def test_usuario_password_set_and_check(ctx):
    u = Usuario(nombre='B', email='b@test.com')
    u.set_password('clave123')
    assert u.check_password('clave123')
    assert u.check_password('clave123') is True
    assert u.check_password('otra') is False


def test_evento_to_dict_sin_asistentes(ctx):
    e = Evento(nombre='Summit', descripcion='Desc', fecha='2026-01-01', capacidad_max=100)
    e.id = 3
    d = e.to_dict()
    assert d['id'] == 3
    assert d['nombre'] == 'Summit'
    assert d['descripcion'] == 'Desc'
    assert d['fecha'] == '2026-01-01'
    assert d['capacidad_max'] == 100
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
    assert len(d['asistentes']) == 1
    assert d['asistentes'][0]['email'] == 'c@test.com'
