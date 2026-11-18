from flask import Blueprint, request, jsonify, url_for, current_app, send_file, abort
from services.report_service import ReportService
from services.reportlab.report_service import ReportService as PDFReportService
from middlewares.authorization import current_cliente_id
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
        # El cliente siempre es el de la sesión (se ignora cualquier cliente_id
        # enviado por el navegador, para que nadie modifique datos de otro).
        cliente_id = current_cliente_id()
        if not cliente_id:
            return {'status': 'error', 'message': 'Sesión no válida. Inicia sesión nuevamente.'}, 401
        
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
        # Solo se consultan los datos del cliente con sesión iniciada
        updated_cliente_id = current_cliente_id()
        if not updated_cliente_id:
            return {'status': 'error', 'message': 'Sesión no válida. Inicia sesión nuevamente.'}, 401
            
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

def _report_path(cliente_id):
    """Ruta privada del PDF de un cliente (fuera de static/, no accesible por URL)."""
    reportes_dir = current_app.config['REPORTS_DIR']
    os.makedirs(reportes_dir, exist_ok=True)
    return os.path.join(reportes_dir, f"informe_cliente_{int(cliente_id)}.pdf")


@report.route('/Panel/Reporte/generar-pdf', methods=['POST'])
def generar_pdf():
    """Genera el PDF del informe para el cliente actual."""
    try:
        cliente_id = current_cliente_id()
        if not cliente_id:
            return jsonify({
                'success': False,
                'message': 'Error: No se encontró la sesión del usuario. Por favor, inicia sesión nuevamente.'
            }), 401

        filepath = _report_path(cliente_id)

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
            'filename': os.path.basename(filepath),
            # Ruta protegida: solo entrega el informe del usuario con sesión
            'download_url': url_for('reports.descargar_pdf')
        })

    except Exception as e:
        print(f"[ERROR] generar_pdf: {e}")
        return jsonify({
            'success': False,
            'message': f'Error al generar reporte: {str(e)}'
        }), 500


@report.route('/Panel/Reporte/informe.pdf', methods=['GET'])
def descargar_pdf():
    """Entrega el PDF del informe SOLO a su dueño (el usuario con sesión)."""
    cliente_id = current_cliente_id()
    if not cliente_id:
        abort(401)
    filepath = _report_path(cliente_id)
    if not os.path.exists(filepath):
        PDFReportService(cliente_id).generar_reporte(filepath)
    resp = send_file(
        filepath,
        mimetype='application/pdf',
        as_attachment=request.args.get('descargar') == '1',
        download_name=f"informe_anual_{cliente_id}.pdf",
        max_age=0,
    )
    resp.headers['Cache-Control'] = 'private, no-store'
    return resp
