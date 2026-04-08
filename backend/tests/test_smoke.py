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
