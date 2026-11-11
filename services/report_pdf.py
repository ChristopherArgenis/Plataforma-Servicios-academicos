"""Generación del reporte en PDF (reportlab, sin servicios externos)."""
import io
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import (
    Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

APP_NAME = "Plataforma de Servicios Académicos"
NAVY = colors.HexColor("#002855")
BLUE = colors.HexColor("#2B6CB0")
GRAY = colors.HexColor("#5B6472")
LIGHT = colors.HexColor("#EEF2F7")
RULE = colors.HexColor("#C9D1DC")
DRAFT = colors.HexColor("#B45309")

MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
          "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

_base = dict(fontName="Helvetica", fontSize=10, leading=13, textColor=colors.HexColor("#1A2B42"))
STYLES = {
    "title": ParagraphStyle("title", **{**_base, "fontName": "Helvetica-Bold", "fontSize": 18,
                                        "leading": 22, "textColor": NAVY}),
    "subtitle": ParagraphStyle("subtitle", **{**_base, "textColor": GRAY}),
    "h2": ParagraphStyle("h2", **{**_base, "fontName": "Helvetica-Bold", "fontSize": 12,
                                  "leading": 16, "textColor": NAVY, "spaceBefore": 14,
                                  "spaceAfter": 6}),
    "body": ParagraphStyle("body", **_base),
    "label": ParagraphStyle("label", **{**_base, "fontName": "Helvetica-Bold", "textColor": GRAY}),
    "small": ParagraphStyle("small", **{**_base, "fontSize": 8.5, "leading": 11, "textColor": GRAY}),
    "cell": ParagraphStyle("cell", **{**_base, "fontSize": 9.5, "leading": 12}),
    "head": ParagraphStyle("head", **{**_base, "fontName": "Helvetica-Bold", "fontSize": 9.5,
                                      "textColor": colors.white}),
    "center": ParagraphStyle("center", **{**_base, "fontSize": 9.5, "alignment": TA_CENTER}),
    "draft": ParagraphStyle("draft", **{**_base, "fontName": "Helvetica-Bold", "textColor": DRAFT}),
}


def spanish_date(dt):
    return f"{dt.day} de {MONTHS[dt.month - 1]} de {dt.year}"


def _p(text, style="body"):
    return Paragraph(escape(str(text)), STYLES[style])


def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(doc.leftMargin, 1.2 * cm, APP_NAME)
    canvas.drawRightString(letter[0] - doc.rightMargin, 1.2 * cm, f"Página {doc.page}")
    canvas.setStrokeColor(RULE)
    canvas.line(doc.leftMargin, 1.6 * cm, letter[0] - doc.rightMargin, 1.6 * cm)
    canvas.restoreState()


def _info_table(rows, width):
    data = [[_p(k, "label"), _p(v)] for k, v in rows]
    table = Table(data, colWidths=[5 * cm, width - 5 * cm])
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return table


def _articles_table(articles, width):
    head = [_p("#", "head"), _p("Artículo", "head"), _p("Año", "head"), _p("Citas", "head")]
    data = [head]
    for i, art in enumerate(articles, 1):
        detail = ", ".join(x for x in (art.authors, art.publication) if x)
        title = Paragraph(
            f"{escape(art.title)}" + (f"<br/><font size=8.5 color='#5B6472'>{escape(detail)}</font>"
                                      if detail else ""),
            STYLES["cell"],
        )
        data.append([_p(i, "center"), title, _p(art.year or "s/f", "center"),
                     _p(art.cited_by, "center")])
    widths = [1.0 * cm, width - 4.2 * cm, 1.6 * cm, 1.6 * cm]
    table = Table(data, colWidths=widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 1), (-1, -1), 0.25, RULE),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


def _signature_block(signature, generated):
    parts = []
    if signature:
        reader = ImageReader(io.BytesIO(signature.image))
        w, h = reader.getSize()
        max_w, max_h = 6.5 * cm, 2.6 * cm
        scale = min(max_w / w, max_h / h)
        parts.append(Image(io.BytesIO(signature.image), width=w * scale, height=h * scale))
        name, title = signature.signer_name, signature.signer_title
    else:
        parts.append(Spacer(1, 2.6 * cm))
        name, title = "Firma pendiente", ""
    line = Table([[""]], colWidths=[7 * cm], rowHeights=[2])
    line.setStyle(TableStyle([("LINEABOVE", (0, 0), (-1, -1), 0.8, NAVY)]))
    parts += [line, _p(name, "center")]
    if title:
        parts.append(_p(title, "center"))
    parts.append(Paragraph(f"Fecha: {spanish_date(generated)}", STYLES["center"]))
    block = Table([[p] for p in parts], colWidths=[8 * cm])
    block.setStyle(TableStyle([("ALIGN", (0, 0), (-1, -1), "CENTER"),
                               ("TOPPADDING", (0, 0), (-1, -1), 1),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 1)]))
    block.hAlign = "CENTER"
    return KeepTogether([Spacer(1, 1.2 * cm), block])


def build_report(user, articles, signature=None, generated=None):
    """Devuelve los bytes del PDF del reporte."""
    generated = generated or datetime.now()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter, leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2.2 * cm,
        title=f"Reporte de producción académica - {user.name}", author=user.name,
        creator=APP_NAME,
    )
    width = doc.width
    years = [a.year for a in articles if a.year]
    period = (f"{min(years)} – {max(years)}" if years and min(years) != max(years)
              else (str(years[0]) if years else "Sin año"))

    story = [
        _p("Reporte de producción académica", "title"),
        _p(f"{user.affiliations or APP_NAME} · Generado el {spanish_date(generated)}", "subtitle"),
    ]
    if not signature:
        story += [Spacer(1, 6), _p("BORRADOR: este reporte aún no tiene firma.", "draft")]

    story += [
        _p("Datos del académico", "h2"),
        _info_table([
            ("Nombre", user.name),
            ("Correo", user.email),
            ("Afiliación", user.affiliations or "—"),
            ("Perfil Google Scholar", f"{user.scholar_name} ({user.scholar_id})"),
            ("Citas totales del perfil", user.cited_by),
        ], width),
        _p("Resumen", "h2"),
        _info_table([
            ("Artículos incluidos", len(articles)),
            ("Citas de estos artículos", sum(a.cited_by for a in articles)),
            ("Periodo", period),
        ], width),
        _p("Artículos incluidos", "h2"),
        _articles_table(articles, width),
        _signature_block(signature, generated),
    ]
    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)
    return buf.getvalue()
