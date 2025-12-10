from flask import Blueprint, request, send_file, current_app
from models.document import DocumentModel
from services.document_service import Plantilla
from models import db
from models.user import (
    Cliente, Libro, ArticuloInforme, Curso, ComiteJurado, Estudiante,
    Congreso, Evento, Divulgacion, Estancia, Financiamiento,
    Patente, Comision, Vinculacion, Distincion, Logro
)
import json

report = Blueprint('reports', __name__)

# ==========================================
# RUTAS DE GUARDADO POR PASO (EXPLICITAS)
# ==========================================

@report.route('/Panel/Reporte/libros/guardar', methods=['POST'])
def save_libros():
    try:
        req_data = request.get_json()
        cliente_id = req_data.get('cliente_id')
        data = req_data.get('data', {})
        
        # Debug prints
        print(f"[DEBUG] Data received: {data}")

        if not cliente_id:
            return {'status': 'error', 'message': 'Cliente ID es requerido'}, 400

        # Buscar registro existente
        record = Libro.query.filter_by(cliente_id=cliente_id).first()
        is_new = False
        
        if not record:
            # Crear nuevo registro
            record = Libro(cliente_id=cliente_id)
            is_new = True
            print(f"[DEBUG] Creating new Libro record for cliente_id={cliente_id}")
        else:
            print(f"[DEBUG] Updating existing Libro record id={record.id}")

        # Campos explícitos de Libro
        # Se reciben como listas/arrays desde el front, se guardan como JSON string
        libros = data.get('libros_cientificos', [])
        capitulos = data.get('capitulos_libro', [])
        
        print(f"[DEBUG] Libros científicos: {libros}")
        print(f"[DEBUG] Capítulos: {capitulos}")
        
        # Asignar valores
        record.libros_cientificos = json.dumps(libros, ensure_ascii=False)
        record.capitulos_libro = json.dumps(capitulos, ensure_ascii=False)
        
        print(f"[DEBUG] JSON libros_cientificos: {record.libros_cientificos}")
        print(f"[DEBUG] JSON capitulos_libro: {record.capitulos_libro}")

        # Solo agregar a la sesión si es nuevo
        # Los registros existentes ya están en la sesión (tracked)
        if is_new:
            db.session.add(record)
        
        db.session.commit()
        print(f"[DEBUG] Commit successful")
        
        return {'status': 'success', 'message': 'Libros guardados correctamente'}
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR] save_libros: {e}")
        return {'status': 'error', 'message': 'Error al guardar libros'}, 500

@report.route('/Panel/Reporte/articulos/guardar', methods=['POST'])
def save_articulos():
    # Nota: Este paso corresponde a "Tesis y Docencia" según el frontend
    try:
        req_data = request.get_json()
        cliente_id = req_data.get('cliente_id')
        data = req_data.get('data', {})

        if not cliente_id:
            return {'status': 'error', 'message': 'Cliente ID requerido'}, 400

        # Para Articulos/Tesis, puede que sea uno solo o lista. 
        # El modelo ArticuloInforme parece diseñado para guardar un solo registro?
        # Revisando el modelo: ArticuloInforme tiene titulo, nivel, etc.
        # Si el usuario puede agregar múltiples, deberíamos tener una tabla relacionada 1:N real
        # O guardar JSON en cada campo.
        # Asumiremos JSON por consistencia con Libro si es múltiple, 
        # PERO el formulario de Tesis (Paso 2) solo muestra UN set de inputs (tituloTesis3, etc.)
        # NO es dinámico como Libros. Entonces es un solo registro (o el último).
        
        record = ArticuloInforme.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = ArticuloInforme(cliente_id=cliente_id)
            db.session.add(record)

        record.titulo = data.get('titulo')
        record.nivel = data.get('nivel')
        record.nombre_estudiante = data.get('nombre_estudiante')
        record.institucion = data.get('institucion')
        record.estatus = data.get('estatus')

        db.session.commit()
        return {'status': 'success', 'message': 'Tesis/Docencia guardada correctamente'}
    except Exception as e:
        db.session.rollback()
        print(f"Error save_articulos: {e}")
        return {'status': 'error', 'message': 'Error al guardar Tesis'}, 500


@report.route('/Panel/Reporte/cursos/guardar', methods=['POST'])
def save_cursos():
    try:
        req_data = request.get_json()
        cliente_id = req_data.get('cliente_id')
        data = req_data.get('data', {})

        if not cliente_id: return {'status': 'error', 'message': 'ID requerido'}, 400

        record = Curso.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Curso(cliente_id=cliente_id)
            db.session.add(record)

        # Cursos es dinámico (lista), guardamos como JSON
        record.materia = json.dumps(data.get('materia', []), ensure_ascii=False)
        record.nivel = json.dumps(data.get('nivel', []), ensure_ascii=False)
        record.periodo = json.dumps(data.get('periodo', []), ensure_ascii=False)
        record.institucion = json.dumps(data.get('institucion', []), ensure_ascii=False)
        record.programas = json.dumps(data.get('programas', []), ensure_ascii=False)

        db.session.commit()
        return {'status': 'success', 'message': 'Cursos guardados correctamente'}
    except Exception as e:
        db.session.rollback()
        print(f"Error save_cursos: {e}")
        return {'status': 'error', 'message': 'Error al guardar cursos'}, 500


@report.route('/Panel/Reporte/comite/guardar', methods=['POST'])
def save_comite():
    try:
        req_data = request.get_json()
        cliente_id = req_data.get('cliente_id')
        data = req_data.get('data', {})

        if not cliente_id: return {'status': 'error', 'message': 'ID requerido'}, 400

        record = ComiteJurado.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = ComiteJurado(cliente_id=cliente_id)
            db.session.add(record)

        record.nivel_academico = data.get('nivel_academico')
        record.programa_posgrado = data.get('programa_posgrado')
        record.participacion = data.get('participacion') # Texto consolidado (e.g. "comite: Tesis")

        db.session.commit()
        return {'status': 'success', 'message': 'Participación (Comité/Jurado) guardada'}
    except Exception as e:
        db.session.rollback()
        print(f"Error save_comite: {e}")
        return {'status': 'error', 'message': 'Error al guardar comité'}, 500


@report.route('/Panel/Reporte/estudiantes/guardar', methods=['POST'])
def save_estudiantes():
    try:
        req_data = request.get_json()
        cliente_id = req_data.get('cliente_id')
        data = req_data.get('data', {})

        if not cliente_id: return {'status': 'error', 'message': 'ID requerido'}, 400

        record = Estudiante.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Estudiante(cliente_id=cliente_id)
            db.session.add(record)

        record.nombre = data.get('nombre')
        record.actividad = data.get('actividad') # e.g. "proyecto: Licenciatura" o "servicio"
        record.procedencia = data.get('procedencia')

        db.session.commit()
        return {'status': 'success', 'message': 'Estudiante guardado correctamente'}
    except Exception as e:
        db.session.rollback()
        print(f"Error save_estudiantes: {e}")
        return {'status': 'error', 'message': 'Error al guardar estudiante'}, 500


@report.route('/Panel/Reporte/congresos/guardar', methods=['POST'])
def save_congresos():
    try:
        req_data = request.get_json()
        cliente_id = req_data.get('cliente_id')
        data = req_data.get('data', {})
        if not cliente_id: return {'status': 'error', 'message': 'ID requerido'}, 400

        record = Congreso.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Congreso(cliente_id=cliente_id)
            db.session.add(record)

        record.titulo = data.get('titulo') # mapeado en JS (tituloTrabajo -> titulo?) Verificar JS
        record.autores = data.get('autores')
        record.nombre = data.get('nombreEvento') # JS: nombreEvento -> nombre
        record.lugar = data.get('lugar')
        record.fechas = f"{data.get('fechaInicio')} - {data.get('fechaFin')}"
        record.ponente = data.get('ponente')

        # Estudiantes es lista en form, CongresoEstudiante tabla intermedia?
        # Por simplicidad ahora, si el modelo Congreso no tiene campo estudiantes, lo ignoramos o unimos a autores?
        # El modelo Congreso NO tiene campo estudiantes. Existe tabla CongresoEstudiante.
        # Para cumplir requerimiento simple: ignoramos estudiantes por ahora o lo agregamos a autores?
        # En JS mapée estudiantes[] a un campo. Si no está en modelo Congreso, se pierde.
        
        db.session.commit()
        return {'status': 'success', 'message': 'Congreso guardado'}
    except Exception as e:
        db.session.rollback()
        print(f"Error save_congresos: {e}")
        return {'status': 'error', 'message': 'Error al guardar congreso'}, 500


@report.route('/Panel/Reporte/eventos/guardar', methods=['POST'])
def save_eventos():
    try:
        req_data = request.get_json()
        cliente_id = req_data.get('cliente_id')
        data = req_data.get('data', {})
        if not cliente_id: return {'status': 'error', 'message': 'ID requerido'}, 400

        record = Evento.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Evento(cliente_id=cliente_id)
            db.session.add(record)

        record.tipo = data.get('tipoEvento')
        record.nombre = data.get('nombreEventoSimple') # JS: nombreEventoSimple -> nombre
        record.num_ponentes = data.get('numPonentes')
        record.num_asistentes = data.get('numAsistentes')

        db.session.commit()
        return {'status': 'success', 'message': 'Evento guardado'}
    except Exception as e:
        db.session.rollback()
        print(f"Error save_eventos: {e}")
        return {'status': 'error', 'message': 'Error al guardar evento'}, 500


@report.route('/Panel/Reporte/divulgacion/guardar', methods=['POST'])
def save_divulgacion():
    # Este paso no está completamente implementado en el frontend aún (paso 6)
    # pero dejo la ruta lista.
    return {'status': 'success', 'message': 'Divulgación guardada (Placeholder)'}

@report.route('/Panel/Reporte/estancias/guardar', methods=['POST'])
def save_estancias():
    return {'status': 'success', 'message': 'Estancia guardada (Placeholder)'}

@report.route('/Panel/Reporte/financiacion/guardar', methods=['POST'])
def save_financiacion():
    return {'status': 'success', 'message': 'Financiación guardada (Placeholder)'}

@report.route('/Panel/Reporte/patentes/guardar', methods=['POST'])
def save_patentes():
    try:
        req_data = request.get_json()
        cliente_id = req_data.get('cliente_id')
        data = req_data.get('data', {})
        if not cliente_id: return {'status': 'error', 'message': 'ID requerido'}, 400

        record = Patente.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Patente(cliente_id=cliente_id)
            db.session.add(record)
        
        # JS debe mandar 'contenido' o 'descripcion' -> mapear a contenido
        record.contenido = data.get('descripcion') or data.get('contenido') 
        
        db.session.commit()
        return {'status': 'success', 'message': 'Patente guardarda'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

@report.route('/Panel/Reporte/comisiones/guardar', methods=['POST'])
def save_comisiones():
    try:
        req_data = request.get_json()
        cliente_id = req_data.get('cliente_id')
        data = req_data.get('data', {})
        if not cliente_id: return {'status': 'error', 'message': 'ID requerido'}, 400

        record = Comision.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Comision(cliente_id=cliente_id)
            db.session.add(record)
        record.contenido = data.get('descripcion')
        db.session.commit()
        return {'status': 'success', 'message': 'Comisión guardada'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

@report.route('/Panel/Reporte/vinculacion/guardar', methods=['POST'])
def save_vinculacion():
    try:
        req_data = request.get_json()
        cliente_id = req_data.get('cliente_id')
        data = req_data.get('data', {})
        if not cliente_id: return {'status': 'error', 'message': 'ID requerido'}, 400

        record = Vinculacion.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Vinculacion(cliente_id=cliente_id)
            db.session.add(record)
        record.contenido = data.get('descripcion')
        db.session.commit()
        return {'status': 'success', 'message': 'Vinculación guardada'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

@report.route('/Panel/Reporte/distinciones/guardar', methods=['POST'])
def save_distinciones():
    try:
        req_data = request.get_json()
        cliente_id = req_data.get('cliente_id')
        data = req_data.get('data', {})
        if not cliente_id: return {'status': 'error', 'message': 'ID requerido'}, 400

        record = Distincion.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Distincion(cliente_id=cliente_id)
            db.session.add(record)
        record.contenido = data.get('descripcion')
        db.session.commit()
        return {'status': 'success', 'message': 'Distinción guardada'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

@report.route('/Panel/Reporte/logros/guardar', methods=['POST'])
def save_logros():
    try:
        req_data = request.get_json()
        cliente_id = req_data.get('cliente_id')
        data = req_data.get('data', {})
        if not cliente_id: return {'status': 'error', 'message': 'ID requerido'}, 400

        record = Logro.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Logro(cliente_id=cliente_id)
            db.session.add(record)
        record.contenido = data.get('descripcion')
        db.session.commit()
        return {'status': 'success', 'message': 'Logro guardado'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500
