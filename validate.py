"""
Quick validation script for the Resume-Job Matching System
Demonstrates basic functionality without requiring heavy ML dependencies
"""

def test_config():
    """Test configuration module"""
    print("Testing Configuration...")
    from config import Config
    
    assert Config.UPLOAD_FOLDER == 'uploads'
    assert 'pdf' in Config.ALLOWED_EXTENSIONS
    assert 'docx' in Config.ALLOWED_EXTENSIONS
    assert len(Config.COMMON_SKILLS) > 20
    print("✓ Configuration module works correctly")
    return True


def test_resume_parser_structure():
    """Test resume parser class structure"""
    print("\nTesting Resume Parser Structure...")
    from resume_parser import ResumeParser
    
    parser = ResumeParser()
    
    # Test email extraction
    email = parser._extract_email("Contact: john.doe@example.com")
    assert email == "john.doe@example.com"
    print("  ✓ Email extraction works")
    
    # Test phone extraction
    phone = parser._extract_phone("Call (555) 123-4567")
    assert phone is not None
    print("  ✓ Phone extraction works")
    
    # Test skills extraction
    skills = parser._extract_skills("I know Python, JavaScript, and Machine Learning")
    assert 'python' in skills
    assert 'javascript' in skills
    assert 'machine learning' in skills
    print(f"  ✓ Skills extraction works (found {len(skills)} skills)")
    
    # Test LinkedIn extraction
    linkedin = parser._extract_linkedin("Profile: linkedin.com/in/johndoe")
    assert linkedin == "linkedin.com/in/johndoe"
    print("  ✓ LinkedIn extraction works")
    
    # Test GitHub extraction  
    github = parser._extract_github("Code at github.com/johndoe")
    assert github == "github.com/johndoe"
    print("  ✓ GitHub extraction works")
    
    print("✓ Resume Parser module works correctly")
    return True


def test_job_analyzer_structure():
    """Test job analyzer class structure"""
    print("\nTesting Job Analyzer Structure...")
    from job_analyzer import JobAnalyzer
    
    analyzer = JobAnalyzer()
    
    job_desc = """
    Senior Python Developer
    
    Required Skills:
    - Python programming
    - JavaScript and React
    - SQL databases
    
    Preferred Skills:
    - AWS cloud experience
    - Docker and Kubernetes
    
    Experience: Minimum 5 years of software development
    
    Education: Bachelor's degree in Computer Science required
    """
    
    job_data = analyzer.analyze_job(job_desc)
    
    assert 'raw_text' in job_data
    assert 'all_skills' in job_data
    assert 'required_skills' in job_data
    assert 'experience_required' in job_data
    
    # Check skills extraction
    skills = [s.lower() for s in job_data['all_skills']]
    assert 'python' in skills
    print(f"  ✓ Skills extraction works (found {len(job_data['all_skills'])} skills)")
    
    # Check experience extraction
    exp = job_data['experience_required']
    assert exp['min_years'] == 5
    print(f"  ✓ Experience extraction works (found {exp['min_years']} years)")
    
    print("✓ Job Analyzer module works correctly")
    return True


def test_matching_engine_basic():
    """Test matching engine basic functionality"""
    print("\nTesting Matching Engine Basic Functions...")
    from matching_engine import MatchingEngine
    
    # Initialize with fallback mode (no model)
    matcher = MatchingEngine()
    
    # Test skills matching
    resume_skills = ['python', 'java', 'sql', 'react']
    job_skills = ['python', 'sql', 'javascript']
    
    score = matcher._calculate_skills_match(resume_skills, job_skills)
    assert 0 <= score <= 1
    print(f"  ✓ Skills matching works (score: {score:.2f})")
    
    # Test matching skills list
    matching = matcher._get_matching_skills(resume_skills, job_skills)
    assert 'python' in matching
    assert 'sql' in matching
    print(f"  ✓ Matching skills detection works (found {len(matching)} matches)")
    
    # Test missing skills list
    required_skills = ['python', 'javascript', 'docker']
    missing = matcher._get_missing_skills(resume_skills, required_skills)
    assert 'javascript' in missing
    assert 'docker' in missing
    print(f"  ✓ Missing skills detection works (found {len(missing)} missing)")
    
    # Test match categorization
    category = matcher._categorize_match(0.80)
    assert category == "Excellent Match"
    print("  ✓ Match categorization works")
    
    print("✓ Matching Engine basic functions work correctly")
    return True


def test_integration():
    """Test integration between components"""
    print("\nTesting Component Integration...")
    from resume_parser import ResumeParser
    from job_analyzer import JobAnalyzer
    from matching_engine import MatchingEngine
    
    parser = ResumeParser()
    analyzer = JobAnalyzer()
    matcher = MatchingEngine()
    
    # Create sample resume
    resume_text = """
    John Doe
    john.doe@email.com | (555) 123-4567
    linkedin.com/in/johndoe | github.com/johndoe
    
    EXPERIENCE
    Senior Software Engineer at Tech Corp (2020 - Present)
    - Developed web applications using Python and JavaScript
    - Built machine learning models
    - Worked with Docker and AWS
    
    EDUCATION
    Bachelor of Science in Computer Science, 2018
    
    SKILLS
    Python, JavaScript, React, SQL, Machine Learning, Docker, AWS, Git
    """
    
    # Create sample job
    job_description = """
    Senior Full Stack Developer
    
    Required Skills:
    - Python and JavaScript
    - React framework
    - SQL databases
    
    Preferred:
    - Machine Learning experience
    - AWS cloud platform
    - Docker containers
    
    3+ years of experience required
    """
    
    # Parse and analyze
    resume_data = parser._extract_information(resume_text)
    job_data = analyzer.analyze_job(job_description)
    
    print(f"  ✓ Parsed resume (found {len(resume_data['skills'])} skills)")
    print(f"  ✓ Analyzed job (found {len(job_data['all_skills'])} skills)")
    
    # Perform matching
    match_result = matcher.match_resume_to_job(resume_data, job_data)
    
    assert 'overall_score' in match_result
    assert 'match_category' in match_result
    assert 'matching_skills' in match_result
    assert 'recommendation' in match_result
    
    print(f"  ✓ Matching completed:")
    print(f"    - Overall Score: {match_result['overall_score']*100:.1f}%")
    print(f"    - Category: {match_result['match_category']}")
    print(f"    - Matching Skills: {len(match_result['matching_skills'])}")
    
    assert match_result['overall_score'] > 0.5, "Should have good match score"
    
    print("✓ Component integration works correctly")
    return True


def test_flask_app_structure():
    """Test Flask app structure"""
    print("\nTesting Flask App Structure...")
    from app import app
    
    assert app is not None
    print("  ✓ Flask app created successfully")
    
    # Test routes exist
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    assert '/' in routes
    assert '/api/health' in routes
    assert '/api/match' in routes
    print(f"  ✓ API routes configured ({len(routes)} routes)")
    
    print("✓ Flask App structure is correct")
    return True


def run_all_tests():
    """Run all validation tests"""
    print("=" * 70)
    print("AI-POWERED RESUME-JOB MATCHING SYSTEM - VALIDATION")
    print("=" * 70)
    
    tests = [
        test_config,
        test_resume_parser_structure,
        test_job_analyzer_structure,
        test_matching_engine_basic,
        test_integration,
        test_flask_app_structure
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            failed += 1
            print(f"✗ {test.__name__} failed: {str(e)}")
    
    print("\n" + "=" * 70)
    print(f"VALIDATION RESULTS: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("\n🎉 All validations passed! The system is working correctly.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the web app: python app.py")
        print("3. Visit http://localhost:5000 to use the system")
        print("4. Or run examples: python examples.py")
        return True
    else:
        print(f"\n⚠️  {failed} validation(s) failed. Please review the errors above.")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
