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
        FORMULARIO DINÁMICO: Múltiples entradas guardadas como JSON.
        
        Args:
            data (dict): {
                'libros_cientificos': [...],
                'capitulos_libro': [...]
            }
            cliente_id (int): ID del cliente
        """
        # Buscar o crear registro único por cliente
        record = Libro.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Libro(cliente_id=cliente_id)
            self.db.add(record)
        
        # Guardar arrays como JSON
        record.libros_cientificos = json.dumps(
            data.get('libros_cientificos', []), 
            ensure_ascii=False
        )
        record.capitulos_libro = json.dumps(
            data.get('capitulos_libro', []), 
            ensure_ascii=False
        )
    
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
        """
        record = Curso.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Curso(cliente_id=cliente_id)
            self.db.add(record)
        
        # Guardar arrays como JSON
        record.materia = json.dumps(data.get('materia', []), ensure_ascii=False)
        record.nivel = json.dumps(data.get('nivel', []), ensure_ascii=False)
        record.periodo = json.dumps(data.get('periodo', []), ensure_ascii=False)
    
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
        """
        # Congresos
        congresos_data = data.get('congresos', [])
        if congresos_data:
            record = Congreso.query.filter_by(cliente_id=cliente_id).first()
            if not record:
                record = Congreso(cliente_id=cliente_id)
                self.db.add(record)
            record.data = json.dumps(congresos_data, ensure_ascii=False)
        
        # Eventos
        eventos_data = data.get('eventos', [])
        if eventos_data:
            record = Evento.query.filter_by(cliente_id=cliente_id).first()
            if not record:
                record = Evento(cliente_id=cliente_id)
                self.db.add(record)
            record.data = json.dumps(eventos_data, ensure_ascii=False)
    
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
        """
        record = Divulgacion.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Divulgacion(cliente_id=cliente_id)
            self.db.add(record)
        
        record.data = json.dumps(data.get('divulgacion', []), ensure_ascii=False)
    
    def _guardar_estancias(self, data, cliente_id):
        """
        Guarda información de estancias.
        """
        record = Estancia.query.filter_by(cliente_id=cliente_id).first()
        if not record:
            record = Estancia(cliente_id=cliente_id)
            self.db.add(record)
        
        record.data = json.dumps(data.get('estancias', []), ensure_ascii=False)
