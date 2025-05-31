import re
import io
from typing import Optional, List
import PyPDF2
from docx import Document

class ResumeParser:
    """Utility class for parsing resumes from different file formats."""
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """Extract text from PDF file content."""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error parsing PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_content: bytes) -> str:
        """Extract text from DOCX file content."""
        try:
            doc = Document(io.BytesIO(file_content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise ValueError(f"Error parsing DOCX: {str(e)}")
    
    @staticmethod
    def extract_text_from_txt(file_content: bytes) -> str:
        """Extract text from TXT file content."""
        try:
            return file_content.decode('utf-8').strip()
        except UnicodeDecodeError:
            try:
                return file_content.decode('latin-1').strip()
            except Exception as e:
                raise ValueError(f"Error parsing TXT: {str(e)}")
    
    @classmethod
    def parse_resume(cls, file_content: bytes, file_type: str) -> str:
        """Parse resume based on file type."""
        file_type = file_type.lower()
        
        if file_type == 'pdf':
            return cls.extract_text_from_pdf(file_content)
        elif file_type in ['docx', 'doc']:
            return cls.extract_text_from_docx(file_content)
        elif file_type == 'txt':
            return cls.extract_text_from_txt(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    @staticmethod
    def extract_contact_info(text: str) -> dict:
        """Extract basic contact information from resume text."""
        contact_info = {}
        
        # Email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        # Phone number extraction (basic patterns)
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\(\d{3}\)\s*\d{3}[-.]?\d{4}',
            r'\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                contact_info['phone'] = phones[0]
                break
        
        return contact_info
    
    @staticmethod
    def extract_sections(text: str) -> dict:
        """Extract common resume sections."""
        sections = {}
        
        # Common section headers
        section_patterns = {
            'education': r'(?i)(education|academic|qualification)',
            'experience': r'(?i)(experience|employment|work history|professional)',
            'skills': r'(?i)(skills|competencies|technical|abilities)',
            'projects': r'(?i)(projects|portfolio)',
            'certifications': r'(?i)(certification|certificate|license)'
        }
        
        text_lines = text.split('\n')
        current_section = None
        
        for i, line in enumerate(text_lines):
            line_clean = line.strip()
            if not line_clean:
                continue
                
            # Check if line is a section header
            for section_name, pattern in section_patterns.items():
                if re.search(pattern, line_clean) and len(line_clean) < 50:
                    current_section = section_name
                    sections[section_name] = []
                    break
            else:
                # Add content to current section
                if current_section and line_clean:
                    sections[current_section].append(line_clean)
        
        # Convert lists to strings
        for section in sections:
            sections[section] = '\n'.join(sections[section])
        
        return sections
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize resume text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\-.,@()]+', '', text)
        
        # Remove multiple consecutive periods or dashes
        text = re.sub(r'[.-]{3,}', '', text)
        
        return text.strip()
