import logging
import os
import secrets

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))

log = logging.getLogger(__name__)


def _secret_key():
    key = os.environ.get("SECRET_KEY")
    if key:
        return key
    # Sin clave fija las sesiones se pierden al reiniciar; útil solo en desarrollo.
    log.warning("SECRET_KEY no está definida: se usa una clave temporal.")
    return secrets.token_hex(32)


class Config:
    SECRET_KEY = _secret_key()

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        "sqlite:///" + os.path.join(basedir, "instance", "plataforma.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")
    SCHOLAR_PROVIDER = os.environ.get("SCHOLAR_PROVIDER", "serpapi").lower()

    # Bootstrap se sirve desde la propia app (funciona sin internet).
    BOOTSTRAP_SERVE_LOCAL = True

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE") == "1"
    TRUST_PROXY = os.environ.get("TRUST_PROXY") == "1"

    ARTICLES_PER_PAGE = 20

    # Tamaño máximo de una petición (p. ej. la imagen de la firma)
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = "test"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SCHOLAR_PROVIDER = "demo"
