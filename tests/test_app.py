from extensions import db
from models import Article, User
from services.scholar import ScholarError, parse_article
from tests.conftest import login, register


def test_register_imports_articles_and_logs_in(app, client):
    resp = register(client)
    assert resp.status_code == 302 and resp.location.endswith("/panel")
    with app.app_context():
        user = User.query.one()
        assert user.articles.count() > 0
        assert user.password_hash != "secreto123"
    assert b"Bienvenido" in client.get("/panel").data


def test_register_validation(client):
    resp = client.post("/register", data=dict(name="A", email="mal", password="123", password2="456"),
                       follow_redirects=True)
    html = resp.data.decode()
    assert "correo no es válido" in html and "al menos 8" in html and "no coinciden" in html


def test_register_duplicate_email(client):
    register(client)
    client.post("/logout")
    resp = client.post("/register", data=dict(name="Otra", email="ana@x.com", password="secreto123",
                                              password2="secreto123"), follow_redirects=True)
    assert "ya está registrado" in resp.data.decode()


def test_register_without_profiles_does_not_crash(client, monkeypatch):
    monkeypatch.setattr("services.scholar.DemoScholar.search_profiles", lambda self, n: [])
    resp = client.post("/register", data=dict(name="Nadie", email="n@x.com", password="secreto123",
                                              password2="secreto123"), follow_redirects=True)
    assert resp.status_code == 200 and "No se encontraron perfiles" in resp.data.decode()


def test_register_scholar_error_is_shown(client, monkeypatch):
    def boom(self, n):
        raise ScholarError("Servicio caído")
    monkeypatch.setattr("services.scholar.DemoScholar.search_profiles", boom)
    resp = client.post("/register", data=dict(name="X", email="x@x.com", password="secreto123",
                                              password2="secreto123"), follow_redirects=True)
    assert "Servicio caído" in resp.data.decode()


def test_register_with_zero_articles_succeeds(app, client, monkeypatch):
    monkeypatch.setattr("services.scholar.DemoScholar.get_articles", lambda self, a: [])
    resp = register(client)
    assert resp.location.endswith("/panel")
    with app.app_context():
        assert User.query.count() == 1


def test_profile_must_come_from_search_results(app, client):
    client.post("/register", data=dict(name="Ana", email="ana@x.com", password="secreto123",
                                       password2="secreto123"))
    client.post("/register/perfil", data={"author_id": "INVENTADO"})
    with app.app_context():
        assert User.query.count() == 0


def test_parse_article_handles_missing_fields():
    assert parse_article({"title": "Sin id"}) is None
    art = parse_article({"title": "T", "citation_id": "c1", "year": "", "cited_by": {"value": None}})
    assert art["year"] is None and art["cited_by"] == 0


def test_login_requires_matching_email_and_password(client):
    register(client, name="Ana", email="ana@x.com")
    client.post("/logout")
    register(client, name="Beto", email="beto@x.com")
    client.post("/logout")
    assert login(client, "ana@x.com", "incorrecta").location.endswith("/")
    assert login(client, "ana@x.com", "secreto123").location.endswith("/panel")


def test_panel_requires_login(client):
    assert client.get("/panel").status_code == 302


def test_logout_clears_session(client):
    register(client)
    client.post("/logout")
    with client.session_transaction() as s:
        assert "_user_id" not in s
    assert client.get("/panel").status_code == 302


def test_sql_injection_does_not_leak_other_users(app, client):
    register(client, name="Ana", email="ana@x.com")
    client.post("/logout")
    register(client, name="Beto", email="beto@x.com")
    with app.app_context():
        ana_titles = {a.title for a in User.query.filter_by(email="ana@x.com").one().articles}
        beto_titles = {a.title for a in User.query.filter_by(email="beto@x.com").one().articles}
    only_ana = ana_titles - beto_titles
    for payload in ['" OR 1=1 --', "' OR '1'='1", 'abc"def', "100%", "_"]:
        resp = client.get("/panel", query_string={"titulo": payload})
        assert resp.status_code == 200
        assert not any(t in resp.data.decode() for t in only_ana)


def test_filters_and_pagination(app, client):
    register(client)
    with app.app_context():
        art = Article.query.filter(Article.year.isnot(None)).first()
        year, word = art.year, art.title.split()[0]
    resp = client.get("/panel", query_string={"year": year, "titulo": word, "page": 999})
    assert resp.status_code == 200
    assert client.get("/panel", query_string={"year": "abc"}).status_code == 200


def test_acquire_only_touches_own_articles(app, client):
    register(client, name="Ana", email="ana@x.com")
    client.post("/logout")
    register(client, name="Beto", email="beto@x.com")
    with app.app_context():
        ana_art = User.query.filter_by(email="ana@x.com").one().articles.first().id
        beto_arts = [a.id for a in User.query.filter_by(email="beto@x.com").one().articles.limit(3)]
    data = {"visible_ids": [str(i) for i in beto_arts + [ana_art]],
            "keys": [str(beto_arts[0]), str(ana_art)]}
    client.post("/panel/adquirir", data=data)
    with app.app_context():
        assert db.session.get(Article, beto_arts[0]).selected
        assert not db.session.get(Article, beto_arts[1]).selected
        assert not db.session.get(Article, ana_art).selected
    client.post(f"/panel/quitar/{beto_arts[0]}")
    with app.app_context():
        assert not db.session.get(Article, beto_arts[0]).selected


def test_csrf_enabled_outside_tests():
    from config import Config
    from factory import create_app

    class Cfg(Config):
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    client = create_app(Cfg).test_client()
    assert client.post("/login", data={"email": "a@x.com", "password": "x"}).status_code == 400


def test_404_page(client):
    assert client.get("/no-existe").status_code == 404


def test_seed_demo_command(app):
    result = app.test_cli_runner().invoke(args=["seed-demo"])
    assert "demo@ejemplo.com" in result.output
    with app.app_context():
        assert User.query.count() == 3
        assert Article.query.filter_by(selected=True).count() > 0
