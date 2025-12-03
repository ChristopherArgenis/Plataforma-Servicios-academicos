from flask import Blueprint, request, redirect, url_for, flash, session
from services.info_service import InfoService

information_bp = Blueprint('information', __name__)

@information_bp.route('/Panel/Info/Save', methods=['POST'])
def save_info():
    if 'username' not in session:
        return redirect(url_for('reg_log.login'))

    # Recopilar datos del formulario
    data = {
        'sni': request.form.get('sni'),
        'pride': request.form.get('pride'),
        'departamento': request.form.get('departamento'),
        'categoria': request.form.get('categoria')
    }

    # Usar el servicio para guardar los datos
    success, message = InfoService.save_informacion_academica(session['username'], data)

    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')

    return redirect(url_for('panel.panel_info', view='form'))
