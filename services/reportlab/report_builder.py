# services/reportlab/report_builder.py
from .base_pdf import BasePDF
from .report_texts import REPORT_TEXTS

class ReportBuilder:
    def __init__(self, filename):
        self.pdf = BasePDF(filename)

    def header(self, info):
        """Renderiza el encabezado institucional y datos del investigador."""
        self.pdf.section(REPORT_TEXTS["header"])
        self.pdf.spacer(5)
        for label, value in info.items():
            self.pdf.paragraph(f"<b>{label}:</b> {value or '---'}")
        self.pdf.spacer(10)

    def render_section(self, section_key, items=None):
        """
        Renderiza una sección del reporte:
        1. Texto institucional (siempre)
        2. Items dinámicos (si existen)
        """
        if section_key not in REPORT_TEXTS:
            return

        # El título de la sección se extrae del primer renglón del texto institucional si es necesario,
        # pero aquí simplemente usamos el texto completo como párrafo base.
        self.pdf.spacer(10)
        self.pdf.paragraph(REPORT_TEXTS[section_key])
        
        if items:
            self.pdf.bullet_list(items)
        else:
            self.pdf.paragraph("<i>No se registraron datos en este periodo.</i>")

    def build(self):
        self.pdf.build()