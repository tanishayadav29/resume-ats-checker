import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from services.parser import extract_text
from services.keyword_matcher import match_keywords
from services.scorer import calculate_ats_score
from services.detailed_suggestions import generate_detailed_suggestions

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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

    keyword_score, keyword_heatmap, missing_keywords = match_keywords(resume_text, job_description)
    score_data = calculate_ats_score(resume_text, keyword_score)
    detailed_suggestions = generate_detailed_suggestions(score_data, missing_keywords)

    return jsonify({
        "score": score_data["score"],
        "breakdown": score_data["breakdown"],
        "sections": score_data["section_presence"],
        "validation": score_data["validation"],
        "keyword_heatmap": keyword_heatmap,
        "detailed_suggestions": detailed_suggestions
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(port=port, debug=True)