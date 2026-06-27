import re


def analyze_job_description(job_description):
    text = job_description.lower()
    categories = {
        'required_skills': [],
        'preferred_skills': [],
        'programming_languages': [],
        'frameworks': [],
        'cloud_platforms': [],
        'databases': [],
        'developer_tools': [],
        'soft_skills': [],
        'certifications': [],
        'years_of_experience': '',
        'education_requirements': [],
        'industry_keywords': [],
        'responsibilities': []
    }

    skill_terms = {
        'required_skills': ['python', 'java', 'javascript', 'react', 'sql', 'docker', 'aws', 'kubernetes', 'django', 'flask', 'rest api', 'api', 'postgresql', 'mongodb', 'machine learning', 'deep learning', 'data science', 'backend', 'frontend', 'linux', 'git', 'redis', 'spark', 'pytorch', 'tensorflow'],
        'frameworks': ['django', 'flask', 'react', 'fastapi', 'spring', 'express', 'vue', 'node.js', 'pytorch', 'tensorflow'],
        'cloud_platforms': ['aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes'],
        'databases': ['postgresql', 'mysql', 'mongodb', 'redis', 'sqlite', 'oracle'],
        'developer_tools': ['git', 'jira', 'jenkins', 'docker', 'linux', 'kubernetes'],
        'soft_skills': ['leadership', 'communication', 'collaboration', 'problem solving', 'ownership', 'teamwork']
    }

    for category, terms in skill_terms.items():
        for term in terms:
            if term in text:
                categories[category].append(term)

    if 'bachelor' in text or 'bs' in text or 'bsc' in text:
        categories['education_requirements'].append('Bachelor\'s degree')
    if 'master' in text:
        categories['education_requirements'].append('Master\'s degree')

    years_match = re.search(r'(\d+)[+\s-]*years?', text)
    if years_match:
        categories['years_of_experience'] = years_match.group(1)

    responsibilities = re.split(r'\.|;|\n', job_description)
    categories['responsibilities'] = [resp.strip() for resp in responsibilities if len(resp.strip()) > 8][:8]

    categories['programming_languages'] = [item for item in categories['required_skills'] if item in {'python', 'java', 'javascript', 'c++', 'c#'}]
    categories['required_skills'] = list(dict.fromkeys(categories['required_skills']))

    return categories
