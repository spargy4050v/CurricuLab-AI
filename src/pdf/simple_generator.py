"""
Generic PDF generator utility for dashboards.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from io import BytesIO
import datetime

class PDFGenerator:
    """Professional PDF generator for structured dictionary data."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup professional typography."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='AppTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#3E2723'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section Heading
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#5D4037'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subsection Heading
        self.styles.add(ParagraphStyle(
            name='SubHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#8D6E63'),
            spaceAfter=8,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))

        # Body text
        self.styles.add(ParagraphStyle(
            name='BodySmall',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#4E342E'),
            spaceAfter=6
        ))

    def generate(self, data: dict, title: str) -> BytesIO:
        """Generate PDF from dictionary data."""
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Header
        story.append(Paragraph("CurricuLab AI", self.styles['AppTitle']))
        story.append(Paragraph(title, self.styles['SectionHeading']))
        story.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", self.styles['BodySmall']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Content dynamic building
        self._build_content(story, data)
        
        # Footer branding
        story.append(Spacer(1, 0.5 * inch))
        story.append(Paragraph("---", self.styles['Normal']))
        story.append(Paragraph("CurricuLab AI - Intelligent Curriculum Design Platform", self.styles['BodySmall']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer

    def _build_content(self, story, data, level=0):
        """Recursively build PDF content from dictionary."""
        if isinstance(data, dict):
            for key, value in data.items():
                label = key.replace('_', ' ').title()
                
                if level == 0:
                    story.append(Paragraph(label, self.styles['SectionHeading']))
                elif level == 1:
                    story.append(Paragraph(label, self.styles['SubHeading']))
                else:
                    story.append(Paragraph(f"<b>{label}:</b>", self.styles['Normal']))
                
                if isinstance(value, (dict, list)):
                    self._build_content(story, value, level + 1)
                else:
                    story.append(Paragraph(str(value), self.styles['Normal']))
                    story.append(Spacer(1, 0.1 * inch))
        
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    self._build_content(story, item, level + 1)
                    story.append(Spacer(1, 0.1 * inch))
                else:
                    story.append(Paragraph(f"• {str(item)}", self.styles['Normal']))
            story.append(Spacer(1, 0.1 * inch))

def generate_pdf(data: dict, title: str) -> BytesIO:
    """Helper function to generate PDF content."""
    generator = PDFGenerator()
    return generator.generate(data, title)
