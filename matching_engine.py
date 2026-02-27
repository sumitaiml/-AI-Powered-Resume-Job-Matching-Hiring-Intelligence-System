"""
AI-Powered Matching Engine
Uses NLP and machine learning to match resumes with job descriptions
"""
import numpy as np
from typing import Dict, List, Tuple
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MatchingEngine:
    """AI-powered matching engine for resumes and jobs"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the matching engine with a sentence transformer model
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        try:
            logger.info(f"Loading sentence transformer model: {model_name}")
            self.model = SentenceTransformer(model_name)
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self.model = None
    
    def match_resume_to_job(self, resume_data: Dict, job_data: Dict) -> Dict:
        """
        Match a resume to a job description using AI
        
        Args:
            resume_data: Parsed resume information
            job_data: Analyzed job information
            
        Returns:
            Dictionary containing match score and detailed analysis
        """
        try:
            if self.model is None:
                return self._fallback_matching(resume_data, job_data)
            
            # Calculate different matching scores
            semantic_score = self._calculate_semantic_similarity(
                resume_data['raw_text'], 
                job_data['raw_text']
            )
            
            skills_score = self._calculate_skills_match(
                resume_data['skills'],
                job_data['all_skills']
            )
            
            required_skills_score = self._calculate_required_skills_match(
                resume_data['skills'],
                job_data['required_skills']
            )
            
            # Weighted overall score
            overall_score = (
                semantic_score * 0.4 +
                skills_score * 0.3 +
                required_skills_score * 0.3
            )
            
            return {
                'overall_score': round(overall_score, 3),
                'semantic_similarity': round(semantic_score, 3),
                'skills_match': round(skills_score, 3),
                'required_skills_match': round(required_skills_score, 3),
                'matching_skills': self._get_matching_skills(
                    resume_data['skills'],
                    job_data['all_skills']
                ),
                'missing_required_skills': self._get_missing_skills(
                    resume_data['skills'],
                    job_data['required_skills']
                ),
                'match_category': self._categorize_match(overall_score),
                'recommendation': self._generate_recommendation(
                    overall_score,
                    resume_data,
                    job_data
                )
            }
            
        except Exception as e:
            logger.error(f"Error in matching: {str(e)}")
            return self._fallback_matching(resume_data, job_data)
    
    def _calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity using sentence transformers"""
        try:
            if not text1 or not text2:
                return 0.0
            
            # Encode texts
            embedding1 = self.model.encode([text1[:5000]])[0]  # Limit text length
            embedding2 = self.model.encode([text2[:5000]])[0]
            
            # Calculate cosine similarity
            similarity = cosine_similarity(
                embedding1.reshape(1, -1),
                embedding2.reshape(1, -1)
            )[0][0]
            
            return max(0.0, min(1.0, float(similarity)))
            
        except Exception as e:
            logger.error(f"Error calculating semantic similarity: {str(e)}")
            return 0.0
    
    def _calculate_skills_match(self, resume_skills: List[str], 
                                job_skills: List[str]) -> float:
        """Calculate skills match percentage"""
        if not job_skills:
            return 0.5  # Neutral score if no skills specified
        
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]
        
        matching = sum(1 for skill in job_skills_lower if skill in resume_skills_lower)
        return matching / len(job_skills_lower) if job_skills_lower else 0.0
    
    def _calculate_required_skills_match(self, resume_skills: List[str],
                                        required_skills: List[str]) -> float:
        """Calculate match for required skills"""
        if not required_skills:
            return 1.0  # Perfect score if no required skills
        
        resume_skills_lower = [s.lower() for s in resume_skills]
        required_skills_lower = [s.lower() for s in required_skills]
        
        matching = sum(1 for skill in required_skills_lower if skill in resume_skills_lower)
        return matching / len(required_skills_lower)
    
    def _get_matching_skills(self, resume_skills: List[str],
                            job_skills: List[str]) -> List[str]:
        """Get list of matching skills"""
        resume_skills_lower = {s.lower(): s for s in resume_skills}
        job_skills_lower = [s.lower() for s in job_skills]
        
        return [resume_skills_lower[s] for s in job_skills_lower 
                if s in resume_skills_lower]
    
    def _get_missing_skills(self, resume_skills: List[str],
                           required_skills: List[str]) -> List[str]:
        """Get list of missing required skills"""
        resume_skills_lower = [s.lower() for s in resume_skills]
        return [s for s in required_skills if s.lower() not in resume_skills_lower]
    
    def _categorize_match(self, score: float) -> str:
        """Categorize match quality based on score"""
        from config import Config
        
        if score >= Config.EXCELLENT_MATCH_THRESHOLD:
            return "Excellent Match"
        elif score >= Config.GOOD_MATCH_THRESHOLD:
            return "Good Match"
        elif score >= Config.FAIR_MATCH_THRESHOLD:
            return "Fair Match"
        else:
            return "Poor Match"
    
    def _generate_recommendation(self, score: float, resume_data: Dict,
                                job_data: Dict) -> str:
        """Generate hiring recommendation"""
        from config import Config
        
        if score >= Config.EXCELLENT_MATCH_THRESHOLD:
            return "Highly recommended for interview. Strong alignment with job requirements."
        elif score >= Config.GOOD_MATCH_THRESHOLD:
            return "Recommended for interview. Good fit with room for growth."
        elif score >= Config.FAIR_MATCH_THRESHOLD:
            return "Consider for interview. May need additional training in some areas."
        else:
            return "Not recommended. Significant gaps in required qualifications."
    
    def _fallback_matching(self, resume_data: Dict, job_data: Dict) -> Dict:
        """Fallback matching when AI model is not available"""
        skills_score = self._calculate_skills_match(
            resume_data['skills'],
            job_data['all_skills']
        )
        
        return {
            'overall_score': round(skills_score, 3),
            'semantic_similarity': 0.0,
            'skills_match': round(skills_score, 3),
            'required_skills_match': 0.0,
            'matching_skills': self._get_matching_skills(
                resume_data['skills'],
                job_data['all_skills']
            ),
            'missing_required_skills': [],
            'match_category': self._categorize_match(skills_score),
            'recommendation': 'Basic skills-based matching used. AI model unavailable.'
        }
    
    def batch_match(self, resume_data: Dict, jobs_data: List[Dict]) -> List[Dict]:
        """
        Match a single resume against multiple jobs
        
        Args:
            resume_data: Parsed resume information
            jobs_data: List of analyzed job descriptions
            
        Returns:
            List of match results sorted by score
        """
        matches = []
        for i, job_data in enumerate(jobs_data):
            match_result = self.match_resume_to_job(resume_data, job_data)
            match_result['job_index'] = i
            matches.append(match_result)
        
        # Sort by overall score (descending)
        matches.sort(key=lambda x: x['overall_score'], reverse=True)
        return matches
