# services/reportlab/base_pdf.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER

class BasePDF:
    def __init__(self, filename):
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=LETTER,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )

        self.story = []
        self.styles = getSampleStyleSheet()
        
        # Default font
        self.styles["Normal"].fontName = "Times-Roman"
        
        # Report title (INFORME ANUAL)
        self.styles.add(ParagraphStyle(
            name="ReportTitle",
            fontName="Times-Bold",
            fontSize=18,
            bold=True,
            spaceAfter=20,
            spaceBefore=10,
            leading=20,
            alignment=TA_CENTER
        ))
        
        # Main section title (1. Investigación, 2. Docencia) - Bold, capitalized
        self.styles.add(ParagraphStyle(
            name="MainTitle",
            fontName="Times-Bold",
            fontSize=12,
            bold=True,
            spaceAfter=10,
            spaceBefore=15,
            leading=14
        ))
        
        # Subsection (1.1, 1.2, 2.1) - Bold
        self.styles.add(ParagraphStyle(
            name="Subsection",
            fontName="Times-Bold",
            fontSize=11,
            bold=True,
            spaceAfter=6,
            spaceBefore=8,
            leftIndent=0,
            leading=13
        ))
        
        # Sub-subsection (2.1.1, 2.1.2) - Normal, indented
        self.styles.add(ParagraphStyle(
            name="SubSubsection",
            fontName="Times-Roman",
            fontSize=10,
            spaceAfter=4,
            spaceBefore=4,
            leftIndent=20,
            leading=12
        ))
        
        # Normal Paragraph (Main Narrative)
        self.styles.add(ParagraphStyle(
            name="NormalParagraph",
            fontName="Times-Roman",
            fontSize=10,
            spaceAfter=8,
            leading=12,
            alignment=TA_JUSTIFY
        ))

        # Dynamic Content Style (Blue, No list)
        self.styles.add(ParagraphStyle(
            name="DynamicContent",
            fontName="Times-Roman",
            fontSize=10,
            textColor="#000080",  # Navy Blue
            spaceAfter=4,
            leading=12,
            leftIndent=10
        ))

        # Legacy styles
        self.styles.add(ParagraphStyle(
            name="Section",
            fontName="Times-Bold",
            fontSize=12,
            spaceAfter=10,
            spaceBefore=20,
            leading=14,
            bold=True
        ))
        self.styles.add(ParagraphStyle(
            name="Item",
            fontName="Times-Roman",
            fontSize=10,
            spaceAfter=6,
            leading=13
        ))

    def report_title(self, text):
        """Renders report title (INFORME ANUAL) - centered, large"""
        self.story.append(Paragraph(text, self.styles["ReportTitle"]))

    def main_title(self, text):
        """Renders main section title (1. Investigación, 2. Docencia) - bold, capitalized"""
        self.story.append(Paragraph(text, self.styles["MainTitle"]))

    def subsection(self, text):
        """Renders subsection (1.1, 1.2, 2.1)"""
        self.story.append(Paragraph(text, self.styles["Subsection"]))

    def subsubsection(self, text):
        """Renders sub-subsection (2.1.1, 2.1.2)"""
        self.story.append(Paragraph(text, self.styles["SubSubsection"]))

    def normal_paragraph(self, text):
        """Renders normal paragraph"""
        self.story.append(Paragraph(text, self.styles["NormalParagraph"]))

    def section(self, title):
        """Legacy method - renders section title"""
        self.story.append(Paragraph(title, self.styles["Section"]))

    def paragraph(self, text):
        """Legacy method - renders paragraph"""
        self.story.append(Paragraph(text, self.styles["Item"]))

    def bullet_list(self, items):
        self.story.append(
            ListFlowable(
                [ListItem(Paragraph(i, self.styles["Item"])) for i in items],
                bulletType='bullet'
            )
        )

    def dynamic_items(self, items):
        """Renders dynamic items in navy blue"""
        for i in items:
            self.story.append(Paragraph(i, self.styles["DynamicContent"]))

    def spacer(self, height=10):
        self.story.append(Spacer(1, height))

    def build(self):
        self.doc.build(self.story)