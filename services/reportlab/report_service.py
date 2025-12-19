# services/reportlab/report_service.py
import json
from datetime import datetime
from .report_builder import ReportBuilder
from models.user import (
    Cliente, Usuario, InformationAcademic, Articles, Articles_Keys, Libro, ArticuloInforme, Curso,
    ComiteJurado, Estudiante, Congreso, Evento, Divulgacion,
    Estancia, Financiamiento, Patente, Comision, Vinculacion,
    Distincion, Logro, Relevantes
)

class ReportService:
    def __init__(self, cliente_id: int):
        self.cliente_id = cliente_id

    def _format_participantes(self, participantes_json: str):
        if not participantes_json:
            return "---"
        try:
            data = json.loads(participantes_json)
            if not isinstance(data, list):
                return participantes_json
            
            formatted = []
            for p in data:
                nombre = p.get('nombre', '---')
                tipo = (p.get('tipo', '---') or '---').capitalize()
                inst = p.get('institucion', '---')
                formatted.append(f"{nombre} ({tipo}, {inst})")
            
            return "<br/>".join(formatted)
        except:
            return participantes_json

    def generar_reporte(self, filename: str):
        builder = ReportBuilder(filename)
        current_year = datetime.now().year

        # =========================
        # 0. HEADER
        # =========================
        cliente = Cliente.query.get(self.cliente_id)
        info = InformationAcademic.query.filter_by(cliente_id=self.cliente_id).first()

        header_info = {
            "Nombre": cliente.nombre if cliente else "Desconocido",
            "Categoría y nivel": info.categoria if info else "---",
            "Departamento": info.departamento if info else "---",
            "SNI": info.sni if info else "---",
            "PRIDE": info.pride if info else "---",
        }
        builder.header(header_info)

        # =========================
        # 1. INVESTIGACIÓN
        # =========================
        libros = Libro.query.filter_by(cliente_id=self.cliente_id).all()
        
        # Query for Articles of current year through Usuario and Articles_Keys
        articulos_investigacion = Articles.query.join(
            Articles_Keys, Articles.id_Articles == Articles_Keys.id_Articles
        ).join(
            Usuario, Articles_Keys.profile_id == Usuario.profile_id
        ).filter(
            Usuario.id == self.cliente_id,
            Articles.year == current_year
        ).all()

        investigacion_items = []

        for l in libros:
            item = []
            if l.libros_cientificos:
                item.append(f"<b>{l.libros_cientificos}</b>")
            if l.capitulos_libro:
                item.append(f"Capítulo: {l.capitulos_libro}")
            if item:
                investigacion_items.append("<br/>".join(item))

        for a in articulos_investigacion:
            investigacion_items.append(
                f"<b>{a.title}</b><br/>"
                f"{a.authors}<br/>"
                f"<i>{a.journal}</i>, Vol. {a.volume or '—'}, pp. {a.pages}, {a.year}."
            )

        builder.render_section("Investigacion", investigacion_items)

        # =========================
        # 2. TESIS (Anterior Docencia)
        # =========================
        cursos = Curso.query.filter_by(cliente_id=self.cliente_id).all()
        comites = ComiteJurado.query.filter_by(cliente_id=self.cliente_id).all()
        estudiantes = Estudiante.query.filter_by(cliente_id=self.cliente_id).all()
        articulos_docencia = ArticuloInforme.query.filter_by(cliente_id=self.cliente_id).all()

        tesis_items = []

        for ad in articulos_docencia:
            tesis_items.append(
                f"<b>{ad.titulo}</b><br/>"
                f"Nivel: {(ad.nivel or '—').capitalize()}<br/>"
                f"Estudiante: {ad.nombre_estudiante or '—'}<br/>"
                f"Institución: {ad.institucion or '—'}<br/>"
                f"Estatus: {(ad.estatus or '—').capitalize()}"
            )

        for c in cursos:
            tesis_items.append(
                f"<b>{c.materia}</b><br/>"
                f"Nivel: {(c.nivel or '—').capitalize()}<br/>"
                f"Periodo: {c.periodo}<br/>"
                f"Institución: {c.institucion or '—'}<br/>"
                f"Programas: {c.programas or '—'}"
            )

        for com in comites:
            tesis_items.append(
                f"<b>{com.titulo_tesis or 'Sin título'}</b><br/>"
                f"Participación: {(com.participacion or '—').capitalize()}<br/>"
                f"Estudiante: {com.nombre_estudiante}<br/>"
                f"Nivel: {(com.nivel_academico or '—').capitalize()}<br/>"
                f"Posgrado: {com.programa_posgrado or '—'}"
            )

        for e in estudiantes:
            tesis_items.append(
                f"<b>{e.actividad}</b><br/>"
                f"Estudiante: {e.nombre}<br/>"
                f"Procedencia: {e.procedencia}<br/>"
                f"Proyecto: {e.titulo_proyecto or '—'}"
            )

        builder.render_section("Docencia", tesis_items)

        # =========================
        # 3. DIFUSIÓN
        # =========================
        congresos = Congreso.query.filter_by(cliente_id=self.cliente_id).all()
        eventos = Evento.query.filter_by(cliente_id=self.cliente_id).all()

        difusion_items = []

        for c in congresos:
            difusion_items.append(
                f"<b>{c.titulo}</b><br/>"
                f"{c.autores or '—'}<br/>"
                f"<i>{c.nombre}</i>, {c.lugar or '—'}<br/>"
                f"Fechas: {c.fechas}<br/>"
                f"Ponente: {c.ponente or '—'}"
            )

        for e in eventos:
            difusion_items.append(
                f"<b>{e.nombre}</b><br/>"
                f"Tipo: {(e.tipo or '—').capitalize()}<br/>"
                f"Ponentes: {e.num_ponentes or 0}<br/>"
                f"Asistentes: {e.num_asistentes or 0}"
            )

        builder.render_section("Difusion", difusion_items)

        # =========================
        # 4. DIVULGACIÓN
        # =========================
        divulgaciones = Divulgacion.query.filter_by(cliente_id=self.cliente_id).all()
        div_items = [
            f"<b>{(d.tipo_actividad or '—').capitalize()}</b><br/>"
            f"{d.autores or '—'}<br/>"
            f"<i>{d.revista or d.tipo_evento}</i><br/>"
            f"Modalidad: {(d.modalidad or '—').capitalize()}"
            for d in divulgaciones
        ]
        builder.render_section("Divulgacion", div_items)

        # =========================
        # 5. PATENTES
        # =========================
        patentes = Patente.query.filter_by(cliente_id=self.cliente_id).all()
        builder.render_section("Patentes", [f"<b>{p.contenido}</b>" if p.contenido else "" for p in patentes if p.contenido])

        # =========================
        # 6. INTERCAMBIO ACADÉMICO
        # =========================
        estancias = Estancia.query.filter_by(cliente_id=self.cliente_id).all()
        est_items = [
            f"<b>{(e.tipo or '—').capitalize()}: {e.nombre}</b><br/>"
            f"Institución: {e.institucion}<br/>"
            f"Origen: {e.origen or '—'}<br/>"
            f"Fechas: {e.fechas}"
            for e in estancias
        ]
        builder.render_section("IntercambioAcademico", est_items)

        # =========================
        # 7. PROYECTOS FINANCIADOS
        # =========================
        proyectos = Financiamiento.query.filter_by(cliente_id=self.cliente_id).all()
        proy_items = [
            f"<b>{p.titulo}</b><br/>"
            f"Fuente: {p.fuente}<br/>"
            f"Participantes: {self._format_participantes(p.participantes)}<br/>"
            f"Clasificación: {(p.clasificado or '—').capitalize()}<br/>"
            f"Índole: {(p.indole or '—').capitalize()}"
            for p in proyectos
        ]
        builder.render_section("ProyectosFinanciados", proy_items)

        # ... (Mantener el resto de secciones si existen)
        # =========================
        # 8. COMISIONES
        # =========================
        comisiones = Comision.query.filter_by(cliente_id=self.cliente_id).all()
        builder.render_section("Comisiones", [f"<b>{c.contenido}</b>" if c.contenido else "" for c in comisiones if c.contenido])

        # =========================
        # 9. VINCULACIÓN
        # =========================
        vinculaciones = Vinculacion.query.filter_by(cliente_id=self.cliente_id).all()
        builder.render_section("Vinculacion", [f"<b>{v.contenido}</b>" if v.contenido else "" for v in vinculaciones if v.contenido])

        # =========================
        # 10. OTROS
        # =========================
        distinciones = Distincion.query.filter_by(cliente_id=self.cliente_id).all()
        builder.render_section("Otros", [f"<b>{d.contenido}</b>" if d.contenido else "" for d in distinciones if d.contenido])

        # =========================
        # 11. LOGROS
        # =========================
        logros = Logro.query.filter_by(cliente_id=self.cliente_id).all()
        builder.render_section("Logros", [f"<b>{l.contenido}</b>" if l.contenido else "" for l in logros if l.contenido])

        # =========================
        # 12. ARTÍCULOS RELEVANTES
        # =========================
        relevantes = Relevantes.query.filter_by(cliente_id=self.cliente_id).all()
        rel_items = [
            f"<b>{r.title}</b><br/>"
            f"{r.authors or '—'}<br/>"
            f"<i>{r.journal or '—'}</i>, {r.year}"
            for r in relevantes
        ]
        builder.render_section("ArticulosRelevantes", rel_items)

        builder.build()