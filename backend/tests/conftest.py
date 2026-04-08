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
