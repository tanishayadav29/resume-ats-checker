import re

CORE_SECTION_KEYWORDS = {
    "Education": ["education", "degree", "university", "college", "gpa", "school", "academic"],
    "Skills": ["skills", "technologies", "languages", "tools", "expertise", "stack", "proficiencies"],
    "Experience": ["experience", "employment", "work history", "professional", "career"],
    "Projects": ["projects", "personal projects", "academic projects", "portfolio"],
    "Certifications": ["certifications", "certs", "licenses", "certified", "certificate"]
}

ACTION_VERBS = [
    "architected", "optimized", "engineered", "implemented", "designed", "delivered", "led", "automated",
    "streamlined", "improved", "boosted", "accelerated", "launched", "orchestrated"
]

DATE_PATTERNS = [
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\b",
    r"\b\d{2}\/\d{4}\b",
    r"\b\d{4}\s*[-–—]\s*(?:Present|present|\d{4})\b",
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}\s*[-–—]\s*(?:Present|present|\d{4})\b"
]

METRIC_PATTERNS = [
    r"\b\d[\d,]*(?:\.\d+)?%\b",
    r"\$\s?\d[\d,]*(?:\.\d+)?\b",
    r"\b\d[\d,]*(?:\.\d+)?[xX]\b",
    r"\b\d[\d,]*(?:\.\d+)?\s+(?:k|m|million|billion)\b"
]

CONTACT_PATTERNS = {
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "phone": r"(?:\+\d{1,2}[\s-])?(?:\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4})",
    "linkedin": r"https?://(?:www\.)?linkedin\.com/in/[A-Za-z0-9_-]+",
    "github": r"https?://(?:www\.)?github\.com/[A-Za-z0-9_-]+"
}

KEYWORDS_WEIGHT = 12.5
SECTIONS_WEIGHT = 12.5
CONTACT_WEIGHT = 12.5
LAYOUT_WEIGHT = 12.5
PAGINATION_WEIGHT = 12.5
DATES_WEIGHT = 12.5
ACTIONS_WEIGHT = 12.5
METRICS_WEIGHT = 12.5


def _normalize_text(text):
    return re.sub(r"\s+", " ", text.strip().lower())


def detect_core_sections(text):
    normalized = _normalize_text(text)
    presence = {}
    found_count = 0

    for section, keywords in CORE_SECTION_KEYWORDS.items():
        found = any(re.search(r"\b" + re.escape(keyword) + r"\b", normalized) for keyword in keywords)
        presence[section] = found
        if found:
            found_count += 1

    section_score = round((found_count / len(CORE_SECTION_KEYWORDS)) * SECTIONS_WEIGHT, 2)
    return presence, section_score


def validate_contact_info(text):
    normalized = _normalize_text(text)
    contact_matches = {}
    valid_count = 0

    for field, pattern in CONTACT_PATTERNS.items():
        match = bool(re.search(pattern, normalized))
        contact_matches[field] = match
        if match:
            valid_count += 1

    contact_score = round((valid_count / len(CONTACT_PATTERNS)) * CONTACT_WEIGHT, 2)
    contact_matches["all_valid"] = valid_count == len(CONTACT_PATTERNS)
    return contact_score, contact_matches


def analyze_layout_blocks(text):
    blocks = [block.strip() for block in re.split(r"\n{2,}", text) if block.strip()]
    word_counts = [len(re.findall(r"\w+", block)) for block in blocks]
    if not blocks:
        return 0.0, {"blocks": 0, "overlong_blocks": 0, "overlong_ratio": 1.0}

    overlong_blocks = sum(1 for count in word_counts if count > 50)
    overlong_ratio = overlong_blocks / len(blocks)
    layout_score = round(max(0.0, (1.0 - overlong_ratio)) * LAYOUT_WEIGHT, 2)

    return layout_score, {
        "blocks": len(blocks),
        "overlong_blocks": overlong_blocks,
        "overlong_ratio": round(overlong_ratio, 2)
    }


def evaluate_pagination(text):
    word_count = len(re.findall(r"\w+", text))
    line_count = len([line for line in text.splitlines() if line.strip()])

    word_penalty = 0.0 if word_count <= 750 else min(1.0, (word_count - 750) / 500)
    line_penalty = 0.0 if line_count <= 65 else min(1.0, (line_count - 65) / 35)
    compliance_ratio = max(0.0, 1.0 - ((word_penalty + line_penalty) / 2))
    pagination_score = round(compliance_ratio * PAGINATION_WEIGHT, 2)

    return pagination_score, {
        "word_count": word_count,
        "line_count": line_count,
        "page_compliant": word_count <= 750 and line_count <= 65,
        "word_penalty": round(word_penalty, 2),
        "line_penalty": round(line_penalty, 2)
    }


def evaluate_dates(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    candidate_lines = [line for line in lines if re.search(r"\d{4}", line)]
    valid_lines = [line for line in candidate_lines if any(re.search(pattern, line) for pattern in DATE_PATTERNS)]

    if not candidate_lines:
        return 0.0, {
            "candidate_lines": 0,
            "valid_lines": 0,
            "timeline_compliant": False,
            "sample_invalid_lines": []
        }

    valid_ratio = len(valid_lines) / len(candidate_lines)
    date_score = round(min(1.0, valid_ratio) * DATES_WEIGHT, 2)
    sample_invalid = [line for line in candidate_lines if line not in valid_lines][:3]

    return date_score, {
        "candidate_lines": len(candidate_lines),
        "valid_lines": len(valid_lines),
        "timeline_compliant": valid_ratio >= 0.8,
        "sample_invalid_lines": sample_invalid
    }


def count_action_verbs(text):
    normalized = _normalize_text(text)
    verb_count = sum(len(re.findall(r"\b" + re.escape(verb) + r"\b", normalized)) for verb in ACTION_VERBS)
    action_score = round(min(1.0, verb_count / 8) * ACTIONS_WEIGHT, 2)

    return action_score, {
        "verb_count": verb_count,
        "has_action_verbs": verb_count >= 4,
        "top_verbs": [verb for verb in ACTION_VERBS if re.search(r"\b" + re.escape(verb) + r"\b", normalized)]
    }


def count_metric_occurrences(text):
    normalized = text
    hits = []
    for pattern in METRIC_PATTERNS:
        hits.extend(re.findall(pattern, normalized))

    deduped = len(hits)
    metric_score = round(min(1.0, deduped / 5) * METRICS_WEIGHT, 2)

    return metric_score, {
        "metric_count": deduped,
        "has_enough_metrics": deduped >= 3,
        "sample_metrics": hits[:5]
    }


def calculate_ats_score(resume_text, keyword_score):
    section_presence, section_score = detect_core_sections(resume_text)
    contact_score, contact_validation = validate_contact_info(resume_text)
    layout_score, layout_details = analyze_layout_blocks(resume_text)
    pagination_score, pagination_details = evaluate_pagination(resume_text)
    dates_score, date_details = evaluate_dates(resume_text)
    action_score, action_details = count_action_verbs(resume_text)
    metric_score, metric_details = count_metric_occurrences(resume_text)

    breakdown = {
        "Keywords": round(keyword_score, 2),
        "Sections": section_score,
        "Contact": contact_score,
        "Layout": layout_score,
        "Pagination": pagination_score,
        "Dates": dates_score,
        "Actions": action_score,
        "Metrics": metric_score
    }

    overall_score = round(sum(breakdown.values()), 2)

    return {
        "score": overall_score,
        "breakdown": breakdown,
        "section_presence": section_presence,
        "validation": {
            "contact": contact_validation,
            "layout": layout_details,
            "pagination": pagination_details,
            "dates": date_details,
            "actions": action_details,
            "metrics": metric_details
        }
    }
