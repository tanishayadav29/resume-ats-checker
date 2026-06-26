import math

CATEGORY_SEVERITY = {
    'Keywords': 'High',
    'Sections': 'High',
    'Contact': 'Critical',
    'Layout': 'Medium',
    'Pagination': 'High',
    'Dates': 'High',
    'Actions': 'Medium',
    'Metrics': 'High'
}

ACTION_VERBS_GUIDANCE = (
    "Open bullet lines with measurable operational verbs such as 'Architected', 'Optimized', 'Engineered', "
    "'Implemented', 'Automated', 'Led', or 'Built'. Start each result statement with a verb, then add a metric or business outcome."
)

METRIC_GUIDANCE = (
    "Convert vague outputs into quantified achievement statements. Use a guiding formula: "
    "Verb + Metric + Result + Context. For example, 'Optimized ETL pipelines by 35% to reduce data latency by 12 hours in a cross-functional team.'"
)

DATE_GUIDANCE = (
    "Use clear enterprise timeline formatting such as 'MM/YYYY - Present', 'MMM YYYY - MMM YYYY', or "
    "'YYYY - Present' for each role. Ensure date ranges are consistent and listed in descending chronology."
)

CONTACT_GUIDANCE = (
    "Provide a professional header with an email, a U.S. or international phone number, a LinkedIn URL, and a GitHub profile link. "
    "Use exact formats like 'https://www.linkedin.com/in/yourname' and 'https://github.com/yourname'."
)

LAYOUT_GUIDANCE = (
    "Break dense text into shorter bullet groups. Keep each paragraph or bullet block under 50 words. Use whitespace and headings to separate job summaries, achievement bullets, and skills."
)

PAGINATION_GUIDANCE = (
    "Keep your resume under 750 words and 65 non-empty lines for strong single-page ATS compliance. If the file is longer, reduce redundant descriptions and consolidate repeated responsibilities."
)

SECTION_GUIDANCE = {
    'Education': "Add a dedicated Education section with degree, institution, location, and graduation date.",
    'Skills': "Add a concise Skills section listing technical proficiencies, tools, languages, and platforms.",
    'Experience': "Ensure one clear Experience section with company, title, location, and dates for each role.",
    'Projects': "Include a Projects section with at least one measurable, outcome-driven project and technology summary.",
    'Certifications': "Add Certifications or Licenses if you have formal credentials such as AWS, PMP, or Certified Scrum Master."
}


def _severity_from_value(category, value):
    if category == 'Contact':
        return 'Critical' if value < 12.5 else 'High'
    if category == 'Keywords':
        return 'High' if value < 6.5 else 'Medium'
    if category == 'Sections':
        return 'High' if value < 6.5 else 'Medium'
    if category == 'Pagination':
        return 'High' if value < 8.5 else 'Medium'
    if category == 'Dates':
        return 'High' if value < 8.5 else 'Medium'
    if category == 'Metrics':
        return 'High' if value < 8.5 else 'Medium'
    return 'Medium'


def _build_suggestion(category, impact, issue, fix):
    return {
        'category': category,
        'impact': impact,
        'issue': issue,
        'fix': fix
    }


def generate_detailed_suggestions(score_data, missing_keywords):
    breakdown = score_data.get('breakdown', {})
    validation = score_data.get('validation', {})
    suggestions = []

    if breakdown.get('Keywords', 0) < 10 or missing_keywords:
        impact = _severity_from_value('Keywords', breakdown.get('Keywords', 0))
        issue = (
            "The resume does not sufficiently match the job description keyword set. "
            "Target keywords extracted from the JD are either missing or too lightly represented."
        )
        keyword_list = ', '.join(missing_keywords[:6]) if missing_keywords else 'key domain terms'
        fix = (
            f"Insert the most relevant JD terms in your summary and experience bullets. Make sure the resume includes: {keyword_list}. "
            "Use the same terminology as the job description and repeat high-value keywords at least twice across your achievements."
        )
        suggestions.append(_build_suggestion('Keywords', impact, issue, fix))

    section_presence = score_data.get('section_presence', {})
    missing_sections = [name for name, present in section_presence.items() if not present]
    if missing_sections:
        impact = _severity_from_value('Sections', 0)
        issue = (
            "Core structural sections are incomplete. A strong resume should include Education, Skills, Experience, Projects, and Certifications."
        )
        fix = (
            "Add any missing sections from the following list with clear headers: "
            f"{', '.join(missing_sections)}. For each section, include concise bullet points, a timeline, and measurable outcomes."
        )
        suggestions.append(_build_suggestion('Sections', impact, issue, fix))

    contact = validation.get('contact', {})
    if not contact.get('all_valid', False):
        impact = _severity_from_value('Contact', breakdown.get('Contact', 0))
        missing = [field for field, valid in contact.items() if field in {'email', 'phone', 'linkedin', 'github'} and not valid]
        issue = (
            "The resume header lacks verified contact channels required for ATS and recruiter screening. "
            f"Missing fields: {', '.join(missing)}."
        )
        fix = CONTACT_GUIDANCE
        suggestions.append(_build_suggestion('Contact', impact, issue, fix))

    layout = validation.get('layout', {})
    if layout.get('overlong_blocks', 0) > 0:
        impact = _severity_from_value('Layout', breakdown.get('Layout', 0))
        issue = (
            f"Found {layout['overlong_blocks']} text blocks longer than 50 words, which can trigger wall-of-text flags in ATS review."
        )
        fix = LAYOUT_GUIDANCE
        suggestions.append(_build_suggestion('Layout', impact, issue, fix))

    pagination = validation.get('pagination', {})
    if not pagination.get('page_compliant', False):
        impact = _severity_from_value('Pagination', breakdown.get('Pagination', 0))
        issue = (
            f"Resume length is outside ideal single-page density limits: {pagination['word_count']} words and {pagination['line_count']} non-empty lines."
        )
        fix = PAGINATION_GUIDANCE
        suggestions.append(_build_suggestion('Pagination', impact, issue, fix))

    dates = validation.get('dates', {})
    if not dates.get('timeline_compliant', True):
        impact = _severity_from_value('Dates', breakdown.get('Dates', 0))
        issue = (
            "Timeline date formatting is inconsistent or missing from experience sections. "
            f"Invalid examples: {', '.join(dates.get('sample_invalid_lines', []) or ['none'])}."
        )
        fix = DATE_GUIDANCE
        suggestions.append(_build_suggestion('Dates', impact, issue, fix))

    actions = validation.get('actions', {})
    if not actions.get('has_action_verbs', False):
        impact = _severity_from_value('Actions', breakdown.get('Actions', 0))
        issue = (
            "The resume lacks high-impact operational verbs in achievement statements, reducing its recruiter appeal."
        )
        fix = ACTION_VERBS_GUIDANCE
        suggestions.append(_build_suggestion('Actions', impact, issue, fix))

    metrics = validation.get('metrics', {})
    if not metrics.get('has_enough_metrics', False):
        impact = _severity_from_value('Metrics', breakdown.get('Metrics', 0))
        issue = (
            "There are too few measurable metrics or KPI statements across the resume. Recruiters rely on quantification."
        )
        fix = METRIC_GUIDANCE
        suggestions.append(_build_suggestion('Metrics', impact, issue, fix))

    if not suggestions:
        suggestions.append(_build_suggestion(
            'Resume Diagnostics',
            'Medium',
            'All core vectors are strong based on the current analysis.',
            'Maintain this structure, continue to mirror JD language, and keep metrics explicit and concise.'
        ))

    return suggestions
