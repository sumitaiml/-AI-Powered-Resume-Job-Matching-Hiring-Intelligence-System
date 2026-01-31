"""
Resume Parser Module
Extracts text and structured information from resume files
"""
import re
import PyPDF2
import pdfplumber
from docx import Document
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ResumeParser:
    """Parse and extract information from resumes"""
    
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        self.linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        self.github_pattern = r'github\.com/[\w-]+'
        
    def parse_resume(self, file_path: str, file_type: str = 'pdf') -> Dict:
        """
        Parse resume file and extract structured information
        
        Args:
            file_path: Path to the resume file
            file_type: Type of file (pdf, docx, txt)
            
        Returns:
            Dictionary containing parsed resume information
        """
        try:
            if file_type == 'pdf':
                text = self._extract_from_pdf(file_path)
            elif file_type in ['docx', 'doc']:
                text = self._extract_from_docx(file_path)
            elif file_type == 'txt':
                text = self._extract_from_txt(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            if not text or len(text.strip()) < 50:
                logger.warning(f"Extracted text too short from {file_path}")
                
            return self._extract_information(text)
            
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            return {
                'raw_text': '',
                'email': None,
                'phone': None,
                'linkedin': None,
                'github': None,
                'skills': [],
                'education': [],
                'experience': []
            }
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        try:
            # Try pdfplumber first (better for complex PDFs)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            logger.warning(f"pdfplumber failed, trying PyPDF2: {str(e)}")
            # Fallback to PyPDF2
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e2:
                logger.error(f"PyPDF2 also failed: {str(e2)}")
                
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
            return file.read()
    
    def _extract_information(self, text: str) -> Dict:
        """Extract structured information from raw text"""
        return {
            'raw_text': text,
            'email': self._extract_email(text),
            'phone': self._extract_phone(text),
            'linkedin': self._extract_linkedin(text),
            'github': self._extract_github(text),
            'skills': self._extract_skills(text),
            'education': self._extract_education(text),
            'experience': self._extract_experience(text)
        }
    
    def _extract_email(self, text: str) -> Optional[str]:
        """Extract email address"""
        match = re.search(self.email_pattern, text)
        return match.group(0) if match else None
    
    def _extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number"""
        match = re.search(self.phone_pattern, text)
        return match.group(0) if match else None
    
    def _extract_linkedin(self, text: str) -> Optional[str]:
        """Extract LinkedIn profile URL"""
        match = re.search(self.linkedin_pattern, text.lower())
        return match.group(0) if match else None
    
    def _extract_github(self, text: str) -> Optional[str]:
        """Extract GitHub profile URL"""
        match = re.search(self.github_pattern, text.lower())
        return match.group(0) if match else None
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from text"""
        from config import Config
        text_lower = text.lower()
        found_skills = []
        
        for skill in Config.COMMON_SKILLS:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education = []
        education_keywords = ['bachelor', 'master', 'phd', 'mba', 'b.s.', 'm.s.', 
                             'b.tech', 'm.tech', 'university', 'college', 'degree']
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in education_keywords):
                education.append(line.strip())
        
        return education[:5]  # Limit to 5 entries
    
    def _extract_experience(self, text: str) -> List[str]:
        """Extract work experience information"""
        experience = []
        experience_keywords = ['experience', 'worked', 'developer', 'engineer', 
                              'manager', 'analyst', 'consultant', 'intern']
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            # Look for year patterns (e.g., 2020-2023, 2020 - Present)
            year_pattern = r'\b(19|20)\d{2}\b'
            if (any(keyword in line_lower for keyword in experience_keywords) and 
                re.search(year_pattern, line)):
                experience.append(line.strip())
        
        return experience[:10]  # Limit to 10 entries
