"""Pruebas de Configuración: clave de SerpAPI administrada por el Super Admin."""
import pytest

from models import db
from models.user import Configuracion
from services import settings_service
from services.settings_service import SettingsError
from tests.conftest import login_as

CLAVE_INSTITUCION = "a" * 60 + "WXYZ"
CLAVE_ENV = "e" * 60 + "ENV1"
CUENTA = {"correo": "admin@uni.mx", "plan": "Developer", "busquedas_mes": 5000,
          "busquedas_restantes": 4321, "uso_mes": 679}


@pytest.fixture(autouse=True)
def sin_internet(monkeypatch):
    """Simula SerpAPI: acepta CLAVE_INSTITUCION y CLAVE_ENV, rechaza lo demás."""
    def fake(key, timeout=10):
        if key in (CLAVE_INSTITUCION, CLAVE_ENV):
            return dict(CUENTA)
        raise SettingsError("SerpAPI rechazó la clave: verifica que esté bien escrita y activa.")
    monkeypatch.setattr(settings_service, "probar_clave", fake)
    monkeypatch.setenv("SERPAPI_KEY", CLAVE_ENV)


def test_only_superadmin_sees_configuration(client):
    for cliente_id in (1, 3):  # investigador y administrador
        login_as(client, cliente_id)
        assert client.get("/Panel/Configuracion").status_code == 302
        client.post("/Panel/Configuracion/serpapi", data={"serpapi_key": CLAVE_INSTITUCION})
        client.post("/logout")
    with client.application.app_context():
        assert Configuracion.query.count() == 0
    login_as(client, 4)  # super admin
    assert client.get("/Panel/Configuracion").status_code == 200


def test_sidebar_link_only_for_superadmin(client):
    login_as(client, 3)
    assert "Configuración" not in client.get("/Panel/Info?view=form").get_data(as_text=True)
    client.post("/logout")
    login_as(client, 4)
    assert "Configuración" in client.get("/Panel/Info?view=form").get_data(as_text=True)


def test_env_key_is_fallback_and_warned(client):
    login_as(client, 4)
    html = client.get("/Panel/Configuracion").get_data(as_text=True)
    assert "clave de respaldo del servidor" in html
    assert CLAVE_ENV not in html  # nunca se muestra completa


def test_superadmin_key_replaces_env_key(app, client):
    login_as(client, 4)
    resp = client.post("/Panel/Configuracion/serpapi", data={"serpapi_key": CLAVE_INSTITUCION})
    html = resp.get_data(as_text=True)
    assert "Usando la clave de la institución" in html and "4321" in html
    assert CLAVE_INSTITUCION not in html and "WXYZ" in html
    with app.app_context():
        from models.query import Query
        assert Query.api_key == CLAVE_INSTITUCION
        valor = Configuracion.query.one().valor
        assert CLAVE_INSTITUCION not in valor  # guardada cifrada


def test_invalid_key_is_not_saved(app, client):
    login_as(client, 4)
    for mala in ["corta", "con espacios " + "x" * 30, "z" * 64]:
        client.post("/Panel/Configuracion/serpapi", data={"serpapi_key": mala})
    with app.app_context():
        assert Configuracion.query.count() == 0
        from models.query import Query
        assert Query.api_key == CLAVE_ENV


def test_delete_returns_to_env_key(app, client):
    login_as(client, 4)
    client.post("/Panel/Configuracion/serpapi", data={"serpapi_key": CLAVE_INSTITUCION})
    client.post("/Panel/Configuracion/serpapi/eliminar")
    with app.app_context():
        from models.query import Query
        assert Query.api_key == CLAVE_ENV


def test_probar_shows_account(client):
    login_as(client, 4)
    html = client.post("/Panel/Configuracion/serpapi/probar").get_data(as_text=True)
    assert "admin@uni.mx" in html and "Developer" in html


def test_changed_secret_key_makes_saved_key_unreadable(app, client):
    login_as(client, 4)
    client.post("/Panel/Configuracion/serpapi", data={"serpapi_key": CLAVE_INSTITUCION})
    original = app.config["SECRET_KEY"]
    try:
        app.config["SECRET_KEY"] = "otra-clave"
        with app.app_context():
            assert settings_service.get_serpapi_key() == CLAVE_ENV
            assert settings_service.serpapi_status()["ilegible"] is True
    finally:
        app.config["SECRET_KEY"] = original


def test_key_saved_with_warning_when_serpapi_unreachable(app, client, monkeypatch):
    def sin_red(key, timeout=10):
        raise settings_service.SerpApiUnreachable("No se pudo contactar a SerpAPI.")
    monkeypatch.setattr(settings_service, "probar_clave", sin_red)
    login_as(client, 4)
    html = client.post("/Panel/Configuracion/serpapi", data={"serpapi_key": CLAVE_INSTITUCION}).get_data(as_text=True)
    assert "no se pudo verificar" in html
    with app.app_context():
        assert settings_service.get_serpapi_key() == CLAVE_INSTITUCION
