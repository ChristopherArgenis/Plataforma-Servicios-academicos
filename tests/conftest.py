"""Configuración de pruebas: usa una base de datos temporal, nunca tu data.db."""
import os
import sys
import tempfile

import pytest

_tmp = tempfile.mkdtemp(prefix="plataforma-tests-")
os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(_tmp, "test.db")
os.environ["REPORTS_DIR"] = os.path.join(_tmp, "reportes")
os.environ["SECRET_KEY"] = "clave-de-pruebas"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app  # noqa: E402
from models import db  # noqa: E402
from models.user import Articles_Keys, Cliente, Usuario  # noqa: E402


@pytest.fixture
def app():
    flask_app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
        clientes = [
            Cliente(id=1, rol=1, nombre="Ana Investigadora", email="ana@x.com"),
            Cliente(id=2, rol=1, nombre="Beto Investigador", email="beto@x.com"),
            Cliente(id=3, rol=2, nombre="Carla Admin", email="carla@x.com"),
            Cliente(id=4, rol=3, nombre="Diego Super", email="diego@x.com"),
        ]
        for c in clientes:
            c.set_password("secreto123")
            db.session.add(c)
        db.session.add_all([
            Usuario(id=1, profile_id="PERFIL_ANA", affilition="UABC", cited_by=10),
            Usuario(id=2, profile_id="PERFIL_BETO", affilition="UNAM", cited_by=5),
            Articles_Keys(title="Articulo de Ana", id_Articles="ana:1", year=2024, profile_id="PERFIL_ANA"),
            Articles_Keys(title="Secreto de Beto", id_Articles="beto:1", year=2024, profile_id="PERFIL_BETO"),
        ])
        db.session.commit()
    yield flask_app
    flask_app.config.update(WTF_CSRF_ENABLED=True)


@pytest.fixture
def client(app):
    return app.test_client()


def login_as(client, cliente_id):
    """Inicia sesión como lo hace /login (mismas claves de sesión)."""
    with client.application.app_context():
        c = db.session.get(Cliente, cliente_id)
        u = db.session.get(Usuario, cliente_id)
        nombre, rol = c.nombre, c.rol
        key = u.profile_id if u else None
    with client.session_transaction() as s:
        s["username"] = nombre
        s["userID"] = cliente_id
        s["CustomerRol"] = rol
        if key:
            s["scholarKey"] = key
