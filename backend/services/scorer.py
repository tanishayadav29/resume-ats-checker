import re

def calculate_ats_score(resume_text, keyword_score, sections_score):
    resume_lower = resume_text.lower()
    
    # 1. Formatting Assessment (15 Points Max)
    formatting_score = 15
    paragraphs = [p for p in resume_text.split('\n') if p.strip()]
    long_paragraphs = [p for p in paragraphs if len(p.split()) > 60]
    
    if len(long_paragraphs) > 2:
        formatting_score -= 5
    if len(resume_text) < 300:
        formatting_score -= 5

    # 2. Experience Metrics Content (15 Points Max)
    # Checks for performance statistics/KPI counts
    has_metrics = len(re.findall(r'\b\d+[\d,%%+]*\b', resume_lower)) > 3
    experience_score = 15 if has_metrics else 7

    # 3. Dynamic Action Verbs / Grammar (15 Points Max)
    action_verbs = ['managed', 'developed', 'led', 'designed', 'implemented', 'optimized', 'engineered', 'built', 'increased', 'created']
    has_action_verbs = any(verb in resume_lower for verb in action_verbs)
    grammar_score = 15 if has_action_verbs else 8

    # Aggregated Weight Matrix Composition
    total_score = round(keyword_score + sections_score + formatting_score + experience_score + grammar_score)
    total_score = max(0, min(total_score, 100))

    return {
        "score": total_score,
        "breakdown": {
            "keywords": round(keyword_score),
            "sections": round(sections_score),
            "formatting": formatting_score,
            "experience": experience_score,
            "grammar": grammar_score
        },
        "has_metrics": has_metrics,
        "has_action_verbs": has_action_verbs
    }