import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Service Layer Modular Routing Imports
from services.parser import extract_text
from services.keyword_matcher import match_keywords
from services.scorer import calculate_ats_score
from services.suggestions import generate_suggestions

app = Flask(__name__)
CORS(app)  # Enables clean connection to your React server

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def detect_sections(text):
    sections = {
        "Education": ["education", "degree", "university", "college", "gpa"],
        "Skills": ["skills", "technologies", "languages", "tools", "expertise"],
        "Experience": ["experience", "employment", "work history", "history", "professional"],
        "Projects": ["projects", "personal projects", "academic projects"],
        "Certifications": ["certifications", "certs", "licenses", "certified"]
    }
    
    detected = {}
    score = 0
    text_lower = text.lower()
    
    for section, keywords in sections.items():
        found = any(re.search(r'\b' + re.escape(kw) + r'\b', text_lower) for kw in keywords)
        detected[section] = found
        if found:
            score += (20 / len(sections)) # 4 points per valid core section bloc
            
    return detected, score

@app.route('/api/analyze', methods=['POST'])
def analyze_resume_endpoint():
    if 'file' not in request.files:
        return jsonify({"error": "No file artifact uploaded"}), 400
        
    file = request.files['file']
    job_description = request.form.get('job_description', '')

    if file.filename == '':
        return jsonify({"error": "Selected empty file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # 1. Parse File Content
    resume_text = extract_text(filepath)
    os.remove(filepath)  # Clean storage space footprint instantly
    
    if not resume_text.strip():
        return jsonify({"error": "Could not parse readable text from document structure"}), 400

    # 2. Run Engine Processing Subsections
    detected_sections, sections_score = detect_sections(resume_text)
    keyword_score, keyword_heatmap, missing_keywords = match_keywords(resume_text, job_description)
    
    # 3. Aggregate Final Scoring Objects
    score_data = calculate_ats_score(resume_text, keyword_score, sections_score)
    
    # 4. Generate Strategic Optimization Logs
    suggestions = generate_suggestions(
        detected_sections, 
        score_data["has_metrics"], 
        score_data["has_action_verbs"], 
        missing_keywords
    )

    return jsonify({
        "score": score_data["score"],
        "breakdown": score_data["breakdown"],
        "sections": detected_sections,
        "keyword_heatmap": keyword_heatmap,
        "suggestions": suggestions
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(port=port, debug=True)