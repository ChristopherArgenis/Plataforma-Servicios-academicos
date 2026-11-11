# services/reportlab/report_builder.py
from .base_pdf import BasePDF
from .report_texts import REPORT_TEXTS
from .text_parser import TextParser

class ReportBuilder:
    def __init__(self, filename):
        self.pdf = BasePDF(filename)

    def header(self, info):
        """Renderiza el encabezado institucional y datos del investigador."""
        # Render title centered and large
        self.pdf.report_title(REPORT_TEXTS["header"])
        self.pdf.spacer(5)
        for label, value in info.items():
            self.pdf.paragraph(f"<b>{label}:</b> {value or '---'}")
        self.pdf.spacer(10)

    def render_section(self, section_key, items=None):
        """
        Renderiza una sección del reporte con estructura jerárquica:
        1. Texto institucional parseado (títulos, subsecciones, párrafos)
        2. Items dinámicos (si existen)
        """
        if section_key not in REPORT_TEXTS:
            return

        # Parse section text into structured components
        components = TextParser.parse_section(REPORT_TEXTS[section_key])
        
        # Render each component with appropriate style
        for component in components:
            if component['type'] == 'main_title':
                self.pdf.main_title(component['text'])
            elif component['type'] == 'subsection':
                self.pdf.subsection(component['text'])
            elif component['type'] == 'subsubsection':
                self.pdf.subsubsection(component['text'])
            elif component['type'] == 'paragraph':
                self.pdf.normal_paragraph(component['text'])
        
        # Add dynamic items if provided
        if items:
            self.pdf.dynamic_items(items)
        else:
            self.pdf.normal_paragraph("<i>No se registraron datos en este periodo.</i>")
        
        self.pdf.spacer(10)

    def build(self):
        self.pdf.build()