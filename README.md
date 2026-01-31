# 🤖 AI-Powered Resume–Job Matching & Hiring Intelligence System

A comprehensive, AI-powered system that intelligently matches resumes with job descriptions using advanced Natural Language Processing (NLP) and machine learning techniques. This system provides hiring intelligence through semantic analysis, skills extraction, and intelligent scoring.

## 🌟 Features

- **Resume Parsing**: Extract structured information from PDF, DOCX, and TXT resume files
- **Job Analysis**: Intelligent analysis of job descriptions to extract requirements and skills
- **AI-Powered Matching**: Uses sentence transformers and semantic similarity for accurate matching
- **Skills Extraction**: Automatically identifies technical and soft skills
- **Scoring System**: Multi-dimensional scoring (semantic similarity, skills match, required skills)
- **Batch Matching**: Match one resume against multiple job postings
- **Web Interface**: Beautiful, user-friendly web UI for easy interaction
- **REST API**: Complete API for integration with other systems
- **Hiring Intelligence**: Provides recommendations and insights for hiring decisions

## 📋 Requirements

- Python 3.8+
- See `requirements.txt` for detailed dependencies

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/sumitaiml/-AI-Powered-Resume-Job-Matching-Hiring-Intelligence-System.git
cd -AI-Powered-Resume-Job-Matching-Hiring-Intelligence-System
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download required NLP models (first run will download automatically):
```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

## 💻 Usage

### Web Interface

Start the Flask web server:
```bash
python app.py
```

Visit `http://localhost:5000` in your browser to access the web interface.

Features:
- Upload resume files (PDF, DOCX, TXT)
- Paste job descriptions
- Get instant matching scores and analysis
- View matching and missing skills
- Receive hiring recommendations

### Command Line Usage

```python
from resume_parser import ResumeParser
from job_analyzer import JobAnalyzer
from matching_engine import MatchingEngine

# Initialize components
parser = ResumeParser()
analyzer = JobAnalyzer()
matcher = MatchingEngine()

# Parse resume
resume_data = parser.parse_resume('path/to/resume.pdf', 'pdf')

# Analyze job description
job_data = analyzer.analyze_job(job_description_text)

# Get matching score
match_result = matcher.match_resume_to_job(resume_data, job_data)

print(f"Match Score: {match_result['overall_score']}")
print(f"Category: {match_result['match_category']}")
print(f"Recommendation: {match_result['recommendation']}")
```

### REST API

#### 1. Parse Resume
```bash
curl -X POST http://localhost:5000/api/parse-resume \
  -F "file=@resume.pdf"
```

#### 2. Analyze Job Description
```bash
curl -X POST http://localhost:5000/api/analyze-job \
  -H "Content-Type: application/json" \
  -d '{"job_description": "Python Developer with 3+ years..."}'
```

#### 3. Match Resume with Job
```bash
curl -X POST http://localhost:5000/api/match \
  -F "file=@resume.pdf" \
  -F "job_description=Senior Python Developer..."
```

#### 4. Batch Match (Multiple Jobs)
```bash
curl -X POST http://localhost:5000/api/batch-match \
  -H "Content-Type: application/json" \
  -d '{
    "resume_data": {...},
    "job_descriptions": ["Job 1...", "Job 2..."]
  }'
```

## 📊 Matching Algorithm

The system uses a sophisticated multi-dimensional matching algorithm:

1. **Semantic Similarity (40% weight)**
   - Uses sentence transformers (all-MiniLM-L6-v2 model)
   - Calculates cosine similarity between resume and job description embeddings
   - Captures contextual understanding beyond keyword matching

2. **Skills Match (30% weight)**
   - Compares candidate skills with all job requirements
   - Identifies matching skills and gaps

3. **Required Skills Match (30% weight)**
   - Focuses specifically on mandatory requirements
   - Critical for filtering candidates

### Scoring Categories

- **Excellent Match** (≥75%): Highly recommended for interview
- **Good Match** (60-74%): Recommended with potential for growth
- **Fair Match** (45-59%): Consider with additional evaluation
- **Poor Match** (<45%): Significant gaps in qualifications

## 🏗️ Architecture

```
├── app.py                 # Flask web application & REST API
├── resume_parser.py       # Resume parsing module
├── job_analyzer.py        # Job description analysis
├── matching_engine.py     # AI matching engine
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── examples.py           # Usage examples
└── README.md            # Documentation
```

## 🔧 Configuration

Edit `config.py` to customize:

- Upload folder location
- Allowed file extensions
- Maximum file size
- Matching thresholds
- NLP model selection
- Skills database

## 📝 Examples

See `examples.py` for detailed usage examples:

```bash
python examples.py
```

This will run three examples:
1. Basic resume-job matching
2. Batch matching (one resume vs multiple jobs)
3. API usage guide

## 🎯 Use Cases

1. **Recruitment Agencies**: Quickly match candidates with client job openings
2. **HR Departments**: Screen applications efficiently and reduce time-to-hire
3. **Job Platforms**: Provide intelligent job recommendations to users
4. **Freelance Platforms**: Match freelancers with project requirements
5. **Career Counseling**: Help job seekers identify skill gaps

## 🔒 Security Considerations

- File uploads are sanitized using `secure_filename`
- Maximum file size limits prevent abuse
- Files are deleted after processing
- No permanent storage of sensitive candidate data
- Input validation on all API endpoints

## 🚀 Performance

- Processes resume in < 2 seconds
- Matching computation in < 1 second
- Supports concurrent requests via Flask
- Scalable with gunicorn for production

## 🛠️ Deployment

### Production Deployment with Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t resume-matcher .
docker run -p 5000:5000 resume-matcher
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Sentence Transformers for NLP models
- Flask for web framework
- scikit-learn for machine learning utilities
- PyPDF2 and python-docx for document parsing

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using Python, Flask, and AI**
