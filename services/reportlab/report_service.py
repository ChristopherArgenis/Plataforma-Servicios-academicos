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
            if l.libros_cientificos:
                investigacion_items.append(f"Libro: {l.libros_cientificos}")
            if l.capitulos_libro:
                investigacion_items.append(f"Capítulo de libro: {l.capitulos_libro}")

        for a in articulos:
            investigacion_items.append(f"Artículo: {a.titulo}")

        builder.render_section("Investigacion", investigacion_items)

        # =========================
        # 2. DOCENCIA
        # =========================
        cursos = Curso.query.filter_by(cliente_id=self.cliente_id).all()
        # comites = ComiteJurado.query.filter_by(cliente_id=self.cliente_id).all()
        # estudiantes = Estudiante.query.filter_by(cliente_id=self.cliente_id).all()

        docencia_items = []

        for c in cursos:
            docencia_items.append(
                f"Curso: {c.materia} ({c.nivel}) – {c.periodo}"
            )
        # ⚠️ TEMPORALMENTE DESACTIVADO
        # La tabla ComiteJurado NO tiene columna titulo_tesis en BD actual
        # for com in comites:
        #     docencia_items.append(
        #         f"{com.participacion}: {com.nombre_estudiante} – {com.titulo_tesis or '---'} ({com.nivel_academico})"
        #     )

        #for e in estudiantes:
        #    docencia_items.append(
        #        f"Estudiante: {e.nombre} – {e.actividad} ({e.procedencia})"
        #    )

        builder.render_section("Docencia", docencia_items)

        # =========================
        # 3. DIFUSIÓN
        # =========================
        congresos = Congreso.query.filter_by(cliente_id=self.cliente_id).all()
        eventos = Evento.query.filter_by(cliente_id=self.cliente_id).all()

        difusion_items = []

        for c in congresos:
            difusion_items.append(
                f"Congreso: {c.titulo} – {c.nombre} ({c.fechas})"
            )

        for e in eventos:
            difusion_items.append(
                f"Evento: {e.nombre} ({e.tipo})"
            )

        builder.render_section("Difusion", difusion_items)

        # =========================
        # 4. DIVULGACIÓN
        # =========================
        divulgaciones = Divulgacion.query.filter_by(cliente_id=self.cliente_id).all()

        div_items = [
            f"{d.tipo_actividad}: {d.revista or d.tipo_evento}"
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
            f"{e.tipo}: {e.nombre} – {e.institucion} ({e.fechas})"
            for e in estancias
        ]
        builder.render_section("Intercambio Academico", est_items)

        # =========================
        # 7. PROYECTOS FINANCIADOS
        # =========================
        proyectos = Financiamiento.query.filter_by(cliente_id=self.cliente_id).all()
        proy_items = [
            f"{p.titulo} – {p.fuente} ({p.clasificado})"
            for p in proyectos
        ]
        builder.render_section("Proyectos financiados", proy_items)

        # =========================
        # 8. COMISIONES ACADÉMICAS
        # =========================
        comisiones = Comision.query.filter_by(cliente_id=self.cliente_id).all()
        builder.render_section(
            "Participación en comisiones académicas",
            [c.contenido for c in comisiones if c.contenido]
        )

        # =========================
        # 9. VINCULACIÓN
        # =========================
        vinculaciones = Vinculacion.query.filter_by(cliente_id=self.cliente_id).all()
        builder.render_section(
            "Actividades de vinculación",
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
        #relevantes = Relevantes.query.filter_by(cliente_id=self.cliente_id).limit(3).all()
        # rel_items = [
          #  f"{r.titulo} ({r.anio})"
          #  for r in relevantes
        # ]
        #builder.render_section(
         #   "3 artículos más importantes/relevantes",
          #  rel_items
        #)

        builder.build()