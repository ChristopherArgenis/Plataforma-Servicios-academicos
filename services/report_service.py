"""
ReportService - Servicio centralizado para manejo de reportes académicos
Implementa la metodología arquitectónica definida para el proyecto
"""
import json
from models import db
from models.user import (
    Libro, ArticuloInforme, Curso, Congreso, Evento,
    ComiteJurado, Estudiante, Financiamiento, Patente, Comision,
    Vinculacion, Distincion, Logro, Divulgacion, Estancia
)
# Nota: Jurado se elimina de imports ya que se usa ComiteJurado para todo.

class ReportService:
    """
    Servicio centralizado para manejo de reportes académicos.
    UNA SOLA INSTANCIA POR REQUEST.
    """
    
    def __init__(self, db_session):
        self.db = db_session
        
        # Diccionario de handlers para cada formulario
        self._form_handlers = {
            'libros': self._guardar_libros,
            'tesis': self._guardar_tesis,
            'cursos': self._guardar_cursos,
            'comites': self._guardar_comites, # Maneja Comites Y Jurados
            'estudiantes': self._guardar_estudiantes, # Separado
            'congresos': self._guardar_congresos,
            'eventos': self._guardar_eventos,
            'financiacion': self._guardar_financiacion,
            'patentes': self._guardar_patentes,
            'comisiones': self._guardar_comisiones,
            'vinculacion': self._guardar_vinculacion,
            'distinciones': self._guardar_distinciones,
            'logros': self._guardar_logros,
            'divulgacion': self._guardar_divulgacion,
            'estancias': self._guardar_estancias,
        }
    
    # ========================================
    # MÉTODOS PÚBLICOS
    # ========================================
    
    def guardar(self, form_name, data, cliente_id):
        handler = self._form_handlers.get(form_name)
        if not handler:
            return False, f"Formulario '{form_name}' no reconocido"
        
        try:
            handler(data, cliente_id)
            self.db.commit()
            return True, "Datos guardados correctamente"
            
        except ValueError as e:
            self.db.rollback()
            return False, str(e)
            
        except Exception as e:
            self.db.rollback()
            print(f"[ERROR] ReportService.guardar({form_name}): {e}")
            return False, f"Error al guardar: {str(e)}"
    
    def obtener(self, collection_name, cliente_id):
        """
        Recupera datos para precargar formularios o mostrar resúmenes.
        """
        data = {}
        
        if collection_name == 'financiacion':
            records = Financiamiento.query.filter_by(cliente_id=cliente_id).all()
            data = []  # Start as list
            if records:
                for record in records:
                    # Reconstruir lista de participantes si es JSON
                    participantes = []
                    if record.participantes:
                        try:
                            # If it's already a JSON string in DB, we keep it as list for frontend?
                            # Frontend expects list of objects in 'participantesLista' key
                            participantes = json.loads(record.participantes)
                        except:
                            # Fallback
                            participantes = [{'nombre': record.participantes, 'tipo': 'N/A', 'institucion': ''}]
                    
                    data.append({
                        'tituloFinanciacion': record.titulo,
                        'fuenteFinanciamiento': record.fuente,
                        'clasificacionFinanciacion': record.clasificado,
                        'indoleFinanciacion': record.indole,
                        'participantesLista': participantes
                    })
        
        return data  # Retorna dict vacío si no hay datos
    
    # ========================================
    # MÉTODOS PRIVADOS (Patrón Canónico)
    # ========================================
    
    def _guardar_libros(self, data, cliente_id):
        Libro.query.filter_by(cliente_id=cliente_id).delete()
        
        # Soporte para nombres de campos JS (camelCase) y Jinja (snake_case o camelCase)
        # Se asume el frontend envía: librosCientificos[], capitulosLibro[]
        t_libros = data.getlist('librosCientificos[]')
        t_capitulos = data.getlist('capitulosLibro[]')
        
        from itertools import zip_longest
        
        has_data = False
        for libro, capitulo in zip_longest(t_libros, t_capitulos, fillvalue=''):
            if not libro and not capitulo: continue
            has_data = True
            registro = Libro(
                cliente_id=cliente_id,
                libros_cientificos=libro.strip() if libro else None,
                capitulos_libro=capitulo.strip() if capitulo else None
            )
            self.db.add(registro)

    def _guardar_tesis(self, data, cliente_id):
        ArticuloInforme.query.filter_by(cliente_id=cliente_id).delete()
        
        titulos = data.getlist('tituloTesis3[]')
        grados = data.getlist('grado3[]')
        estudiantes = data.getlist('estudiante3[]')
        instituciones = data.getlist('institucion3[]')
        estatus_list = data.getlist('estatus3[]')
        
        from itertools import zip_longest
        for titulo, grado, estudiante, institucion, estatus in zip_longest(
            titulos, grados, estudiantes, instituciones, estatus_list, fillvalue=''
        ):
            if not titulo: continue
            registro = ArticuloInforme(
                cliente_id=cliente_id,
                titulo=titulo.strip(),
                nivel=grado.strip(),
                nombre_estudiante=estudiante.strip(),
                institucion=institucion.strip(),
                estatus=estatus.strip()
            )
            self.db.add(registro)

    def _guardar_cursos(self, data, cliente_id):
        Curso.query.filter_by(cliente_id=cliente_id).delete()
        
        materias = data.getlist('materia4[]')
        niveles = data.getlist('nivel4[]')
        periodos = data.getlist('periodo4[]')
        instituciones = data.getlist('institucion4[]')
        programas = data.getlist('programas4[]')
        
        from itertools import zip_longest
        for materia, nivel, periodo, institucion, programa in zip_longest(
            materias, niveles, periodos, instituciones, programas, fillvalue=''
        ):
            if not materia: continue
            registro = Curso(
                cliente_id=cliente_id,
                materia=materia.strip(),
                nivel=nivel.strip(),
                periodo=periodo.strip(),
                institucion=institucion.strip(),
                programas=programa.strip()
            )
            self.db.add(registro)
    
    def _guardar_comites(self, data, cliente_id):
        """
        Maneja Comités Y Jurados en la misma tabla ComiteJurado.
        Diferenciados por campo 'participacion'.
        """
        ComiteJurado.query.filter_by(cliente_id=cliente_id).delete()
        
        # Recuperar listas del formulario unificado
        # El frontend debe enviar arrays para cada fila
        tipos = data.getlist('tipoParticipacion[]') # 'comite' o 'jurado'
        subtipos = data.getlist('subapartadoComite[]') # Para comite
        niveles = data.getlist('nivelAcademico[]') 
        programas = data.getlist('programaPosgrado[]')
        titulos = data.getlist('tituloTesisComite[]')
        estudiantes = data.getlist('estudianteComite[]')
        
        from itertools import zip_longest
        for tipo, sub, nivel, programa, titulo, estudiante in zip_longest(
            tipos, subtipos, niveles, programas, titulos, estudiantes, fillvalue=''
        ):
            if not tipo: continue # Si no hay tipo seleccionado, ignorar
            
            # Construir valor de participacion
            participacion_str = ""
            if tipo == 'comite':
                participacion_str = f"Comité - {sub}" if sub else "Comité"
            else:
                participacion_str = tipo
                
            registro = ComiteJurado(
                cliente_id=cliente_id,
                nivel_academico=nivel.strip() if nivel else None,
                programa_posgrado=programa.strip() if programa else None,
                participacion=participacion_str,
                titulo_tesis=titulo.strip() if titulo else None,
                nombre_estudiante=estudiante.strip() if estudiante else None
            )
            self.db.add(registro)

    def _guardar_estudiantes(self, data, cliente_id):
        Estudiante.query.filter_by(cliente_id=cliente_id).delete()
        
        activ_est = data.getlist('tipoEstudiante[]')
        nombres = data.getlist('nombreEstudianteParticipacion[]')
        titulos_proy = data.getlist('tituloProyectoEstudiante[]')
        procedencias = data.getlist('procedenciaServicio[]')
        
        from itertools import zip_longest
        for activ, nombre, titulo, procedencia in zip_longest(
            activ_est, nombres, titulos_proy, procedencias, fillvalue=''
        ):
            if not activ: continue
            registro = Estudiante(
                cliente_id=cliente_id,
                actividad=activ.strip(),
                nombre=nombre.strip(),
                titulo_proyecto=titulo.strip(),
                procedencia=procedencia.strip()
            )
            self.db.add(registro)
    
    def _guardar_congresos(self, data, cliente_id):
        Congreso.query.filter_by(cliente_id=cliente_id).delete()
        
        titulos = data.getlist('tituloTrabajo[]')
        autores = data.getlist('autores[]')
        nombres = data.getlist('nombreEvento[]')
        lugares = data.getlist('lugar[]')
        fechas_inicio = data.getlist('fechaInicio[]')
        fechas_fin = data.getlist('fechaFin[]')
        ponentes = data.getlist('ponente[]')
        
        from itertools import zip_longest
        for titulo, autor, nombre, lugar, f_ini, f_fin, ponente in zip_longest(
            titulos, autores, nombres, lugares, fechas_inicio, fechas_fin, ponentes, fillvalue=''
        ):
            if not titulo: continue
            fechas = f"{f_ini} al {f_fin}" if f_ini and f_fin else f_ini or f_fin
            registro = Congreso(
                cliente_id=cliente_id,
                titulo=titulo.strip(),
                autores=autor.strip(),
                nombre=nombre.strip(),
                lugar=lugar.strip(),
                fechas=fechas,
                ponente=ponente.strip()
            )
            self.db.add(registro)
    
    def _guardar_eventos(self, data, cliente_id):
        Evento.query.filter_by(cliente_id=cliente_id).delete()
        
        tipos = data.getlist('tipoEvento[]')
        nombres = data.getlist('nombreEventoSimple[]')
        num_ponentes = data.getlist('numPonentes[]')
        num_asistentes = data.getlist('numAsistentes[]')
        
        from itertools import zip_longest
        for tipo, nombre, ponentes, asistentes in zip_longest(
            tipos, nombres, num_ponentes, num_asistentes, fillvalue=''
        ):
            if not tipo: continue
            registro = Evento(
                cliente_id=cliente_id,
                tipo=tipo.strip(),
                nombre=nombre.strip(),
                num_ponentes=int(ponentes) if ponentes and ponentes.strip().isdigit() else None,
                num_asistentes=int(asistentes) if asistentes and asistentes.strip().isdigit() else None
            )
            self.db.add(registro)
    
    def _guardar_financiacion(self, data, cliente_id):
        # Multiple records strategy
        Financiamiento.query.filter_by(cliente_id=cliente_id).delete()
        
        titulos = data.getlist('tituloFinanciacion[]')
        fuentes = data.getlist('fuenteFinanciamiento[]')
        clasificaciones = data.getlist('clasificacionFinanciacion[]')
        indoles = data.getlist('indoleFinanciacion[]')
        participantes_json_list = data.getlist('participantesLista[]')
        
        from itertools import zip_longest
        for titulo, fuente, clas, indole, parts_json in zip_longest(
            titulos, fuentes, clasificaciones, indoles, participantes_json_list, fillvalue=''
        ):
            if not titulo: continue
            
            registro = Financiamiento(
                cliente_id=cliente_id,
                titulo=titulo.strip(),
                fuente=fuente.strip(),
                clasificado=clas.strip(),
                indole=indole.strip(),
                participantes=parts_json # Save raw JSON string
            )
            self.db.add(registro)
    
    def _guardar_patentes(self, data, cliente_id):
        record = Patente.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Patente(cliente_id=cliente_id)
            self.db.add(record)
        record.contenido = data.get('descripcion', '')

    def _guardar_comisiones(self, data, cliente_id):
        record = Comision.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Comision(cliente_id=cliente_id)
            self.db.add(record)
        record.contenido = data.get('descripcion', '')

    def _guardar_vinculacion(self, data, cliente_id):
        record = Vinculacion.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Vinculacion(cliente_id=cliente_id)
            self.db.add(record)
        record.contenido = data.get('descripcion', '')

    def _guardar_distinciones(self, data, cliente_id):
        record = Distincion.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Distincion(cliente_id=cliente_id)
            self.db.add(record)
        record.contenido = data.get('descripcion', '')

    def _guardar_logros(self, data, cliente_id):
        record = Logro.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Logro(cliente_id=cliente_id)
            self.db.add(record)
        record.contenido = data.get('descripcion', '')
    
    def _guardar_divulgacion(self, data, cliente_id):
        Divulgacion.query.filter_by(cliente_id=cliente_id).delete()
        
        tipos = data.getlist('tipoDivulgacion[]')
        autores = data.getlist('autoresDivulgacion[]')
        revistas = data.getlist('revistaDivulgacion[]')
        tipos_evento = data.getlist('tipoEventoDivulgacion[]')
        modalidades = data.getlist('modalidadDivulgacion[]')
        
        from itertools import zip_longest
        for tipo, autor, revista, tipo_ev, modalidad in zip_longest(
            tipos, autores, revistas, tipos_evento, modalidades, fillvalue=''
        ):
            if not tipo: continue
            registro = Divulgacion(
                cliente_id=cliente_id,
                tipo_actividad=tipo.strip(),
                autores=autor.strip(),
                revista=revista.strip(),
                tipo_evento=tipo_ev.strip(),
                modalidad=modalidad.strip()
            )
            self.db.add(registro)
    
    def _guardar_estancias(self, data, cliente_id):
        Estancia.query.filter_by(cliente_id=cliente_id).delete()
        
        tipos = data.getlist('tipoEstancia[]')
        nombres = data.getlist('nombreEstancia[]')
        origenes = data.getlist('origenEstancia[]')
        instituciones = data.getlist('institucionProcedencia[]')
        f_inis = data.getlist('fechaInicioEstancia[]')
        f_fins = data.getlist('fechaFinEstancia[]')
        
        from itertools import zip_longest
        for tipo, nombre, origen, institucion, f_ini, f_fin in zip_longest(
            tipos, nombres, origenes, instituciones, f_inis, f_fins, fillvalue=''
        ):
            if not tipo: continue
            fechas = f"{f_ini} al {f_fin}" if f_ini and f_fin else f_ini or f_fin
            registro = Estancia(
                cliente_id=cliente_id,
                tipo=tipo.strip(),
                nombre=nombre.strip(),
                origen=origen.strip(),
                institucion=institucion.strip(),
                fechas=fechas.strip()
            )
            self.db.add(registro)
