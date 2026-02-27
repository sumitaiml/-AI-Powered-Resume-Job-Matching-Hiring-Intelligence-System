"""
Flask Web Application for Resume-Job Matching System
"""
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import traceback

from config import Config
from resume_parser import ResumeParser
from job_analyzer import JobAnalyzer
from matching_engine import MatchingEngine

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)
CORS(app)

# Initialize components
resume_parser = ResumeParser()
job_analyzer = JobAnalyzer()
matching_engine = MatchingEngine(Config.SENTENCE_TRANSFORMER_MODEL)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Resume-Job Matching System'
    })


@app.route('/api/parse-resume', methods=['POST'])
def parse_resume():
    """Parse resume file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Parse resume
        file_type = filename.rsplit('.', 1)[1].lower()
        resume_data = resume_parser.parse_resume(filepath, file_type)
        
        # Clean up
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'data': resume_data
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/analyze-job', methods=['POST'])
def analyze_job():
    """Analyze job description"""
    try:
        data = request.get_json()
        if not data or 'job_description' not in data:
            return jsonify({'error': 'No job description provided'}), 400
        
        job_description = data['job_description']
        job_data = job_analyzer.analyze_job(job_description)
        
        return jsonify({
            'success': True,
            'data': job_data
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/match', methods=['POST'])
def match_resume_job():
    """Match resume with job description"""
    try:
        # Check if file upload or JSON data
        if 'file' in request.files:
            # File upload mode
            file = request.files['file']
            job_description = request.form.get('job_description', '')
            
            if not job_description:
                return jsonify({'error': 'Job description required'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'Invalid file type'}), 400
            
            # Save and parse resume
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            file_type = filename.rsplit('.', 1)[1].lower()
            resume_data = resume_parser.parse_resume(filepath, file_type)
            
            # Clean up
            os.remove(filepath)
            
        else:
            # JSON mode
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            resume_data = data.get('resume_data')
            job_description = data.get('job_description')
            
            if not resume_data or not job_description:
                return jsonify({'error': 'Both resume_data and job_description required'}), 400
        
        # Analyze job
        job_data = job_analyzer.analyze_job(job_description)
        
        # Perform matching
        match_result = matching_engine.match_resume_to_job(resume_data, job_data)
        
        return jsonify({
            'success': True,
            'resume': resume_data,
            'job': job_data,
            'match': match_result
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/batch-match', methods=['POST'])
def batch_match():
    """Match one resume against multiple job descriptions"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        resume_data = data.get('resume_data')
        job_descriptions = data.get('job_descriptions', [])
        
        if not resume_data or not job_descriptions:
            return jsonify({'error': 'Both resume_data and job_descriptions required'}), 400
        
        # Analyze all jobs
        jobs_data = [job_analyzer.analyze_job(jd) for jd in job_descriptions]
        
        # Perform batch matching
        matches = matching_engine.batch_match(resume_data, jobs_data)
        
        return jsonify({
            'success': True,
            'resume': resume_data,
            'matches': matches
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


# HTML Template for the web interface
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI-Powered Resume-Job Matching System</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 40px;
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
            font-size: 1.1em;
        }
        .section {
            margin-bottom: 30px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        .section h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }
        input[type="file"] {
            display: block;
            width: 100%;
            padding: 12px;
            border: 2px dashed #667eea;
            border-radius: 8px;
            background: white;
            cursor: pointer;
        }
        textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-family: inherit;
            font-size: 14px;
            resize: vertical;
            min-height: 150px;
        }
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
            width: 100%;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .results {
            margin-top: 30px;
            padding: 25px;
            background: white;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
            display: none;
        }
        .results.show {
            display: block;
        }
        .score-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 25px;
        }
        .score-value {
            font-size: 4em;
            font-weight: bold;
            margin: 10px 0;
        }
        .score-category {
            font-size: 1.5em;
            margin-top: 10px;
        }
        .metric {
            display: flex;
            justify-content: space-between;
            padding: 12px;
            margin-bottom: 10px;
            background: #f8f9fa;
            border-radius: 6px;
        }
        .metric-label {
            font-weight: 600;
            color: #333;
        }
        .metric-value {
            color: #667eea;
            font-weight: bold;
        }
        .skills-list {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 10px;
        }
        .skill-tag {
            background: #667eea;
            color: white;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 14px;
        }
        .skill-tag.missing {
            background: #dc3545;
        }
        .recommendation {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin-top: 20px;
            border-radius: 6px;
        }
        .loading {
            text-align: center;
            padding: 20px;
            display: none;
        }
        .loading.show {
            display: block;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .error {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 6px;
            margin-top: 15px;
            display: none;
        }
        .error.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AI-Powered Resume Matching</h1>
        <p class="subtitle">Intelligent Resume-Job Matching & Hiring Intelligence System</p>
        
        <div class="section">
            <h2>📄 Upload Resume</h2>
            <div class="form-group">
                <label for="resumeFile">Select Resume (PDF, DOCX, TXT)</label>
                <input type="file" id="resumeFile" accept=".pdf,.docx,.doc,.txt">
            </div>
        </div>
        
        <div class="section">
            <h2>💼 Job Description</h2>
            <div class="form-group">
                <label for="jobDescription">Paste Job Description</label>
                <textarea id="jobDescription" placeholder="Enter the job description here..."></textarea>
            </div>
        </div>
        
        <button id="matchButton" onclick="performMatching()">
            🔍 Analyze & Match
        </button>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p style="margin-top: 15px;">Analyzing resume and matching with job description...</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="results" id="results">
            <h2 style="margin-bottom: 20px;">📊 Matching Results</h2>
            
            <div class="score-card">
                <div>Overall Match Score</div>
                <div class="score-value" id="overallScore">-</div>
                <div class="score-category" id="matchCategory">-</div>
            </div>
            
            <div class="metric">
                <span class="metric-label">Semantic Similarity</span>
                <span class="metric-value" id="semanticScore">-</span>
            </div>
            <div class="metric">
                <span class="metric-label">Skills Match</span>
                <span class="metric-value" id="skillsScore">-</span>
            </div>
            <div class="metric">
                <span class="metric-label">Required Skills Match</span>
                <span class="metric-value" id="requiredSkillsScore">-</span>
            </div>
            
            <div style="margin-top: 25px;">
                <h3 style="color: #333; margin-bottom: 10px;">✅ Matching Skills</h3>
                <div class="skills-list" id="matchingSkills"></div>
            </div>
            
            <div style="margin-top: 25px;">
                <h3 style="color: #333; margin-bottom: 10px;">❌ Missing Required Skills</h3>
                <div class="skills-list" id="missingSkills"></div>
            </div>
            
            <div class="recommendation">
                <strong>💡 Recommendation:</strong>
                <p id="recommendation" style="margin-top: 10px;"></p>
            </div>
        </div>
    </div>
    
    <script>
        async function performMatching() {
            const fileInput = document.getElementById('resumeFile');
            const jobDescription = document.getElementById('jobDescription').value;
            const button = document.getElementById('matchButton');
            const loading = document.getElementById('loading');
            const results = document.getElementById('results');
            const error = document.getElementById('error');
            
            // Validation
            if (!fileInput.files[0]) {
                showError('Please select a resume file');
                return;
            }
            if (!jobDescription.trim()) {
                showError('Please enter a job description');
                return;
            }
            
            // Show loading
            button.disabled = true;
            loading.classList.add('show');
            results.classList.remove('show');
            error.classList.remove('show');
            
            try {
                // Prepare form data
                const formData = new FormData();
                formData.append('file', fileInput.files[0]);
                formData.append('job_description', jobDescription);
                
                // Make API call
                const response = await fetch('/api/match', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Matching failed');
                }
                
                // Display results
                displayResults(data);
                results.classList.add('show');
                
            } catch (err) {
                showError(err.message);
            } finally {
                button.disabled = false;
                loading.classList.remove('show');
            }
        }
        
        function displayResults(data) {
            const match = data.match;
            
            // Overall score
            document.getElementById('overallScore').textContent = 
                (match.overall_score * 100).toFixed(1) + '%';
            document.getElementById('matchCategory').textContent = match.match_category;
            
            // Metrics
            document.getElementById('semanticScore').textContent = 
                (match.semantic_similarity * 100).toFixed(1) + '%';
            document.getElementById('skillsScore').textContent = 
                (match.skills_match * 100).toFixed(1) + '%';
            document.getElementById('requiredSkillsScore').textContent = 
                (match.required_skills_match * 100).toFixed(1) + '%';
            
            // Matching skills
            const matchingSkillsDiv = document.getElementById('matchingSkills');
            matchingSkillsDiv.innerHTML = '';
            if (match.matching_skills && match.matching_skills.length > 0) {
                match.matching_skills.forEach(skill => {
                    const tag = document.createElement('span');
                    tag.className = 'skill-tag';
                    tag.textContent = skill;
                    matchingSkillsDiv.appendChild(tag);
                });
            } else {
                matchingSkillsDiv.innerHTML = '<p style="color: #666;">No matching skills found</p>';
            }
            
            // Missing skills
            const missingSkillsDiv = document.getElementById('missingSkills');
            missingSkillsDiv.innerHTML = '';
            if (match.missing_required_skills && match.missing_required_skills.length > 0) {
                match.missing_required_skills.forEach(skill => {
                    const tag = document.createElement('span');
                    tag.className = 'skill-tag missing';
                    tag.textContent = skill;
                    missingSkillsDiv.appendChild(tag);
                });
            } else {
                missingSkillsDiv.innerHTML = '<p style="color: #28a745;">All required skills present!</p>';
            }
            
            // Recommendation
            document.getElementById('recommendation').textContent = match.recommendation;
        }
        
        function showError(message) {
            const error = document.getElementById('error');
            error.textContent = message;
            error.classList.add('show');
        }
    </script>
</body>
</html>
'''


if __name__ == '__main__':
    # Use debug=True only for development
    # For production, use: gunicorn -w 4 -b 0.0.0.0:5000 app:app
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
