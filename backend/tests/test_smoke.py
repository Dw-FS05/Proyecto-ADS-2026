from app import app


def test_app_carga():
    assert app is not None
    assert app.name == 'app'


def test_get_eventos_responde_200(client):
    r = client.get('/api/eventos')
    assert r.status_code == 200
    body = r.get_json()
    assert isinstance(body, list)


def test_login_endpoint_responde(client):
    r = client.post('/api/login', json={'email': 'noexiste@x.com', 'password': 'x'})
    assert r.status_code == 401


def test_listar_usuarios_responde(client):
    r = client.get('/api/admin/usuarios')
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)
