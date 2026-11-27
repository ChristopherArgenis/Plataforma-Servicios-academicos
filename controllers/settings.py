"""Configuración del sistema (solo Super Admin): clave de SerpAPI."""
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from middlewares.authorization import current_cliente, superadmin_required
from services import settings_service
from services.settings_service import SettingsError

settings_bp = Blueprint('settings', __name__)


def _render(cuenta=None):
    context = {
        'user': session.get('username'),
        'rol': current_cliente().rol,
        'active_page': 'configuracion',
        'serpapi': settings_service.serpapi_status(),
        'cuenta': cuenta,
    }
    if request.headers.get('HX-Request'):
        return render_template('partials/configuracion.html', **context)
    return render_template('base_panel.html', **context)


@settings_bp.route('/Panel/Configuracion', methods=['GET'])
@superadmin_required
def configuracion():
    return _render()


@settings_bp.route('/Panel/Configuracion/serpapi', methods=['POST'])
@superadmin_required
def guardar_serpapi():
    try:
        cuenta = settings_service.guardar_serpapi_key(
            request.form.get('serpapi_key'), current_cliente().id
        )
    except SettingsError as exc:
        flash(str(exc), 'danger')
        return redirect(url_for('settings.configuracion'))
    if cuenta:
        flash('Clave de SerpAPI guardada. A partir de ahora las consultas usan esta cuenta.', 'success')
    else:
        flash('Clave guardada, pero no se pudo verificar porque el servidor no logró contactar '
              'a SerpAPI. Usa "Probar clave" cuando haya conexión.', 'warning')
    return _render(cuenta)


@settings_bp.route('/Panel/Configuracion/serpapi/probar', methods=['POST'])
@superadmin_required
def probar_serpapi():
    key = settings_service.get_serpapi_key()
    if not key:
        flash('No hay ninguna clave configurada.', 'warning')
        return redirect(url_for('settings.configuracion'))
    try:
        cuenta = settings_service.probar_clave(key)
    except SettingsError as exc:
        flash(str(exc), 'danger')
        return redirect(url_for('settings.configuracion'))
    flash('La clave funciona correctamente.', 'success')
    return _render(cuenta)


@settings_bp.route('/Panel/Configuracion/serpapi/eliminar', methods=['POST'])
@superadmin_required
def eliminar_serpapi():
    settings_service.eliminar_serpapi_key()
    flash('Clave eliminada de la configuración.', 'info')
    return redirect(url_for('settings.configuracion'))
