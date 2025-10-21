import re

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group() if match else None

def extract_keywords_from_jd(jd_text):
    stopwords = {"developer", "engineer", "experience", "with", "and", "role", "required", "for", "in"}
    words = re.findall(r'\b\w+\b', jd_text.lower())
    return [w for w in words if w not in stopwords and len(w) > 3]
