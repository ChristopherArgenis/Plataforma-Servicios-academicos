import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import TestConfig  # noqa: E402
from extensions import db  # noqa: E402
from factory import create_app  # noqa: E402


@pytest.fixture
def app():
    app = create_app(TestConfig)
    yield app
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, name="Ana López", email="ana@x.com", password="secreto123", pick=0):
    client.post("/register", data=dict(name=name, email=email, password=password, password2=password))
    with client.session_transaction() as s:
        pending = s.get("pending_registration")
    if not pending:
        return None
    author_id = pending["profiles"][pick]["author_id"]
    return client.post("/register/perfil", data={"author_id": author_id})


def login(client, email="ana@x.com", password="secreto123"):
    return client.post("/login", data=dict(email=email, password=password))
