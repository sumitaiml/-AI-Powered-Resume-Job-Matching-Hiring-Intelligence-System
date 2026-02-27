"""
Example usage of the Resume-Job Matching System
"""
from resume_parser import ResumeParser
from job_analyzer import JobAnalyzer
from matching_engine import MatchingEngine


def example_1_basic_matching():
    """Example: Basic resume-job matching"""
    print("=" * 60)
    print("Example 1: Basic Resume-Job Matching")
    print("=" * 60)
    
    # Sample resume text
    resume_text = """
    John Doe
    john.doe@email.com | (555) 123-4567
    linkedin.com/in/johndoe | github.com/johndoe
    
    EXPERIENCE
    Senior Software Engineer at Tech Corp (2020 - Present)
    - Developed scalable web applications using Python, Django, and React
    - Implemented machine learning models for recommendation systems
    - Led team of 5 engineers in agile environment
    
    Software Engineer at StartUp Inc (2018 - 2020)
    - Built RESTful APIs using Flask and PostgreSQL
    - Worked with Docker and Kubernetes for deployment
    
    EDUCATION
    Bachelor of Science in Computer Science
    University of Technology, 2018
    
    SKILLS
    Python, JavaScript, React, Django, Flask, Machine Learning,
    TensorFlow, Docker, Kubernetes, AWS, PostgreSQL, Git, Agile
    """
    
    # Sample job description
    job_description = """
    Senior Full Stack Developer
    
    We are seeking an experienced Full Stack Developer to join our team.
    
    Required Skills:
    - 3+ years of experience in software development
    - Strong proficiency in Python and JavaScript
    - Experience with React or Angular
    - Knowledge of Django or Flask
    - Database experience (PostgreSQL, MySQL)
    
    Preferred Skills:
    - Machine Learning experience
    - Cloud platform experience (AWS, Azure, GCP)
    - Docker and Kubernetes knowledge
    - Agile/Scrum methodology
    
    Responsibilities:
    - Design and develop full-stack web applications
    - Collaborate with cross-functional teams
    - Mentor junior developers
    """
    
    # Initialize components
    parser = ResumeParser()
    analyzer = JobAnalyzer()
    matcher = MatchingEngine()
    
    # Parse resume (simulating text file)
    resume_data = parser._extract_information(resume_text)
    print(f"\n✓ Resume parsed successfully")
    print(f"  - Email: {resume_data['email']}")
    print(f"  - Skills found: {len(resume_data['skills'])}")
    
    # Analyze job
    job_data = analyzer.analyze_job(job_description)
    print(f"\n✓ Job analyzed successfully")
    print(f"  - Required skills: {len(job_data['required_skills'])}")
    print(f"  - All skills: {len(job_data['all_skills'])}")
    
    # Perform matching
    match_result = matcher.match_resume_to_job(resume_data, job_data)
    
    print(f"\n{'='*60}")
    print("MATCHING RESULTS")
    print(f"{'='*60}")
    print(f"Overall Score: {match_result['overall_score']*100:.1f}%")
    print(f"Match Category: {match_result['match_category']}")
    print(f"Semantic Similarity: {match_result['semantic_similarity']*100:.1f}%")
    print(f"Skills Match: {match_result['skills_match']*100:.1f}%")
    print(f"Required Skills Match: {match_result['required_skills_match']*100:.1f}%")
    
    print(f"\nMatching Skills: {', '.join(match_result['matching_skills'])}")
    if match_result['missing_required_skills']:
        print(f"Missing Required Skills: {', '.join(match_result['missing_required_skills'])}")
    
    print(f"\nRecommendation: {match_result['recommendation']}")
    print()


def example_2_batch_matching():
    """Example: Match one resume against multiple jobs"""
    print("=" * 60)
    print("Example 2: Batch Matching (1 Resume vs Multiple Jobs)")
    print("=" * 60)
    
    resume_text = """
    Jane Smith
    jane.smith@email.com
    
    Data Scientist with 4 years of experience
    
    SKILLS
    Python, R, Machine Learning, Deep Learning, TensorFlow, 
    PyTorch, scikit-learn, Pandas, NumPy, SQL, Data Visualization
    
    EXPERIENCE
    Data Scientist at AI Company (2020-Present)
    - Built ML models for predictive analytics
    - Deployed models using Docker and AWS
    """
    
    job_descriptions = [
        """
        Data Scientist Position
        Required: Python, Machine Learning, SQL, Statistics
        Preferred: TensorFlow, AWS
        """,
        """
        Machine Learning Engineer
        Required: Python, Deep Learning, TensorFlow or PyTorch
        Preferred: Docker, Kubernetes, Cloud platforms
        """,
        """
        Backend Developer
        Required: Java, Spring Boot, REST APIs
        Preferred: Microservices, Docker
        """
    ]
    
    parser = ResumeParser()
    analyzer = JobAnalyzer()
    matcher = MatchingEngine()
    
    resume_data = parser._extract_information(resume_text)
    jobs_data = [analyzer.analyze_job(jd) for jd in job_descriptions]
    
    matches = matcher.batch_match(resume_data, jobs_data)
    
    print(f"\n{'='*60}")
    print("BATCH MATCHING RESULTS (Sorted by Score)")
    print(f"{'='*60}\n")
    
    for i, match in enumerate(matches, 1):
        print(f"{i}. Job {match['job_index'] + 1}")
        print(f"   Score: {match['overall_score']*100:.1f}%")
        print(f"   Category: {match['match_category']}")
        print(f"   Matching Skills: {', '.join(match['matching_skills'][:5])}")
        print()


def example_3_api_usage():
    """Example: How to use the REST API"""
    print("=" * 60)
    print("Example 3: REST API Usage")
    print("=" * 60)
    
    print("""
To use the REST API, start the Flask server:

    python app.py

Then make API calls:

1. Parse Resume:
   POST /api/parse-resume
   Content-Type: multipart/form-data
   Body: file=<resume.pdf>

2. Analyze Job:
   POST /api/analyze-job
   Content-Type: application/json
   Body: {"job_description": "..."}

3. Match Resume with Job:
   POST /api/match
   Content-Type: multipart/form-data
   Body: file=<resume.pdf>, job_description="..."

4. Batch Match:
   POST /api/batch-match
   Content-Type: application/json
   Body: {
       "resume_data": {...},
       "job_descriptions": ["...", "..."]
   }

Example using curl:

curl -X POST http://localhost:5000/api/match \\
  -F "file=@resume.pdf" \\
  -F "job_description=Senior Python Developer required..."

Example using Python requests:

import requests

# Match resume with job
with open('resume.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/match',
        files={'file': f},
        data={'job_description': 'Python Developer...'}
    )
    result = response.json()
    print(f"Match Score: {result['match']['overall_score']}")
    """)


if __name__ == '__main__':
    example_1_basic_matching()
    example_2_batch_matching()
    example_3_api_usage()
