"""
Professional PDF generator using ReportLab.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from io import BytesIO
from src.curriculum.models import Curriculum


class CurriculumPDFGenerator:
    """Generate professional curriculum PDFs using ReportLab."""
    
    def __init__(self):
        """Initialize PDF generator."""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Semester heading
        self.styles.add(ParagraphStyle(
            name='SemesterHeading',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#16A085'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
    
    def generate(self, curriculum: Curriculum) -> BytesIO:
        """
        Generate PDF for curriculum.
        
        Args:
            curriculum: Curriculum object
            
        Returns:
            BytesIO buffer containing PDF
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build PDF content
        story = []
        
        # Title
        story.append(Paragraph(curriculum.title, self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Basic info
        info_text = f"""
        <b>Level:</b> {curriculum.level}<br/>
        <b>Duration:</b> {curriculum.duration_semesters} Semesters<br/>
        <b>Total Credits:</b> {curriculum.total_credits}
        """
        story.append(Paragraph(info_text, self.styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Overview
        story.append(Paragraph("Overview", self.styles['CustomHeading']))
        story.append(Paragraph(curriculum.overview, self.styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Learning Outcomes
        story.append(Paragraph("Learning Outcomes", self.styles['CustomHeading']))
        for outcome in curriculum.learning_outcomes:
            story.append(Paragraph(f"• {outcome}", self.styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Career Paths
        if curriculum.career_paths:
            story.append(Paragraph("Career Paths", self.styles['CustomHeading']))
            for career in curriculum.career_paths:
                story.append(Paragraph(f"• {career}", self.styles['Normal']))
            story.append(Spacer(1, 0.3 * inch))
        
        # Semester-wise breakdown
        story.append(PageBreak())
        story.append(Paragraph("Curriculum Structure", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2 * inch))
        
        for semester in curriculum.semesters:
            # Semester heading
            semester_title = f"Semester {semester.semester_number} ({semester.total_credits} Credits)"
            story.append(Paragraph(semester_title, self.styles['SemesterHeading']))
            
            # Course table
            table_data = [['Code', 'Course Name', 'Credits', 'Category']]
            
            for course in semester.courses:
                table_data.append([
                    course.code,
                    course.name,
                    str(course.credits),
                    course.category
                ])
            
            table = Table(table_data, colWidths=[1*inch, 3.5*inch, 0.8*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            
            story.append(table)
            story.append(Spacer(1, 0.3 * inch))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return buffer
    
    def save_to_file(self, curriculum: Curriculum, filename: str):
        """
        Save curriculum PDF to file.
        
        Args:
            curriculum: Curriculum object
            filename: Output filename
        """
        buffer = self.generate(curriculum)
        
        with open(filename, 'wb') as f:
            f.write(buffer.read())
        
        print(f"✓ PDF saved to: {filename}")
