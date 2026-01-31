"""
Test Suite for Resume-Job Matching System
"""
import unittest
from resume_parser import ResumeParser
from job_analyzer import JobAnalyzer
from matching_engine import MatchingEngine


class TestResumeParser(unittest.TestCase):
    """Test resume parsing functionality"""
    
    def setUp(self):
        self.parser = ResumeParser()
    
    def test_email_extraction(self):
        """Test email extraction from text"""
        text = "Contact me at john.doe@example.com"
        email = self.parser._extract_email(text)
        self.assertEqual(email, "john.doe@example.com")
    
    def test_phone_extraction(self):
        """Test phone number extraction"""
        text = "Call me at (555) 123-4567"
        phone = self.parser._extract_phone(text)
        self.assertIsNotNone(phone)
    
    def test_skills_extraction(self):
        """Test skills extraction"""
        text = "I have experience with Python, JavaScript, and Machine Learning"
        skills = self.parser._extract_skills(text)
        self.assertIn('python', skills)
        self.assertIn('javascript', skills)
        self.assertIn('machine learning', skills)
    
    def test_linkedin_extraction(self):
        """Test LinkedIn profile extraction"""
        text = "Find me on linkedin.com/in/johndoe"
        linkedin = self.parser._extract_linkedin(text)
        self.assertEqual(linkedin, "linkedin.com/in/johndoe")
    
    def test_github_extraction(self):
        """Test GitHub profile extraction"""
        text = "My code is at github.com/johndoe"
        github = self.parser._extract_github(text)
        self.assertEqual(github, "github.com/johndoe")


class TestJobAnalyzer(unittest.TestCase):
    """Test job description analysis"""
    
    def setUp(self):
        self.analyzer = JobAnalyzer()
    
    def test_skills_extraction(self):
        """Test extracting skills from job description"""
        job_desc = "Looking for Python and React developer with AWS experience"
        job_data = self.analyzer.analyze_job(job_desc)
        self.assertIn('python', job_data['all_skills'])
        self.assertIn('react', job_data['all_skills'])
        self.assertIn('aws', job_data['all_skills'])
    
    def test_experience_extraction(self):
        """Test experience requirement extraction"""
        job_desc = "Minimum 5 years of experience required"
        job_data = self.analyzer.analyze_job(job_desc)
        self.assertEqual(job_data['experience_required']['min_years'], 5)
    
    def test_required_skills_section(self):
        """Test identifying required skills section"""
        job_desc = """
        Required Skills:
        - Python
        - SQL
        """
        job_data = self.analyzer.analyze_job(job_desc)
        # Should find skills in required section
        self.assertTrue(len(job_data['all_skills']) > 0)


class TestMatchingEngine(unittest.TestCase):
    """Test matching engine functionality"""
    
    def setUp(self):
        self.matcher = MatchingEngine()
        self.parser = ResumeParser()
        self.analyzer = JobAnalyzer()
    
    def test_skills_match_calculation(self):
        """Test skills matching calculation"""
        resume_skills = ['python', 'java', 'sql']
        job_skills = ['python', 'sql', 'javascript']
        score = self.matcher._calculate_skills_match(resume_skills, job_skills)
        # Should match 2 out of 3 skills
        self.assertAlmostEqual(score, 2/3, places=2)
    
    def test_perfect_skills_match(self):
        """Test perfect skills match"""
        skills = ['python', 'javascript', 'react']
        score = self.matcher._calculate_skills_match(skills, skills)
        self.assertEqual(score, 1.0)
    
    def test_no_skills_match(self):
        """Test no skills matching"""
        resume_skills = ['python', 'java']
        job_skills = ['ruby', 'php']
        score = self.matcher._calculate_skills_match(resume_skills, job_skills)
        self.assertEqual(score, 0.0)
    
    def test_matching_skills_list(self):
        """Test getting list of matching skills"""
        resume_skills = ['Python', 'Java', 'SQL']
        job_skills = ['python', 'sql', 'javascript']
        matching = self.matcher._get_matching_skills(resume_skills, job_skills)
        self.assertEqual(len(matching), 2)
        # Should preserve original case from resume
        self.assertIn('Python', matching)
        self.assertIn('SQL', matching)
    
    def test_missing_skills_list(self):
        """Test getting list of missing required skills"""
        resume_skills = ['python', 'java']
        required_skills = ['python', 'javascript', 'react']
        missing = self.matcher._get_missing_skills(resume_skills, required_skills)
        self.assertEqual(len(missing), 2)
        self.assertIn('javascript', missing)
        self.assertIn('react', missing)
    
    def test_match_category_excellent(self):
        """Test excellent match categorization"""
        category = self.matcher._categorize_match(0.80)
        self.assertEqual(category, "Excellent Match")
    
    def test_match_category_good(self):
        """Test good match categorization"""
        category = self.matcher._categorize_match(0.65)
        self.assertEqual(category, "Good Match")
    
    def test_match_category_fair(self):
        """Test fair match categorization"""
        category = self.matcher._categorize_match(0.50)
        self.assertEqual(category, "Fair Match")
    
    def test_match_category_poor(self):
        """Test poor match categorization"""
        category = self.matcher._categorize_match(0.30)
        self.assertEqual(category, "Poor Match")
    
    def test_full_matching_workflow(self):
        """Test complete matching workflow"""
        resume_text = """
        John Doe
        john@email.com
        
        Skills: Python, JavaScript, React, SQL, Machine Learning
        Experience: 5 years as Software Engineer
        """
        
        job_description = """
        Senior Developer Position
        Required: Python, JavaScript, SQL
        Preferred: React, Machine Learning
        3+ years experience required
        """
        
        resume_data = self.parser._extract_information(resume_text)
        job_data = self.analyzer.analyze_job(job_description)
        match_result = self.matcher.match_resume_to_job(resume_data, job_data)
        
        # Should have high match score
        self.assertGreater(match_result['overall_score'], 0.5)
        self.assertIsNotNone(match_result['match_category'])
        self.assertIsNotNone(match_result['recommendation'])
        self.assertIn('matching_skills', match_result)
        self.assertIn('missing_required_skills', match_result)
    
    def test_batch_matching(self):
        """Test batch matching functionality"""
        resume_text = "Skills: Python, Java, SQL"
        job_desc_1 = "Required: Python, SQL"
        job_desc_2 = "Required: Ruby, PHP"
        job_desc_3 = "Required: Java, SQL"
        
        resume_data = self.parser._extract_information(resume_text)
        jobs_data = [
            self.analyzer.analyze_job(job_desc_1),
            self.analyzer.analyze_job(job_desc_2),
            self.analyzer.analyze_job(job_desc_3)
        ]
        
        matches = self.matcher.batch_match(resume_data, jobs_data)
        
        # Should return 3 matches
        self.assertEqual(len(matches), 3)
        # Should be sorted by score (descending)
        self.assertGreaterEqual(matches[0]['overall_score'], matches[1]['overall_score'])
        self.assertGreaterEqual(matches[1]['overall_score'], matches[2]['overall_score'])


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def setUp(self):
        self.parser = ResumeParser()
        self.analyzer = JobAnalyzer()
        self.matcher = MatchingEngine()
    
    def test_high_quality_match(self):
        """Test a high-quality candidate-job match"""
        resume_text = """
        Senior Software Engineer
        contact@example.com | linkedin.com/in/engineer
        
        SKILLS
        Python, Django, Flask, React, JavaScript, PostgreSQL, Docker,
        Kubernetes, AWS, Machine Learning, TensorFlow, Git, Agile, CI/CD
        
        EXPERIENCE
        Senior Software Engineer - Tech Corp (2019-Present)
        - Led development of ML-powered applications
        - Managed cloud infrastructure on AWS
        - Implemented CI/CD pipelines
        
        EDUCATION
        M.S. Computer Science, MIT, 2019
        """
        
        job_description = """
        Senior Full Stack Developer
        
        REQUIRED QUALIFICATIONS:
        - 5+ years of experience in software development
        - Strong proficiency in Python and JavaScript
        - Experience with React or Vue.js
        - Knowledge of Django or Flask
        - Database experience (PostgreSQL preferred)
        - Understanding of Docker and Kubernetes
        
        PREFERRED QUALIFICATIONS:
        - Machine Learning experience
        - AWS or cloud platform experience
        - CI/CD pipeline knowledge
        - Master's degree in Computer Science
        
        RESPONSIBILITIES:
        - Design and develop full-stack applications
        - Implement machine learning features
        - Mentor junior developers
        - Collaborate with product team
        """
        
        resume_data = self.parser._extract_information(resume_text)
        job_data = self.analyzer.analyze_job(job_description)
        match_result = self.matcher.match_resume_to_job(resume_data, job_data)
        
        # Assertions for high-quality match
        self.assertGreater(match_result['overall_score'], 0.6,
                          "High-quality match should score above 60%")
        self.assertIn(match_result['match_category'], 
                     ['Excellent Match', 'Good Match'])
        self.assertGreater(len(match_result['matching_skills']), 5,
                          "Should have many matching skills")
        self.assertIn('python', [s.lower() for s in match_result['matching_skills']])
    
    def test_poor_quality_match(self):
        """Test a poor candidate-job match"""
        resume_text = """
        Junior Designer
        designer@example.com
        
        SKILLS
        Photoshop, Illustrator, Figma, UI/UX Design
        
        EXPERIENCE
        Graphic Designer - Design Studio (2021-Present)
        """
        
        job_description = """
        Senior Backend Engineer
        
        REQUIRED:
        - 5+ years backend development
        - Strong Java and Spring Boot
        - Microservices architecture
        - PostgreSQL and MongoDB
        """
        
        resume_data = self.parser._extract_information(resume_text)
        job_data = self.analyzer.analyze_job(job_description)
        match_result = self.matcher.match_resume_to_job(resume_data, job_data)
        
        # Assertions for poor match
        self.assertLess(match_result['overall_score'], 0.5,
                       "Poor match should score below 50%")
        self.assertEqual(match_result['match_category'], 'Poor Match')


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestResumeParser))
    suite.addTests(loader.loadTestsFromTestCase(TestJobAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestMatchingEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
