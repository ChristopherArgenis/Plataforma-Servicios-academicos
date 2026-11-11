import logging
import os
import secrets

from dotenv import load_dotenv

# Determine the absolute path of the directory this script is in
basedir = os.path.abspath(os.path.dirname(__file__))

# Lee las variables del archivo .env (claves y configuración privada)
load_dotenv(os.path.join(basedir, '.env'))


def _secret_key():
    key = os.environ.get('SECRET_KEY')
    if key:
        return key
    # Sin una clave fija las sesiones se cierran al reiniciar; solo sirve para desarrollo.
    logging.getLogger(__name__).warning(
        "SECRET_KEY no está definida en .env: se usa una clave temporal."
    )
    return secrets.token_hex(32)


class Config:
    # Clave para firmar las sesiones (se define en .env)
    SECRET_KEY = _secret_key()

    # Base de datos: por defecto 'data.db' en la carpeta del proyecto
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or (
        'sqlite:///' + os.path.join(basedir, 'data.db')
    )

    # Disable modification tracking to save memory (not necessary for most cases)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Carpeta privada para los PDF generados (no es accesible desde el navegador)
    REPORTS_DIR = os.environ.get('REPORTS_DIR') or os.path.join(basedir, 'instance', 'reportes')

    # Cookies de sesión
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE') == '1'
