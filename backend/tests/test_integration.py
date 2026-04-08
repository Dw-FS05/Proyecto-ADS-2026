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
