# app.py
import os
import tempfile
import streamlit as st
from PyPDF2 import PdfReader
from datetime import datetime, time
from sklearn.metrics.pairwise import cosine_similarity
from embedding_utils import get_cohere_embeddings
from email_utils import send_email_app_password
from gemini_utils import classify_experience
from text_utils import extract_email, extract_keywords_from_jd

from email_graph import StateGraph, END

# -----------------------------
# API Keys from Streamlit secrets
# -----------------------------
GEMINI_KEY = st.secrets["GEMINI_API_KEY"]
COHERE_KEY = st.secrets["COHERE_API_KEY"]
GMAIL_PASS = st.secrets["GMAIL_APP_PASS"]
SENDER_EMAIL = "gungunsachdevahere@gmail.com"

# -----------------------------
# Streamlit Gradient Background & Custom CSS
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom right, #ffe6f9, #e0ccff);
        color: #333333;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background: linear-gradient(to right, #ffb3ff, #800080);
        color: #333333;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5em 1em;
        border: none;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        cursor: pointer;
    }
    .stFileUploader>div, .stTextInput>div, .stTextArea>div {
        background: rgba(255, 255, 255, 0.35);
        border-radius: 10px;
        padding: 1em;
        margin-bottom: 1em;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("Recruitment Screening Tool")
uploaded_file = st.file_uploader("Upload Candidate Resume (PDF)", type=["pdf"])
job_description = st.text_area("Enter Job Description")

# -----------------------------
# Resume Processing
# -----------------------------
if uploaded_file and job_description:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        pdf_reader = PdfReader(tmp_file.name)
        resume_text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                resume_text += page_text + "\n"

    if not resume_text.strip():
        st.error("❌ Uploaded PDF is empty or text could not be extracted.")
        st.stop()

    st.info("✅ PDF loaded successfully.")

    candidate_email = extract_email(resume_text)
    if candidate_email:
        st.success(f"✅ Extracted Email: {candidate_email}")
    else:
        st.warning("⚠️ No email address found in resume.")

    # -----------------------------
    # Generate embeddings & Skill Match
    # -----------------------------
    jd_embedding = get_cohere_embeddings(job_description, COHERE_KEY)
    resume_chunks = [resume_text[i:i+500] for i in range(0, len(resume_text), 500)]
    chunk_embeddings = [get_cohere_embeddings(chunk, COHERE_KEY) for chunk in resume_chunks]

    similarity_scores = [cosine_similarity([jd_embedding], [emb])[0][0] for emb in chunk_embeddings]
    max_similarity = max(similarity_scores)
    avg_similarity = sum(similarity_scores) / len(similarity_scores)

    jd_keywords = extract_keywords_from_jd(job_description)
    resume_lower = resume_text.lower()
    matched_keywords = sum(1 for kw in jd_keywords if kw in resume_lower)
    keyword_match_ratio = matched_keywords / len(jd_keywords) if jd_keywords else 0

    experience_level = classify_experience(resume_text, GEMINI_KEY)
    st.info(f"Experience level: {experience_level}")

    # -----------------------------
    # Skill Match Logic
    # -----------------------------
    if max_similarity >= 0.5:
        skill_match = "Match"
    elif max_similarity >= 0.35 and keyword_match_ratio >= 0.6:
        skill_match = "Match"
    elif "Senior" in experience_level and (max_similarity >= 0.3 or keyword_match_ratio >= 0.5):
        skill_match = "Match"
    else:
        skill_match = "No Match"

    st.info(f"Skill match: {skill_match} "
            f"(Max similarity: {round(max_similarity*100,2)}%, "
            f"Avg similarity: {round(avg_similarity*100,2)}%, "
            f"Keyword match ratio: {round(keyword_match_ratio*100,2)}%)")

    # -----------------------------
    # LangGraph Workflow for Email Decision
    # -----------------------------
    today = datetime.now().date()
    fixed_time = time(14, 0)
    now = datetime.combine(today, fixed_time).strftime("%d %B %Y, %I:%M %p")

    graph = StateGraph()
    graph.add_node("decide_email", lambda s: s)
    graph.add_edge("decide_email", END)
    email_workflow = graph.compile()

    email_decision = email_workflow.invoke({
        "skill_match": skill_match,
        "experience_level": experience_level,
        "now": now
    })

    subject = email_decision["subject"]
    body = email_decision["body"]

    # -----------------------------
    # Send Email
    # -----------------------------
    if candidate_email:
        try:
            send_email_app_password(candidate_email, subject, body, SENDER_EMAIL, GMAIL_PASS)
            st.success("📧 Email sent successfully!")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
