import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO

class CVGenerator:
    def generate_cv(self, data):
        """Generate a professional CV as PDF."""
        try:
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter,
                                   rightMargin=72, leftMargin=72,
                                   topMargin=72, bottomMargin=72)
            
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#2E4053'),
                spaceAfter=30
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#2E4053'),
                spaceAfter=12
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=6
            )
            
            story = []
            
            # Name
            story.append(Paragraph(data.get('cv_name', 'Your Name'), title_style))
            
            # Contact Information
            contact_text = f"📧 {data.get('cv_email', '')} | 📱 {data.get('cv_phone', '')}"
            story.append(Paragraph(contact_text, body_style))
            story.append(Spacer(1, 20))
            
            # Education
            story.append(Paragraph("🎓 Education", heading_style))
            story.append(Paragraph(data.get('cv_education', ''), body_style))
            story.append(Spacer(1, 12))
            
            # Experience
            story.append(Paragraph("💼 Work Experience", heading_style))
            story.append(Paragraph(data.get('cv_experience', ''), body_style))
            story.append(Spacer(1, 12))
            
            # Skills
            story.append(Paragraph("🛠️ Skills", heading_style))
            skills_text = data.get('cv_skills', '')
            # Format skills nicely
            skills_list = [skill.strip() for skill in skills_text.split(',')]
            story.append(Paragraph("• " + " • ".join(skills_list), body_style))
            
            # Build PDF
            doc.build(story)
            buffer.seek(0)
            
            return buffer
            
        except Exception as e:
            print(f"CV Generation Error: {e}")
            return None
