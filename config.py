"""
Configuration settings for the Resume-Job Matching System
"""
import os

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Upload settings
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # NLP Model settings
    SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'
    
    # Matching thresholds
    MIN_MATCH_SCORE = 0.0
    EXCELLENT_MATCH_THRESHOLD = 0.75
    GOOD_MATCH_THRESHOLD = 0.60
    FAIR_MATCH_THRESHOLD = 0.45
    
    # Skills extraction
    COMMON_SKILLS = [
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'swift',
        'kotlin', 'typescript', 'go', 'rust', 'scala', 'r',
        'machine learning', 'deep learning', 'neural networks', 'nlp',
        'computer vision', 'data science', 'data analysis', 'statistics',
        'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'oracle',
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
        'git', 'agile', 'scrum', 'devops', 'ci/cd',
        'react', 'angular', 'vue', 'node.js', 'django', 'flask',
        'tensorflow', 'pytorch', 'keras', 'scikit-learn',
        'html', 'css', 'rest api', 'graphql', 'microservices',
        'leadership', 'communication', 'problem solving', 'teamwork'
    ]
    
    @staticmethod
    def init_app(app):
        """Initialize application configuration"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
