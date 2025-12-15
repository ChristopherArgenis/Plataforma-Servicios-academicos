"""
ReportService - Servicio centralizado para manejo de reportes académicos
Implementa la metodología arquitectónica definida para el proyecto
"""
import json
from models import db
from models.user import (
    Libro, ArticuloInforme, Curso, Congreso, Evento,
    ComiteJurado, Financiamiento, Patente, Comision,
    Vinculacion, Distincion, Logro, Divulgacion, Estancia
)


class ReportService:
    """
    Servicio centralizado para manejo de reportes académicos.
    UNA SOLA INSTANCIA POR REQUEST.
    
    Responsabilidades:
    - Guardar datos de formularios
    - Obtener datos para visualización/edición
    - Manejar lógica de negocio
    - Gestionar transacciones
    """
    
    def __init__(self, db_session):
        """
        Inicializa el servicio con la sesión de base de datos.
        
        Args:
            db_session: Sesión de SQLAlchemy (db.session)
        """
        self.db = db_session
        
        # Diccionario de handlers para cada formulario
        self._form_handlers = {
            'libros': self._guardar_libros,
            'tesis': self._guardar_tesis,
            'cursos': self._guardar_cursos,
            'comites': self._guardar_comites,
            'difusion': self._guardar_difusion,
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
    # MÉTODOS PÚBLICOS (Interfaz del Servicio)
    # ========================================
    
    def guardar(self, form_name, data, cliente_id):
        """
        Punto de entrada único para guardar cualquier formulario.
        
        Args:
            form_name (str): Identificador del formulario ('libros', 'cursos', etc.)
            data (dict): Datos del formulario
            cliente_id (int): ID del cliente
            
        Returns:
            tuple: (success: bool, message: str)
        """
        # Validar que el formulario existe
        handler = self._form_handlers.get(form_name)
        if not handler:
            return False, f"Formulario '{form_name}' no reconocido"
        
        try:
            # Ejecutar handler específico
            handler(data, cliente_id)
            
            # Commit de la transacción
            self.db.commit()
            
            return True, "Datos guardados correctamente"
            
        except ValueError as e:
            # Error de validación
            self.db.rollback()
            return False, str(e)
            
        except Exception as e:
            # Error inesperado
            self.db.rollback()
            print(f"[ERROR] ReportService.guardar({form_name}): {e}")
            return False, "Error al guardar los datos"
    
    def obtener(self, form_name, cliente_id):
        """
        Obtiene datos de un formulario para visualización/edición.
        
        Args:
            form_name (str): Identificador del formulario
            cliente_id (int): ID del cliente
            
        Returns:
            dict: Datos del formulario o None si no existe
        """
        # TODO: Implementar en fase 2
        pass
    
    # ========================================
    # MÉTODOS PRIVADOS (Lógica Específica)
    # ========================================
    
    def _guardar_libros(self, data, cliente_id):
        """
        Guarda libros científicos y capítulos de libro.
        FORMULARIO DINÁMICO: múltiples filas por cliente.
        
        Args:
            data: Objeto con método getlist() (request.form o similar)
            cliente_id (int): ID del cliente
        """
        # Obtener arrays de datos
        libros = data.get('libros_cientificos', []) if isinstance(data, dict) else []
        capitulos = data.get('capitulos_libro', []) if isinstance(data, dict) else []
        
        # Validar que hay datos
        if not libros and not capitulos:
            return
        
        # Estrategia overwrite controlado: eliminar registros anteriores
        Libro.query.filter_by(cliente_id=cliente_id).delete()
        
        # Crear una fila por cada par libro/capítulo
        # Usar zip_longest para manejar arrays de diferente longitud
        from itertools import zip_longest
        
        for libro, capitulo in zip_longest(libros, capitulos, fillvalue=''):
            # Saltar filas completamente vacías
            if not libro and not capitulo:
                continue
            
            registro = Libro(
                cliente_id=cliente_id,
                libros_cientificos=libro.strip() if libro else None,
                capitulos_libro=capitulo.strip() if capitulo else None
            )
            self.db.add(registro)
    
    def _guardar_tesis(self, data, cliente_id):
        """
        Guarda información de tesis y docencia.
        """
        record = ArticuloInforme.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = ArticuloInforme(cliente_id=cliente_id)
            self.db.add(record)
        
        # Guardar arrays como JSON
        record.tesis_dirigidas = json.dumps(
            data.get('tesis_dirigidas', []),
            ensure_ascii=False
        )
    
    def _guardar_cursos(self, data, cliente_id):
        """
        Guarda información de cursos impartidos.
        FORMULARIO DINÁMICO: múltiples filas por cliente.
        """
        materias = data.get('materia', [])
        niveles = data.get('nivel', [])
        periodos = data.get('periodo', [])
        
        if not materias:
            return
        
        # Eliminar registros anteriores
        Curso.query.filter_by(cliente_id=cliente_id).delete()
        
        # Crear una fila por cada curso
        from itertools import zip_longest
        for materia, nivel, periodo in zip_longest(materias, niveles, periodos, fillvalue=''):
            if not materia:
                continue
            
            registro = Curso(
                cliente_id=cliente_id,
                materia=materia.strip(),
                nivel=nivel.strip() if nivel else None,
                periodo=periodo.strip() if periodo else None
            )
            self.db.add(registro)
    
    def _guardar_comites(self, data, cliente_id):
        """
        Guarda información de comités y estudiantes.
        """
        record = ComiteJurado.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = ComiteJurado(cliente_id=cliente_id)
            self.db.add(record)
        
        record.comites = json.dumps(data.get('comites', []), ensure_ascii=False)
        record.estudiantes = json.dumps(data.get('estudiantes', []), ensure_ascii=False)
    
    def _guardar_difusion(self, data, cliente_id):
        """
        Guarda información de congresos y eventos.
        FORMULARIO DINÁMICO: múltiples filas por cliente.
        """
        # CONGRESOS
        titulos_congreso = data.get('tituloCongreso', [])
        if titulos_congreso:
            Congreso.query.filter_by(cliente_id=cliente_id).delete()
            
            autores = data.get('autoresCongreso', [])
            nombres = data.get('nombreCongreso', [])
            lugares = data.get('lugarCongreso', [])
            
            from itertools import zip_longest
            for titulo, autor, nombre, lugar in zip_longest(titulos_congreso, autores, nombres, lugares, fillvalue=''):
                if not titulo:
                    continue
                
                registro = Congreso(
                    cliente_id=cliente_id,
                    titulo=titulo.strip(),
                    autores=autor.strip() if autor else None,
                    nombre=nombre.strip() if nombre else None,
                    lugar=lugar.strip() if lugar else None
                )
                self.db.add(registro)
        
        # EVENTOS
        tipos_evento = data.get('tipoEvento', [])
        if tipos_evento:
            Evento.query.filter_by(cliente_id=cliente_id).delete()
            
            nombres = data.get('nombreEventoSimple', [])
            num_ponentes = data.get('numPonentes', [])
            num_asistentes = data.get('numAsistentes', [])
            
            from itertools import zip_longest
            for tipo, nombre, ponentes, asistentes in zip_longest(tipos_evento, nombres, num_ponentes, num_asistentes, fillvalue=''):
                if not tipo:
                    continue
                
                registro = Evento(
                    cliente_id=cliente_id,
                    tipo=tipo.strip(),
                    nombre=nombre.strip() if nombre else None,
                    num_ponentes=int(ponentes) if ponentes and ponentes.isdigit() else None,
                    num_asistentes=int(asistentes) if asistentes and asistentes.isdigit() else None
                )
                self.db.add(registro)
    
    def _guardar_financiacion(self, data, cliente_id):
        """
        Guarda información de proyectos financiados.
        """
        record = Financiamiento.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Financiamiento(cliente_id=cliente_id)
            self.db.add(record)
        
        record.titulo = data.get('titulo')
        record.fuente = data.get('fuente')
        record.clasificacion = data.get('clasificacion')
        record.indole = data.get('indole')
        record.participantes = json.dumps(
            data.get('participantes', []),
            ensure_ascii=False
        )
    
    def _guardar_patentes(self, data, cliente_id):
        """
        Guarda información de patentes (texto simple).
        """
        record = Patente.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Patente(cliente_id=cliente_id)
            self.db.add(record)
        
        record.descripcion = data.get('descripcion', '')
    
    def _guardar_comisiones(self, data, cliente_id):
        """
        Guarda información de comisiones (texto simple).
        """
        record = Comision.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Comision(cliente_id=cliente_id)
            self.db.add(record)
        
        record.descripcion = data.get('descripcion', '')
    
    def _guardar_vinculacion(self, data, cliente_id):
        """
        Guarda información de vinculación (texto simple).
        """
        record = Vinculacion.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Vinculacion(cliente_id=cliente_id)
            self.db.add(record)
        
        record.descripcion = data.get('descripcion', '')
    
    def _guardar_distinciones(self, data, cliente_id):
        """
        Guarda información de distinciones (texto simple).
        """
        record = Distincion.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Distincion(cliente_id=cliente_id)
            self.db.add(record)
        
        record.descripcion = data.get('descripcion', '')
    
    def _guardar_logros(self, data, cliente_id):
        """
        Guarda información de logros (texto simple).
        """
        record = Logro.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Logro(cliente_id=cliente_id)
            self.db.add(record)
        
        record.descripcion = data.get('descripcion', '')
    
    def _guardar_divulgacion(self, data, cliente_id):
        """
        Guarda información de divulgación.
        FORMULARIO DINÁMICO: múltiples filas por cliente.
        """
        tipos = data.get('tipoDivulgacion', [])
        if not tipos:
            return
        
        Divulgacion.query.filter_by(cliente_id=cliente_id).delete()
        
        autores = data.get('autoresDivulgacion', [])
        revistas = data.get('revistaDivulgacion', [])
        tipos_evento = data.get('tipoEventoDivulgacion', [])
        modalidades = data.get('modalidadDivulgacion', [])
        
        from itertools import zip_longest
        for tipo, autor, revista, tipo_ev, modalidad in zip_longest(tipos, autores, revistas, tipos_evento, modalidades, fillvalue=''):
            if not tipo:
                continue
            
            registro = Divulgacion(
                cliente_id=cliente_id,
                tipo_actividad=tipo.strip(),
                autores=autor.strip() if autor else None,
                revista=revista.strip() if revista else None,
                tipo_evento=tipo_ev.strip() if tipo_ev else None,
                modalidad=modalidad.strip() if modalidad else None
            )
            self.db.add(registro)
    
    def _guardar_estancias(self, data, cliente_id):
        """
        Guarda información de estancias.
        FORMULARIO DINÁMICO: múltiples filas por cliente.
        """
        tipos = data.get('tipoEstancia', [])
        if not tipos:
            return
        
        Estancia.query.filter_by(cliente_id=cliente_id).delete()
        
        nombres = data.get('nombreEstancia', [])
        origenes = data.get('origenEstancia', [])
        instituciones = data.get('institucionProcedencia', [])
        
        from itertools import zip_longest
        for tipo, nombre, origen, institucion in zip_longest(tipos, nombres, origenes, instituciones, fillvalue=''):
            if not tipo:
                continue
            
            registro = Estancia(
                cliente_id=cliente_id,
                tipo=tipo.strip(),
                nombre=nombre.strip() if nombre else None,
                origen=origen.strip() if origen else None,
                institucion=institucion.strip() if institucion else None
            )
            self.db.add(registro)
