🧠 Recruitment Screening Tool
An AI-powered Streamlit web app that automates the recruitment screening process by analyzing resumes, comparing them with job descriptions, and sending personalized selection emails automatically.
🧩 Instructions to Run Locally
1️⃣ Clone the repository
git clone https://github.com/your-username/Recruitment-Screening-Tool.git
cd Recruitment-Screening-Tool

2️⃣ Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

3️⃣ Install all dependencies
pip install -r requirements.txt

4️⃣ Set up Streamlit secrets
Create a file at:
.streamlit/secrets.toml
GEMINI_API_KEY = "your_gemini_api_key"
COHERE_API_KEY = "your_cohere_api_key"
GMAIL_APP_PASS = "your_gmail_app_password"

5️⃣ Run the Streamlit app
streamlit run app.py
Local URL: http://localhost:8501

<img width="862" height="479" alt="image" src="https://github.com/user-attachments/assets/dd1505c1-47c7-4d02-8d10-2fae8ac0e247" />
