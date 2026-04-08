import json


def test_listar_eventos_vacio(client):
    r = client.get('/api/eventos')
    assert r.status_code == 200
    assert r.get_json() == []


def test_crear_usuario_y_login(client):
    r = client.post(
        '/api/admin/usuarios',
        data=json.dumps({
            'nombre': 'Test',
            'email': 'test@test.com',
            'password': 'secret123',
            'rol': 'asistente',
        }),
        content_type='application/json',
    )
    assert r.status_code == 201

    r = client.post(
        '/api/login',
        data=json.dumps({'email': 'test@test.com', 'password': 'secret123'}),
        content_type='application/json',
    )
    assert r.status_code == 200
    data = r.get_json()
    assert 'token' in data
    assert data['rol'] == 'asistente'


def test_login_credenciales_invalidas(client):
    r = client.post(
        '/api/login',
        data=json.dumps({'email': 'nada@test.com', 'password': 'x'}),
        content_type='application/json',
    )
    assert r.status_code == 401


def test_crear_evento_y_listar(client):
    r = client.post(
        '/api/eventos',
        data=json.dumps({
            'nombre': 'Conferencia',
            'descripcion': 'Desc',
            'fecha': '2026-06-01',
            'capacidad_max': 50,
        }),
        content_type='application/json',
    )
    assert r.status_code == 201
    evento_id = r.get_json()['id']

    r = client.get('/api/eventos')
    assert r.status_code == 200
    lista = r.get_json()
    assert len(lista) == 1
    assert lista[0]['nombre'] == 'Conferencia'
    assert lista[0]['id'] == evento_id


def test_obtener_evento(client):
    client.post(
        '/api/eventos',
        data=json.dumps({'nombre': 'E1', 'capacidad_max': 10}),
        content_type='application/json',
    )
    r = client.get('/api/eventos/1')
    assert r.status_code == 200
    assert r.get_json()['nombre'] == 'E1'


def test_registrar_asistente(client):
    client.post(
        '/api/admin/usuarios',
        data=json.dumps({
            'nombre': 'Asistente',
            'email': 'a@a.com',
            'password': 'p',
            'rol': 'asistente',
        }),
        content_type='application/json',
    )
    client.post(
        '/api/eventos',
        data=json.dumps({'nombre': 'Meetup', 'capacidad_max': 5}),
        content_type='application/json',
    )
    r = client.post(
        '/api/eventos/1/registrar',
        data=json.dumps({'usuario_id': 1}),
        content_type='application/json',
    )
    assert r.status_code == 201

    r = client.get('/api/eventos/1')
    assert len(r.get_json()['asistentes']) == 1


def test_listar_usuarios(client):
    client.post(
        '/api/admin/usuarios',
        data=json.dumps({
            'nombre': 'U1',
            'email': 'u1@u.com',
            'password': 'p',
        }),
        content_type='application/json',
    )
    r = client.get('/api/admin/usuarios')
    assert r.status_code == 200
    assert len(r.get_json()) == 1


def test_flujo_evento_lleno_rechaza_registro(client):
    client.post(
        '/api/admin/usuarios',
        data=json.dumps({
            'nombre': 'P1',
            'email': 'p1@test.com',
            'password': 'x',
            'rol': 'asistente',
        }),
        content_type='application/json',
    )
    client.post(
        '/api/admin/usuarios',
        data=json.dumps({
            'nombre': 'P2',
            'email': 'p2@test.com',
            'password': 'x',
            'rol': 'asistente',
        }),
        content_type='application/json',
    )
    client.post(
        '/api/eventos',
        data=json.dumps({'nombre': 'Mini', 'capacidad_max': 1}),
        content_type='application/json',
    )
    assert client.post(
        '/api/eventos/1/registrar',
        data=json.dumps({'usuario_id': 1}),
        content_type='application/json',
    ).status_code == 201
    r = client.post(
        '/api/eventos/1/registrar',
        data=json.dumps({'usuario_id': 2}),
        content_type='application/json',
    )
    assert r.status_code == 400


def test_registro_duplicado_rechaza(client):
    client.post(
        '/api/admin/usuarios',
        data=json.dumps({
            'nombre': 'Solo',
            'email': 'solo@test.com',
            'password': 'x',
            'rol': 'asistente',
        }),
        content_type='application/json',
    )
    client.post(
        '/api/eventos',
        data=json.dumps({'nombre': 'Ev', 'capacidad_max': 10}),
        content_type='application/json',
    )
    assert client.post(
        '/api/eventos/1/registrar',
        data=json.dumps({'usuario_id': 1}),
        content_type='application/json',
    ).status_code == 201
    r = client.post(
        '/api/eventos/1/registrar',
        data=json.dumps({'usuario_id': 1}),
        content_type='application/json',
    )
    assert r.status_code == 400
