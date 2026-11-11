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

@information_bp.route('/Panel/Info/UpdateName', methods=['POST'])
def update_name():
    if 'username' not in session:
        return {'status': 'error', 'message': 'No autorizado'}, 401
    
    req_data = request.get_json()
    new_name = req_data.get('nombre')
    
    if not new_name:
        return {'status': 'error', 'message': 'Nombre requerido'}, 400
        
    success, msg = InfoService.update_nombre_cliente(session['username'], new_name)
    
    if success:
        # Actualizar sesión también para que se refleje de inmediato si se usa session['username']
        session['username'] = new_name
        return {'status': 'success', 'message': msg}
    else:
        return {'status': 'error', 'message': msg}, 500
