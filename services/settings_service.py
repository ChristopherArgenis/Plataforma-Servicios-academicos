"""Configuración del sistema que se administra desde la página (Super Admin).

La clave de SerpAPI se busca en este orden:
  1. La que el Super Admin guardó en Configuración (cifrada en la base de datos).
  2. SERPAPI_KEY del archivo .env (respaldo del desarrollador).
"""
import base64
import hashlib
import os
import re
from datetime import datetime

import requests
from cryptography.fernet import Fernet, InvalidToken
from flask import current_app, has_app_context

from models import db
from models.user import Configuracion

SERPAPI_SETTING = 'serpapi_key'
SERPAPI_ACCOUNT_URL = 'https://serpapi.com/account.json'
KEY_PATTERN = re.compile(r'^[A-Za-z0-9]{20,128}$')


class SettingsError(Exception):
    """Error apto para mostrar al usuario."""


class SerpApiUnreachable(SettingsError):
    """No se pudo contactar a SerpAPI (red), lo que no significa que la clave sea mala."""


# ---------------- Cifrado ----------------

def _fernet():
    """Cifrado derivado de SECRET_KEY: sin ella, la clave guardada no se puede leer."""
    secret = current_app.config['SECRET_KEY'].encode()
    key = base64.urlsafe_b64encode(hashlib.sha256(b'serpapi-config:' + secret).digest())
    return Fernet(key)


def _encrypt(value):
    return _fernet().encrypt(value.encode()).decode()


def _decrypt(token):
    try:
        return _fernet().decrypt(token.encode()).decode()
    except InvalidToken:
        # Ocurre si cambió SECRET_KEY: hay que volver a capturar la clave.
        return None


# ---------------- Clave de SerpAPI ----------------

def _db_record():
    return Configuracion.query.filter_by(clave=SERPAPI_SETTING).first()


def get_serpapi_key():
    """Clave que usa la aplicación para consultar Google Scholar."""
    if not has_app_context():
        # Fuera de la app (scripts sueltos) no hay base de datos: se usa el .env
        return os.environ.get('SERPAPI_KEY', '')
    record = _db_record()
    if record:
        value = _decrypt(record.valor)
        if value:
            return value
    return os.environ.get('SERPAPI_KEY', '')


def mask(key):
    return '•' * 12 + key[-4:] if key else ''


def serpapi_status():
    """Información para mostrar en la página (nunca incluye la clave completa)."""
    record = _db_record()
    if record:
        value = _decrypt(record.valor)
        if value:
            return {
                'origen': 'configuracion',
                'mascara': mask(value),
                'actualizado_en': record.actualizado_en,
                'actualizado_por': record.autor.nombre if record.autor else None,
                'ilegible': False,
            }
    env_key = os.environ.get('SERPAPI_KEY', '')
    return {
        'origen': 'env' if env_key else 'ninguna',
        'mascara': mask(env_key),
        'actualizado_en': None,
        'actualizado_por': None,
        # Hay un registro pero no se pudo descifrar (cambió SECRET_KEY)
        'ilegible': record is not None,
    }


def probar_clave(key, timeout=10):
    """Consulta la cuenta en SerpAPI. No gasta búsquedas.

    Devuelve un dict con los datos de la cuenta, o lanza SettingsError.
    """
    try:
        resp = requests.get(SERPAPI_ACCOUNT_URL, params={'api_key': key}, timeout=timeout)
        data = resp.json()
    except (requests.RequestException, ValueError) as exc:
        raise SerpApiUnreachable('No se pudo contactar a SerpAPI. Revisa la conexión a internet del servidor.') from exc
    if resp.status_code != 200 or 'error' in data:
        raise SettingsError('SerpAPI rechazó la clave: verifica que esté bien escrita y activa.')
    return {
        'correo': data.get('account_email'),
        'plan': data.get('plan_name'),
        'busquedas_mes': data.get('searches_per_month'),
        'busquedas_restantes': data.get('total_searches_left', data.get('plan_searches_left')),
        'uso_mes': data.get('this_month_usage'),
    }


def guardar_serpapi_key(key, cliente_id, verificar=True):
    """Valida, prueba y guarda (cifrada) la clave del Super Admin.

    Devuelve los datos de la cuenta si se pudo probar, o None si no hubo conexión
    con SerpAPI (en ese caso se guarda igual; si SerpAPI la rechaza, no se guarda).
    """
    key = (key or '').strip()
    if not KEY_PATTERN.match(key):
        raise SettingsError('La clave no tiene el formato esperado (solo letras y números, sin espacios).')
    cuenta = None
    if verificar:
        try:
            cuenta = probar_clave(key)
        except SerpApiUnreachable:
            cuenta = None

    record = _db_record() or Configuracion(clave=SERPAPI_SETTING)
    record.valor = _encrypt(key)
    record.actualizado_por = cliente_id
    record.actualizado_en = datetime.now()
    db.session.add(record)
    db.session.commit()
    return cuenta


def eliminar_serpapi_key():
    record = _db_record()
    if record:
        db.session.delete(record)
        db.session.commit()
