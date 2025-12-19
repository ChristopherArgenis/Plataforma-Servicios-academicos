"""
InformeUpdateService - Servicio especializado para actualizaciones parciales desde la vista Informe Anual.
"""
from services.report_service import ReportService
from models import db

import json
from datetime import datetime
from models.user import (
    Libro, ArticuloInforme, Curso, ComiteJurado, Estudiante, 
    Congreso, Evento, Divulgacion, Estancia, Financiamiento, 
    Patente, Comision, Vinculacion, Distincion, Logro, Relevantes
)

class InformeUpdateService:
    def __init__(self):
        self.report_service = ReportService(db.session)

    def get_informe_data(self, cliente_id):
        """
        Recupera todos los datos necesarios para el Informe Anual de un cliente.
        """
        # Proyectos con participantes parseados
        proyectos_raw = Financiamiento.query.filter_by(cliente_id=cliente_id).all()
        proyectos = []
        for p in proyectos_raw:
            parts_list = []
            if p.participantes:
                try:
                    parts_list = json.loads(p.participantes)
                except:
                    parts_list = []
            
            proyectos.append({
                'titulo': p.titulo,
                'fuente': p.fuente,
                'clasificado': p.clasificado,
                'indole': p.indole,
                'participantes': parts_list
            })

        return {
            'investigacion': {
                'libros': Libro.query.filter_by(cliente_id=cliente_id).all(),
                'articulos': ArticuloInforme.query.filter_by(cliente_id=cliente_id).all()
            },
            'docencia': {
                'cursos': Curso.query.filter_by(cliente_id=cliente_id).all(),
                'comites': ComiteJurado.query.filter_by(cliente_id=cliente_id).all(),
                'estudiantes': Estudiante.query.filter_by(cliente_id=cliente_id).all()
            },
            'difusion': {
                'congresos': Congreso.query.filter_by(cliente_id=cliente_id).all(),
                'eventos': Evento.query.filter_by(cliente_id=cliente_id).all()
            },
            'divulgacion': Divulgacion.query.filter_by(cliente_id=cliente_id).all(),
            'patentes': Patente.query.filter_by(cliente_id=cliente_id).all(),
            'intercambio': Estancia.query.filter_by(cliente_id=cliente_id).all(),
            'proyectos': proyectos,
            'comisiones': Comision.query.filter_by(cliente_id=cliente_id).all(),
            'vinculacion': Vinculacion.query.filter_by(cliente_id=cliente_id).all(),
            'distinciones': Distincion.query.filter_by(cliente_id=cliente_id).all(),
            'logros': Logro.query.filter_by(cliente_id=cliente_id).all(),
            'relevantes': Relevantes.query.filter_by(cliente_id=cliente_id).all()
        }

    def update_section(self, section, request_form, cliente_id):
        """
        Mapea las secciones del Informe Anual a los handlers del ReportService.
        """
        # Mapeo de nombres de sección del Informe Anual a nombres de formulario del ReportService
        section_mapping = {
            'libros': 'libros',
            'articulos': 'tesis', # ArticuloInforme se maneja como 'tesis' en ReportService
            'cursos': 'cursos',
            'comites': 'comites',
            'estudiantes': 'estudiantes',
            'congresos': 'congresos',
            'eventos': 'eventos',
            'divulgacion': 'divulgacion',
            'patentes': 'patentes',
            'comisiones': 'comisiones',
            'vinculacion': 'vinculacion',
            'distinciones': 'distinciones',
            'logros': 'logros',
            'estancias': 'estancias',
            'proyectos': 'financiacion'
        }

        form_name = section_mapping.get(section)
        if not form_name:
            return False, f"Sección '{section}' no soportada para edición."

        # El ReportService usualmente espera getlist para arrays y get para strings
        # Pasamos el request_form (que es un MultiDict) directamente
        success, message = self.report_service.guardar(form_name, request_form, cliente_id)
        
        return success, message
