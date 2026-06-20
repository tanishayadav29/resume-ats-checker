def generate_suggestions(detected_sections, has_metrics, has_action_verbs, missing_keywords):
    suggestions = []
    
    if not has_metrics:
        suggestions.append("Quantify your achievements: Add measurable metrics and business KPIs (e.g., 'Optimized query speeds by 30%').")
        
    if not has_action_verbs:
        suggestions.append("Incorporate powerful action verbs at the beginning of bullet points (e.g., 'Engineered', 'Architected', 'Optimized').")
        
    if missing_keywords:
        suggestions.append(f"Incorporate missing core skill keywords from target JD: {', '.join(missing_keywords[:4])}")
        
    if not detected_sections.get("Certifications"):
        suggestions.append("Consider adding a standalone 'Certifications' section to fulfill automated baseline compliance screening pipelines.")
        
    return suggestions
