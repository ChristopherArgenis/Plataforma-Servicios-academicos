# services/reportlab/report_service.py
from .report_builder import ReportBuilder
from models.user import (
    Cliente, InformationAcademic, Libro, ArticuloInforme, Curso,
    ComiteJurado, Estudiante, Congreso, Evento, Divulgacion,
    Estancia, Financiamiento, Patente, Comision, Vinculacion,
    Distincion, Logro, Relevantes
)

class ReportService:
    def __init__(self, cliente_id: int):
        self.cliente_id = cliente_id

    def generar_reporte(self, filename: str):
        builder = ReportBuilder(filename)

        # =========================
        # 0. HEADER – DATOS GENERALES
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
        articulos = ArticuloInforme.query.filter_by(cliente_id=self.cliente_id).all()

        investigacion_items = []

        for l in libros:
            data = []
            if l.libros_cientificos: data.append(f"Libro: {l.libros_cientificos}")
            if l.capitulos_libro: data.append(f"Capítulo: {l.capitulos_libro}")
            investigacion_items.append(" – ".join(data))

        for a in articulos:
            investigacion_items.append(
                f"Artículo: {a.titulo} – Nivel: {a.nivel or '---'} – Estudiante: {a.nombre_estudiante or '---'} – Institución: {a.institucion or '---'} – Estatus: {a.estatus or '---'}"
            )

        builder.render_section("Investigacion", investigacion_items)

        # =========================
        # 2. DOCENCIA
        # =========================
        cursos = Curso.query.filter_by(cliente_id=self.cliente_id).all()
        comites = ComiteJurado.query.filter_by(cliente_id=self.cliente_id).all()
        estudiantes = Estudiante.query.filter_by(cliente_id=self.cliente_id).all()

        docencia_items = []

        for c in cursos:
            docencia_items.append(
                f"Curso: {c.materia} – Nivel: {c.nivel} – Periodo: {c.periodo} – Institución: {c.institucion or '---'} – Programas: {c.programas or '---'}"
            )

        for com in comites:
            docencia_items.append(
                f"Participación: {com.participacion} – Estudiante: {com.nombre_estudiante} – Tesis: {com.titulo_tesis or '---'} – Nivel: {com.nivel_academico} – Posgrado: {com.programa_posgrado or '---'}"
            )

        for e in estudiantes:
            docencia_items.append(
                f"Estudiante: {e.nombre} – Actividad: {e.actividad} – Procedencia: {e.procedencia} – Proyecto: {e.titulo_proyecto or '---'}"
            )

        builder.render_section("Docencia", docencia_items)

        # =========================
        # 3. DIFUSIÓN
        # =========================
        congresos = Congreso.query.filter_by(cliente_id=self.cliente_id).all()
        eventos = Evento.query.filter_by(cliente_id=self.cliente_id).all()

        difusion_items = []

        for c in congresos:
            difusion_items.append(
                f"Congreso: {c.nombre} – Título Trabajo: {c.titulo} – Autores: {c.autores or '---'} – Lugar: {c.lugar or '---'} – Fechas: {c.fechas} – Ponente: {c.ponente or '---'}"
            )

        for e in eventos:
            difusion_items.append(
                f"Evento: {e.nombre} – Tipo: {e.tipo} – Ponentes: {e.num_ponentes or 0} – Asistentes: {e.num_asistentes or 0}"
            )

        builder.render_section("Difusion", difusion_items)

        # =========================
        # 4. DIVULGACIÓN
        # =========================
        divulgaciones = Divulgacion.query.filter_by(cliente_id=self.cliente_id).all()

        div_items = [
            f"Actividad: {d.tipo_actividad} – Revista/Evento: {d.revista or d.tipo_evento} – Autores: {d.autores or '---'} – Modalidad: {d.modalidad or '---'}"
            for d in divulgaciones
        ]

        builder.render_section("Divulgacion", div_items)

        # =========================
        # 5. PATENTES
        # =========================
        patentes = Patente.query.filter_by(cliente_id=self.cliente_id).all()
        builder.render_section(
            "Patentes",
            [p.contenido for p in patentes if p.contenido]
        )

        # =========================
        # 6. INTERCAMBIO ACADÉMICO
        # =========================
        estancias = Estancia.query.filter_by(cliente_id=self.cliente_id).all()
        est_items = [
            f"Tipo: {e.tipo} – Nombre: {e.nombre} – Institución: {e.institucion} – Origen: {e.origen or '---'} – Fechas: {e.fechas}"
            for e in estancias
        ]
        builder.render_section("IntercambioAcademico", est_items)

        # =========================
        # 7. PROYECTOS FINANCIADOS
        # =========================
        proyectos = Financiamiento.query.filter_by(cliente_id=self.cliente_id).all()
        proy_items = [
            f"Título: {p.titulo} – Fuente: {p.fuente} – Participantes: {p.participantes or '---'} – Clasificación: {p.clasificado} – Índole: {p.indole or '---'}"
            for p in proyectos
        ]
        builder.render_section("ProyectosFinanciados", proy_items)

        # =========================
        # 8. COMISIONES ACADÉMICAS
        # =========================
        comisiones = Comision.query.filter_by(cliente_id=self.cliente_id).all()
        builder.render_section(
            "Comisiones",
            [c.contenido for c in comisiones if c.contenido]
        )

        # =========================
        # 9. VINCULACIÓN
        # =========================
        vinculaciones = Vinculacion.query.filter_by(cliente_id=self.cliente_id).all()
        builder.render_section(
            "Vinculacion",
            [v.contenido for v in vinculaciones if v.contenido]
        )

        # =========================
        # 10. OTROS
        # =========================
        distinciones = Distincion.query.filter_by(cliente_id=self.cliente_id).all()
        builder.render_section(
            "Otros",
            [d.contenido for d in distinciones if d.contenido]
        )

        # =========================
        # 11. LOGROS
        # =========================
        logros = Logro.query.filter_by(cliente_id=self.cliente_id).all()
        builder.render_section(
            "Logros",
            [l.contenido for l in logros if l.contenido]
        )

        # =========================
        # 12. ARTÍCULOS RELEVANTES
        # =========================
        relevantes = Relevantes.query.filter_by(cliente_id=self.cliente_id).limit(3).all()
        rel_items = [
            f"Título: {r.title} – Autores: {r.authors or '---'} – Revista: {r.journal or '---'} – Año: {r.year}"
            for r in relevantes
        ]
        builder.render_section(
            "ArticulosRelevantes",
            rel_items
        )

        builder.build()