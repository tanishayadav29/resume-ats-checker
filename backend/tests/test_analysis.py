import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.parser import extract_resume_profile
from services.jd_analyzer import analyze_job_description
from services.insights import build_resume_insights
from services.scorer import calculate_ats_score


class AnalysisPipelineTests(unittest.TestCase):
    def test_extract_resume_profile_detects_common_fields(self):
        text = """
        Jane Doe
        jane@example.com
        +1 555 123 4567
        github.com/janedoe
        linkedin.com/in/janedoe
        Education
        B.S. Computer Science, University of Example, 2024
        Skills
        Python, SQL, React
        Projects
        Built a dashboard for analytics.
        Experience
        Software Engineer Intern, Example Corp, Jan 2024 - Present
        """
        profile = extract_resume_profile(text)
        self.assertEqual(profile['name'], 'Jane Doe')
        self.assertIn('jane@example.com', profile['email'])
        self.assertGreaterEqual(len(profile['skills']), 3)

    def test_job_description_analysis_extracts_categories(self):
        jd = """
        We are hiring a Python Backend Engineer with Django, PostgreSQL, Docker, AWS, and leadership experience.
        Required: Python, Django, REST APIs, PostgreSQL, Docker, AWS.
        """
        analysis = analyze_job_description(jd)
        self.assertIn('python', analysis['required_skills'])
        self.assertIn('docker', analysis['required_skills'])
        self.assertIn('aws', analysis['required_skills'])

    def test_calculate_ats_score_uses_weighted_recruiter_focused_breakdown(self):
        resume_text = """
        Jane Doe
        Software Engineer
        Education
        B.S. Computer Science, University of Example, 2024
        Skills
        Python, SQL, React, Docker, AWS
        Projects
        Built a dashboard that improved analytics workflows and reduced report time by 40%.
        Experience
        Software Engineer Intern, Example Corp, Jan 2024 - Present
        """
        result = calculate_ats_score(resume_text, 10.0, job_description='Python backend engineer with Django and AWS')
        self.assertIn('Keyword Match', result['breakdown'])
        self.assertIn('Skills Match', result['breakdown'])
        self.assertIn('Projects Relevance', result['breakdown'])
        self.assertIn('Impact & Quantification', result['breakdown'])
        self.assertIn('Grade', result)
        self.assertGreaterEqual(result['score'], 0)

    def test_build_resume_insights_generates_gap_and_coach_feedback(self):
        profile = {
            'name': 'Jane Doe',
            'skills': ['python', 'sql', 'react'],
            'projects': ['Built a dashboard'],
            'experience': [],
            'education': ['B.S. Computer Science'],
            'links': {'github': 'https://github.com/janedoe'}
        }
        job_analysis = {
            'required_skills': ['python', 'django', 'docker', 'aws'],
            'preferred_skills': ['kubernetes'],
            'soft_skills': ['leadership']
        }
        score_data = {
            'breakdown': {'Keywords': 9.0, 'Sections': 10.0, 'Contact': 10.0, 'Layout': 10.0, 'Pagination': 10.0, 'Dates': 8.0, 'Actions': 7.0, 'Metrics': 6.0},
            'score': 70.0,
            'validation': {'contact': {'all_valid': True}, 'pagination': {'page_compliant': True}, 'dates': {'timeline_compliant': True}, 'metrics': {'has_enough_metrics': False}, 'actions': {'has_action_verbs': True}}
        }
        insights = build_resume_insights(profile, job_analysis, score_data, {'python': 90}, ['django', 'docker', 'aws'])
        self.assertIn('skills_gap', insights)
        self.assertGreaterEqual(len(insights['skills_gap']), 1)
        self.assertIn('ai_coach', insights)
        self.assertGreaterEqual(len(insights['ai_coach']), 1)


if __name__ == '__main__':
    unittest.main()
