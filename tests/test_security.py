"""Pruebas de las correcciones de seguridad."""
import os

from models import db
from models.user import Cliente, Financiamiento, Libro
from tests.conftest import login_as

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# 1. Los PDF del informe ya no son públicos -------------------------------

def test_pdf_is_private_and_only_for_its_owner(app, client):
    login_as(client, 1)
    resp = client.post("/Panel/Reporte/generar-pdf")
    data = resp.get_json()
    assert data["success"] is True
    assert data["download_url"] == "/Panel/Reporte/informe.pdf"
    assert "/static/" not in data["download_url"]
    # El archivo queda en la carpeta privada, no en static/
    assert os.path.exists(os.path.join(app.config["REPORTS_DIR"], "informe_cliente_1.pdf"))

    pdf = client.get("/Panel/Reporte/informe.pdf")
    assert pdf.status_code == 200 and pdf.data.startswith(b"%PDF")
    assert b"Ana Investigadora" in pdf.data or pdf.mimetype == "application/pdf"

    # Sin sesión no se puede descargar
    client.post("/logout")
    assert client.get("/Panel/Reporte/informe.pdf").status_code == 302


def test_pdf_download_never_serves_another_client(app, client):
    login_as(client, 2)
    client.post("/Panel/Reporte/generar-pdf")
    # Aunque se intente pedir el de otro cliente, se entrega el propio
    resp = client.get("/Panel/Reporte/informe.pdf?cliente_id=1")
    assert "informe_anual_2.pdf" in resp.headers["Content-Disposition"]


def test_old_public_reports_are_blocked(client):
    assert client.get("/static/reportes/informe_cliente_1.pdf").status_code == 404
    login_as(client, 1)
    assert client.get("/static/reportes/informe_cliente_1.pdf").status_code == 404


# 2. El cliente_id se toma de la sesión -----------------------------------

def test_save_ignores_cliente_id_sent_by_browser(app, client):
    login_as(client, 1)
    resp = client.post("/Panel/Reporte/libros/guardar", data={
        "cliente_id": "2",  # intento de escribir en los datos de Beto
        "librosCientificos[]": ["Libro de Ana"],
        "capitulosLibro[]": [""],
    })
    assert resp.get_json()["status"] == "success"
    with app.app_context():
        assert Libro.query.filter_by(cliente_id=2).count() == 0
        assert Libro.query.filter_by(cliente_id=1).one().libros_cientificos == "Libro de Ana"


def test_read_ignores_cliente_id_sent_by_browser(app, client):
    with app.app_context():
        db.session.add(Financiamiento(cliente_id=2, titulo="Proyecto secreto de Beto"))
        db.session.commit()
    login_as(client, 1)
    resp = client.get("/Panel/Reporte/financiacion/obtener?cliente_id=2")
    assert "Proyecto secreto de Beto" not in resp.get_data(as_text=True)


def test_save_requires_session(client):
    resp = client.post("/Panel/Reporte/libros/guardar", data={"cliente_id": "1"})
    assert resp.status_code == 302  # redirige al inicio de sesión


# 3. Administración con control de rol ------------------------------------

def test_researcher_cannot_use_admin(app, client):
    login_as(client, 1)
    assert client.get("/Administracion?table=Cliente").status_code == 302
    with client.session_transaction() as s:
        s["nameTable"] = "Cliente"
    client.post("/Admin/crear", data={"rol": "3", "name": "Intruso", "email": "i@x.com", "password": "x"})
    client.post("/Admin/actualizar", data={"update-id": "1", "rol": "3"})
    client.post("/Admin/eliminar", data={"delete-id": "2"})
    with app.app_context():
        assert Cliente.query.filter_by(nombre="Intruso").count() == 0
        assert db.session.get(Cliente, 1).rol == 1
        assert db.session.get(Cliente, 2) is not None


def test_admin_cannot_escalate_or_touch_higher_roles(app, client):
    login_as(client, 3)  # administrador (rol 2)
    assert client.get("/Administracion?table=Cliente").status_code == 200
    client.post("/Admin/crear", data={"rol": "3", "name": "Nuevo Super", "email": "n@x.com", "password": "x"})
    client.post("/Admin/actualizar", data={"update-id": "1", "rol": "3"})
    client.post("/Admin/actualizar", data={"update-id": "4", "rol": "1"})
    client.post("/Admin/eliminar", data={"delete-id": "4"})
    client.post("/Admin/eliminar", data={"delete-id": "3"})  # su propia cuenta
    with app.app_context():
        assert Cliente.query.filter_by(nombre="Nuevo Super").count() == 0
        assert db.session.get(Cliente, 1).rol == 1
        assert db.session.get(Cliente, 4).rol == 3
        assert db.session.get(Cliente, 3) is not None


def test_admin_can_manage_lower_roles(app, client):
    login_as(client, 3)
    client.post("/Admin/actualizar", data={"update-id": "1", "rol": "2"})
    with app.app_context():
        assert db.session.get(Cliente, 1).rol == 2


def test_demoted_admin_loses_access_immediately(app, client):
    login_as(client, 3)
    with app.app_context():
        db.session.get(Cliente, 3).rol = 1
        db.session.commit()
    assert client.get("/Administracion?table=Cliente").status_code == 302


# 4 y 5. Sin modo debug y sin claves en el código --------------------------

def test_debug_off_and_no_secrets_in_code(app):
    assert app.debug is False
    with open(os.path.join(ROOT, "app.py"), encoding="utf-8") as f:
        assert "eyJhbGciOi" not in f.read()
    with open(os.path.join(ROOT, "models", "query.py"), encoding="utf-8") as f:
        assert "3f62fef4ad58" not in f.read()


def test_serpapi_key_comes_from_environment(monkeypatch):
    from models.query import Query
    monkeypatch.setenv("SERPAPI_KEY", "clave-desde-env")
    assert Query.api_key == "clave-desde-env"


# 6. Sin inyección SQL en los filtros de Adquisición ------------------------

def test_sql_injection_in_title_filter(client):
    login_as(client, 1)
    for payload in ['" OR 1=1 --', "' OR '1'='1", 'abc"def', "%", "_"]:
        resp = client.post("/Panel", data={"titulo": payload, "year": ""})
        assert resp.status_code == 200, payload
        assert "Secreto de Beto" not in resp.get_data(as_text=True), payload


def test_title_filter_still_works(client):
    login_as(client, 1)
    html = client.post("/Panel", data={"titulo": "Articulo", "year": "2024"}).get_data(as_text=True)
    assert "Articulo de Ana" in html


# 7. CSRF -------------------------------------------------------------------

def test_csrf_blocks_posts_without_token(app, client):
    app.config["WTF_CSRF_ENABLED"] = True
    login_as(client, 1)
    assert client.post("/Panel/Reporte/libros/guardar", data={}).status_code == 400
    assert client.post("/login", data={"email": "ana@x.com", "password": "secreto123"}).status_code == 400


def test_pages_include_csrf_token(client):
    html = client.get("/").get_data(as_text=True)
    assert 'name="csrf-token"' in html and "csrf.js" in html


# 8. Logout borra toda la sesión --------------------------------------------

def test_logout_clears_whole_session(client):
    login_as(client, 1)
    client.post("/logout")
    with client.session_transaction() as s:
        assert dict(s) == {}
