"""
Job Description Analyzer Module
Analyzes and extracts requirements from job descriptions
"""
import re
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobAnalyzer:
    """Analyze job descriptions and extract requirements"""
    
    def __init__(self):
        self.required_keywords = ['required', 'must have', 'mandatory', 'essential']
        self.preferred_keywords = ['preferred', 'nice to have', 'plus', 'bonus']
        
    def analyze_job(self, job_description: str) -> Dict:
        """
        Analyze job description and extract structured information
        
        Args:
            job_description: Raw job description text
            
        Returns:
            Dictionary containing analyzed job information
        """
        try:
            return {
                'raw_text': job_description,
                'required_skills': self._extract_required_skills(job_description),
                'preferred_skills': self._extract_preferred_skills(job_description),
                'all_skills': self._extract_all_skills(job_description),
                'experience_required': self._extract_experience_requirement(job_description),
                'education_required': self._extract_education_requirement(job_description),
                'responsibilities': self._extract_responsibilities(job_description)
            }
        except Exception as e:
            logger.error(f"Error analyzing job description: {str(e)}")
            return {
                'raw_text': job_description,
                'required_skills': [],
                'preferred_skills': [],
                'all_skills': [],
                'experience_required': None,
                'education_required': [],
                'responsibilities': []
            }
    
    def _extract_all_skills(self, text: str) -> List[str]:
        """Extract all skills mentioned in job description"""
        from config import Config
        text_lower = text.lower()
        found_skills = []
        
        for skill in Config.COMMON_SKILLS:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        return found_skills
    
    def _extract_required_skills(self, text: str) -> List[str]:
        """Extract required skills from job description"""
        required_skills = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            # Check if line is in required section
            if any(keyword in line_lower for keyword in self.required_keywords):
                # Look at next few lines for skills
                for j in range(i, min(i + 10, len(lines))):
                    skills = self._extract_all_skills(lines[j])
                    required_skills.extend(skills)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_skills = []
        for skill in required_skills:
            if skill not in seen:
                seen.add(skill)
                unique_skills.append(skill)
        
        return unique_skills
    
    def _extract_preferred_skills(self, text: str) -> List[str]:
        """Extract preferred skills from job description"""
        preferred_skills = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            # Check if line is in preferred section
            if any(keyword in line_lower for keyword in self.preferred_keywords):
                # Look at next few lines for skills
                for j in range(i, min(i + 10, len(lines))):
                    skills = self._extract_all_skills(lines[j])
                    preferred_skills.extend(skills)
        
        # Remove duplicates
        return list(set(preferred_skills))
    
    def _extract_experience_requirement(self, text: str) -> Dict:
        """Extract experience requirements"""
        # Look for patterns like "3+ years", "5-7 years", "minimum 2 years"
        patterns = [
            r'(\d+)\s*\+?\s*years?\s+(?:of\s+)?experience',
            r'minimum\s+(\d+)\s+years?',
            r'at least\s+(\d+)\s+years?',
            r'(\d+)\s*-\s*(\d+)\s+years?'
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                if len(match.groups()) == 1:
                    return {
                        'min_years': int(match.group(1)),
                        'max_years': None
                    }
                else:
                    return {
                        'min_years': int(match.group(1)),
                        'max_years': int(match.group(2))
                    }
        
        return {'min_years': None, 'max_years': None}
    
    def _extract_education_requirement(self, text: str) -> List[str]:
        """Extract education requirements"""
        education = []
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'diploma',
                             'b.s.', 'm.s.', 'mba', 'b.tech', 'm.tech']
        
        lines = text.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in education_keywords):
                education.append(line.strip())
        
        return education[:3]  # Limit to 3 entries
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities"""
        responsibilities = []
        responsibility_keywords = ['responsibilities', 'duties', 'role', 'you will']
        
        lines = text.split('\n')
        in_responsibility_section = False
        
        for line in lines:
            line_lower = line.lower()
            line_stripped = line.strip()
            
            # Check if we're entering responsibilities section
            if any(keyword in line_lower for keyword in responsibility_keywords):
                in_responsibility_section = True
                continue
            
            # Check if we're leaving the section (new section header)
            if in_responsibility_section and line_stripped.isupper() and len(line_stripped) > 3:
                in_responsibility_section = False
            
            # Extract responsibilities (usually bulleted or numbered)
            if in_responsibility_section and len(line_stripped) > 20:
                if line_stripped.startswith(('•', '-', '*', '○')) or re.match(r'^\d+\.', line_stripped):
                    responsibilities.append(line_stripped)
        
        return responsibilities[:10]  # Limit to 10 entries
