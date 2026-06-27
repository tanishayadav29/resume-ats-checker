def build_resume_insights(profile, job_analysis, score_data, keyword_matches, missing_keywords):
    skills_gap = []
    for skill in missing_keywords[:5]:
        skills_gap.append({
            'skill': skill,
            'importance': 'High',
            'why': f'{skill} is explicitly referenced in the target role and would strengthen ATS alignment.',
            'where': 'Job description requirements',
            'priority': 'High'
        })

    ai_coach = []
    if not profile.get('projects'):
        ai_coach.append('Add a dedicated Projects section with problem-solving details and outcomes.')
    if not profile.get('experience'):
        ai_coach.append('Highlight internships, research, leadership, or hackathon work to balance limited professional experience.')
    if score_data.get('validation', {}).get('metrics', {}).get('has_enough_metrics', False) is False:
        ai_coach.append('Add quantifiable impact using percentages, user growth, latency reduction, or cost savings.')

    return {
        'skills_gap': skills_gap,
        'ai_coach': ai_coach,
        'keyword_matches': keyword_matches,
        'missing_keywords': missing_keywords,
        'overall_score': score_data.get('score', 0),
        'section_scores': score_data.get('breakdown', {})
    }
