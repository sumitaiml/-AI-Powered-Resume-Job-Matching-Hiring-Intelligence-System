# Quick Start Guide

## AI-Powered Resume-Job Matching System

This guide will help you get started quickly with the system.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 2GB of free disk space (for ML models)
- Internet connection (for initial setup)

## Installation

### Step 1: Clone or Download

If you haven't already, get the code:
```bash
git clone https://github.com/sumitaiml/-AI-Powered-Resume-Job-Matching-Hiring-Intelligence-System.git
cd -AI-Powered-Resume-Job-Matching-Hiring-Intelligence-System
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages. First installation may take 5-10 minutes.

### Step 4: Verify Installation

```bash
python validate.py
```

You should see "All validations passed!" message.

## Usage Options

### Option 1: Web Interface (Easiest)

Start the web server:
```bash
python app.py
```

Then open your browser and go to:
```
http://localhost:5000
```

You'll see a beautiful interface where you can:
1. Upload a resume (PDF, DOCX, or TXT)
2. Paste a job description
3. Click "Analyze & Match"
4. Get instant results with scores and recommendations

### Option 2: Command Line

Run the examples to see how it works:
```bash
python examples.py
```

This will show three examples:
- Basic resume-job matching
- Batch matching (one resume vs multiple jobs)
- API usage guide

### Option 3: Python API

Use it in your own Python code:

```python
from resume_parser import ResumeParser
from job_analyzer import JobAnalyzer
from matching_engine import MatchingEngine

# Initialize
parser = ResumeParser()
analyzer = JobAnalyzer()
matcher = MatchingEngine()

# Parse resume
resume_data = parser.parse_resume('resume.pdf', 'pdf')

# Analyze job
job_data = analyzer.analyze_job(job_description_text)

# Get match
result = matcher.match_resume_to_job(resume_data, job_data)

print(f"Match Score: {result['overall_score']*100:.1f}%")
print(f"Category: {result['match_category']}")
```

### Option 4: REST API

Start the server:
```bash
python app.py
```

Then make HTTP requests:

```bash
# Match resume with job
curl -X POST http://localhost:5000/api/match \
  -F "file=@/path/to/resume.pdf" \
  -F "job_description=Senior Python Developer..."
```

## Quick Test

Want to test it right away without any files? Run:

```bash
python validate.py
```

This will run through all components with sample data and show you results.

## Common Issues

### Issue: "ModuleNotFoundError"
**Solution:** Make sure you installed dependencies: `pip install -r requirements.txt`

### Issue: Model download fails
**Solution:** The AI model downloads automatically on first run. If it fails:
1. Check your internet connection
2. The system will automatically fall back to basic matching

### Issue: "Permission denied" on file upload
**Solution:** Make sure the `uploads/` directory exists and is writable:
```bash
mkdir uploads
chmod 755 uploads
```

### Issue: Port 5000 already in use
**Solution:** Use a different port:
```bash
python app.py --port 5001
```
Or edit `app.py` and change the port number.

## Understanding the Results

When you match a resume with a job, you get:

1. **Overall Score (0-100%)**: Combined score from all factors
2. **Match Category**: 
   - Excellent Match (75%+): Highly recommended
   - Good Match (60-74%): Recommended
   - Fair Match (45-59%): Consider with review
   - Poor Match (<45%): Significant gaps

3. **Semantic Similarity**: How well the resume and job align contextually
4. **Skills Match**: Percentage of job skills found in resume
5. **Required Skills Match**: Percentage of mandatory skills present
6. **Matching Skills**: List of skills that match
7. **Missing Skills**: Skills required but not found in resume
8. **Recommendation**: AI-generated hiring recommendation

## Next Steps

1. **Try with Your Own Data**: Upload your resume and job descriptions
2. **Integrate**: Use the API to integrate with your hiring system
3. **Customize**: Edit `config.py` to add more skills or adjust thresholds
4. **Scale**: Deploy with gunicorn for production use

## Getting Help

- Check the main README.md for detailed documentation
- Run `python examples.py` to see usage examples
- Review the code - it's well-commented
- Open an issue on GitHub for bugs or questions

## Tips for Best Results

1. **Resume Format**: PDF and DOCX work best. Ensure text is selectable (not scanned images)
2. **Job Descriptions**: Include clear "Required Skills" and "Preferred Skills" sections
3. **Skills Keywords**: Use common industry terms (e.g., "Python" not "python programming language")
4. **Complete Information**: More detailed resumes and job descriptions = better matches

Happy Matching! 🚀
