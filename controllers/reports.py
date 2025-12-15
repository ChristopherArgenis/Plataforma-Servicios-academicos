from flask import Blueprint, request
from services.report_service import ReportService
from models import db

report = Blueprint('reports', __name__)

# ==========================================
# RUTAS DE GUARDADO - USANDO SERVICIO
# ==========================================

# ==========================================
# RUTAS DE GUARDADO - USANDO SERVICIO
# ==========================================

def _handle_save_request(collection_name):
    """
    Helper para manejar peticiones de guardado estándar.
    """
    try:
        # Usar request.form en lugar de JSON
        cliente_id = request.form.get('cliente_id')
        
        # Fallback a args si no está en form (aunque debería estar en form)
        if not cliente_id:
            cliente_id = request.args.get('cliente_id')
            
        if not cliente_id:
            return {'status': 'error', 'message': 'Cliente ID requerido'}, 400
        
        service = ReportService(db.session)
        success, message = service.guardar(collection_name, request.form, cliente_id)


        
        if success:
            return {'status': 'success', 'message': message}
        else:
            return {'status': 'error', 'message': message}, 500
            
    except Exception as e:
        print(f"[ERROR] save_{collection_name}: {e}")
        return {'status': 'error', 'message': f'Error interno: {str(e)}'}, 500

@report.route('/Panel/Reporte/libros/guardar', methods=['POST'])
def save_libros():
    return _handle_save_request('libros')

@report.route('/Panel/Reporte/articulos/guardar', methods=['POST'])
def save_articulos():
    return _handle_save_request('tesis')

@report.route('/Panel/Reporte/cursos/guardar', methods=['POST'])
def save_cursos():
    return _handle_save_request('cursos')

@report.route('/Panel/Reporte/comite/guardar', methods=['POST'])
def save_comite():
    # Maneja tanto Comités como Jurados (mismo form/tabla)
    return _handle_save_request('comites')

# Jurados eliminada por consolidación (usa save_comite)

@report.route('/Panel/Reporte/estudiantes/guardar', methods=['POST'])
def save_estudiantes():
    return _handle_save_request('estudiantes')

@report.route('/Panel/Reporte/congresos/guardar', methods=['POST'])
def save_congresos():
    return _handle_save_request('congresos')

@report.route('/Panel/Reporte/eventos/guardar', methods=['POST'])
def save_eventos():
    return _handle_save_request('eventos')

@report.route('/Panel/Reporte/divulgacion/guardar', methods=['POST'])
def save_divulgacion():
    return _handle_save_request('divulgacion')

@report.route('/Panel/Reporte/estancias/guardar', methods=['POST'])
def save_estancias():
    return _handle_save_request('estancias')

@report.route('/Panel/Reporte/financiacion/obtener', methods=['GET'])
def get_financiacion():
    try:
        updated_cliente_id = request.args.get('cliente_id')
        if not updated_cliente_id:
            return {'status': 'error', 'message': 'Cliente ID requerido'}, 400
            
        service = ReportService(db.session)
        data = service.obtener('financiacion', updated_cliente_id)
        
        return {'status': 'success', 'data': data}
    except Exception as e:
        print(f"[ERROR] get_financiacion: {e}")
        return {'status': 'error', 'message': str(e)}, 500

@report.route('/Panel/Reporte/financiacion/guardar', methods=['POST'])
def save_financiacion():
    return _handle_save_request('financiacion')

@report.route('/Panel/Reporte/patentes/guardar', methods=['POST'])
def save_patentes():
    return _handle_save_request('patentes')

@report.route('/Panel/Reporte/comisiones/guardar', methods=['POST'])
def save_comisiones():
    return _handle_save_request('comisiones')

@report.route('/Panel/Reporte/vinculacion/guardar', methods=['POST'])
def save_vinculacion():
    return _handle_save_request('vinculacion')

@report.route('/Panel/Reporte/distinciones/guardar', methods=['POST'])
def save_distinciones():
    return _handle_save_request('distinciones')

@report.route('/Panel/Reporte/logros/guardar', methods=['POST'])
def save_logros():
    return _handle_save_request('logros')
