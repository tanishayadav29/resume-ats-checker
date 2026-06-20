# 1. Create and activate a virtual environment

# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# 2. Install the Core Backend Framework & Utilities
pip install Flask flask-cors werkzeug

# 3. Install Document Parsers
pip install pypdf python-docx

# 4. Install NLP and Data Science Libraries
pip install spacy scikit-learn

# 5. Download the English NLP Model for spaCy (CRITICAL STEP)
python -m spacy download en_core_web_sm