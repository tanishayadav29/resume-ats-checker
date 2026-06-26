import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def _normalize_text(text):
    return re.sub(r"\s+", " ", text.strip().lower())


def _extract_target_tokens(text):
    doc = nlp(text)
    tokens = []
    for token in doc:
        if token.pos_ in {"NOUN", "PROPN"} and not token.is_stop and not token.is_punct and len(token.lemma_) > 2:
            lemma = token.lemma_.lower()
            if lemma not in tokens:
                tokens.append(lemma)
    return tokens


def match_keywords(resume_text, job_desc):
    normalized_resume = _normalize_text(resume_text)
    normalized_jd = _normalize_text(job_desc)

    if not normalized_jd:
        return 0.0, {}, []

    target_tokens = _extract_target_tokens(normalized_jd)
    top_keywords = target_tokens[:12]

    keyword_heatmap = {}
    missing_keywords = []
    matched_keywords = 0

    for keyword in top_keywords:
        count = len(re.findall(r"\b" + re.escape(keyword) + r"\b", normalized_resume))
        match_percent = min(100, int((count / 2) * 100)) if count > 0 else 0
        if count > 0:
            matched_keywords += 1
        else:
            missing_keywords.append(keyword)
        keyword_heatmap[keyword] = match_percent

    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([normalized_resume, normalized_jd])
        similarity = float(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0])
        keyword_score = round(similarity * 12.5, 2)
    except Exception:
        keyword_score = round((matched_keywords / len(top_keywords)) * 12.5, 2) if top_keywords else 0.0

    if not top_keywords and normalized_jd:
        keyword_heatmap["No extracted keywords"] = 0

    return keyword_score, keyword_heatmap, missing_keywords
