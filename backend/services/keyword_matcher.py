import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def match_keywords(resume_text, job_desc):
    if not job_desc.strip():
        return 25, {"Add a Job Description to view itemized keyword matching": 0}, []

    resume_lower = resume_text.lower()
    jd_doc = nlp(job_desc.lower())
    
    # Extract structural keywords (Nouns & Proper Nouns) from Job Description
    target_keywords = []
    for token in jd_doc:
        if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2 and not token.is_stop and not token.is_punct:
            keyword = token.text.strip()
            if keyword and keyword not in target_keywords:
                target_keywords.append(keyword)
    
    # Limit to top 12 keywords for display cleanliness
    target_keywords = target_keywords[:12]

    keyword_heatmap = {}
    missing_keywords = []
    matched_count = 0

    for kw in target_keywords:
        # Check occurrences using explicit boundary flags
        count = len(re.findall(r'\b' + re.escape(kw) + r'\b', resume_lower))
        # Scaled density percentage logic (2+ mentions = 100% matched bar display)
        match_percentage = min(count * 50, 100)
        keyword_heatmap[kw] = match_percentage
        
        if count > 0:
            matched_count += 1
        else:
            missing_keywords.append(kw)

    # Use TF-IDF Cosine Similarity for the official NLP score component weight
    try:
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform([resume_lower, job_desc.lower()])
        similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        keyword_score = round(similarity * 35)
    except Exception:
        keyword_score = round((matched_count / len(target_keywords)) * 35) if target_keywords else 35

    return keyword_score, keyword_heatmap, missing_keywords