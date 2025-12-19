from flask import Blueprint, request, jsonify, url_for, session
from services.report_service import ReportService
from services.reportlab.report_service import ReportService as PDFReportService
from models import db
import os

report = Blueprint('reports', __name__)

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

# ==========================================
# GENERACIÓN DE PDF
# ==========================================

@report.route('/Panel/Reporte/generar-pdf', methods=['POST'])
def generar_pdf():
    """Genera el PDF del informe para el cliente actual."""
    try:
        # Get cliente_id from session
        cliente_id = session.get('userID')
        
        if not cliente_id:
            # Fallback if session variable is missing but username exists
            username = session.get('username')
            if username:
                from models.user import Cliente
                client = Cliente.query.filter_by(nombre=username).first()
                if client:
                    cliente_id = client.id
                    session['userID'] = cliente_id
            
        if not cliente_id:
            return jsonify({
                'success': False,
                'message': 'Error: No se encontró la sesión del usuario. Por favor, inicia sesión nuevamente.'
            }), 401
        
        # Generate filename
        filename = f"informe_cliente_{cliente_id}.pdf"
        
        # Ensure reportes directory exists
        reportes_dir = os.path.join('static', 'reportes')
        os.makedirs(reportes_dir, exist_ok=True)
        
        filepath = os.path.join(reportes_dir, filename)
        
        # Generate PDF
        pdf_service = PDFReportService(cliente_id)
        pdf_service.generar_reporte(filepath)
        
        # Verify file was created
        if not os.path.exists(filepath):
            return jsonify({
                'success': False,
                'message': 'Error: El archivo PDF no se generó correctamente'
            }), 500
        
        return jsonify({
            'success': True,
            'message': 'Reporte generado exitosamente',
            'filename': filename,
            'download_url': url_for('static', filename=f'reportes/{filename}', _external=True)
        })
        
    except Exception as e:
        print(f"[ERROR] generar_pdf: {e}")
        return jsonify({
            'success': False,
            'message': f'Error al generar reporte: {str(e)}'
        }), 500
