# services/reportlab/base_pdf.py
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import cm

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
        self.styles.add(ParagraphStyle(
            name="Section",
            fontSize=12,
            spaceAfter=10,
            spaceBefore=20,
            leading=14,
            bold=True
        ))
        self.styles.add(ParagraphStyle(
            name="Item",
            fontSize=10,
            spaceAfter=6,
            leading=13
        ))

    def section(self, title):
        self.story.append(Paragraph(title, self.styles["Section"]))

    def paragraph(self, text):
        self.story.append(Paragraph(text, self.styles["Item"]))

    def bullet_list(self, items):
        self.story.append(
            ListFlowable(
                [ListItem(Paragraph(i, self.styles["Item"])) for i in items],
                bulletType='bullet'
            )
        )

    def spacer(self, height=10):
        self.story.append(Spacer(1, height))

    def build(self):
        self.doc.build(self.story)