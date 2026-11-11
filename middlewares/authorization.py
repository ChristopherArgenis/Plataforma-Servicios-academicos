"""Utilidades de autorización: quién es el usuario actual y qué puede hacer.

El identificador del cliente SIEMPRE se toma de la sesión del servidor,
nunca de lo que manda el navegador (formularios o parámetros de la URL).
"""
from functools import wraps

from flask import flash, redirect, session, url_for

from models import db
from models.user import Cliente

# Roles: 0 = sin acceso, 1 = investigador, 2 = administrador, 3 = super admin
ROL_ADMIN = 2


def current_cliente_id():
    """Devuelve el id del cliente con sesión iniciada, o None."""
    cliente_id = session.get('userID')
    if cliente_id:
        return cliente_id
    username = session.get('username')
    if username:
        cliente = Cliente.query.filter_by(nombre=username).first()
        if cliente:
            session['userID'] = cliente.id
            return cliente.id
    return None


def current_cliente():
    cliente_id = current_cliente_id()
    return db.session.get(Cliente, cliente_id) if cliente_id else None


def admin_required(view):
    """Permite el acceso solo a administradores (rol >= 2).

    El rol se lee de la base de datos en cada petición, así un cambio de rol
    se aplica de inmediato aunque la sesión sea antigua.
    """
    @wraps(view)
    def wrapper(*args, **kwargs):
        cliente = current_cliente()
        if not cliente or (cliente.rol or 0) < ROL_ADMIN:
            flash("Acceso denegado: se requieren permisos de administrador.", "danger")
            return redirect(url_for('panel.panel_get'))
        return view(*args, **kwargs)
    return wrapper


def can_manage(actor, target_rol):
    """Un administrador no puede crear, cambiar ni borrar cuentas de rol mayor al suyo."""
    try:
        return int(target_rol or 0) <= (actor.rol or 0)
    except (TypeError, ValueError):
        return False
