import google.generativeai as genai

def classify_experience(resume_text, gemini_key):
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"Classify this resume as Entry-level, Mid-level, or Senior-level:\n\n{resume_text}"
    response = model.generate_content(prompt)
    return response.text.strip()
