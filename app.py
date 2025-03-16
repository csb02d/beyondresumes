import streamlit as st
import openai
import pandas as pd
import os
import docx2txt
import pdfplumber  # Replacing PyPDF2 for better PDF text extraction
from dotenv import load_dotenv
from fpdf import FPDF

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Job classification system using Pave.com's job families
job_families = {
    "Sales": ["SDR", "BDR", "Account Executive", "Sales Manager", "VP of Sales"],
    "Marketing": ["Marketing Coordinator", "Content Strategist", "SEO Specialist", "Growth Marketer", "CMO"],
    "Engineering": ["Software Engineer", "Backend Developer", "Frontend Developer", "Full Stack Developer", "DevOps Engineer"],
    "Product": ["Product Manager", "Product Designer", "UX Researcher", "Scrum Master", "Head of Product"],
    "Data Science": ["Data Analyst", "Machine Learning Engineer", "AI Researcher", "Data Engineer", "Chief Data Officer"],
    "Customer Success": ["Customer Support Specialist", "Customer Success Manager", "Head of Customer Success", "Implementation Specialist"],
    "Operations": ["Operations Manager", "Chief Operating Officer", "Business Operations Analyst"],
    "Finance": ["Financial Analyst", "Controller", "CFO"],
    "HR": ["HR Coordinator", "Recruiter", "VP of People"],
    "Legal": ["Legal Counsel", "Corporate Attorney", "Head of Legal"]
}

# Function to get job family based on role
def get_job_family(role):
    for family, roles in job_families.items():
        if role in roles:
            return family
    return "Unknown"

# ✅ FIXED: Enhanced Resume Parsing to Handle More Formats
def parse_resume(uploaded_file):
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        if file_extension == "pdf":
            text = ""
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text + "\n"
            if not text.strip():
                text = "PDF text extraction failed. Please try a DOCX file."
        
        elif file_extension in ["doc", "docx"]:
            text = docx2txt.process(uploaded_file)
        
        else:
            text = "Unsupported file format."

        return text
    return None

# ✅ FIXED: OpenAI API Call (APIRemovedInV1 Issue)
def detect_role(parsed_text):
    prompt = f"""
    Analyze the following resume text and extract the most relevant job title:
    {parsed_text}
    """
<<<<<<< HEAD
    response = openai.client.completions.create(
        model="gpt-4",
=======
    response = openai.client.completions.create(  # ✅ Updated API call
        model="gpt-4-turbo",
>>>>>>> eecda2e (Fixed OpenAI API & Improved Resume Parsing)
        messages=[{"role": "system", "content": "You are an AI that detects job roles from resume text."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

<<<<<<< HEAD
# Function to generate tailored questions
def generate_role_specific_questions(role, seniority):
    prompt = f"""
    Generate a set of interview questions for a {seniority} {role} that tell a compelling story about their experience, leadership, and skills. Ensure the questionnaire can be completed in under 10 minutes.
    """
    response = openai.ChatCompletions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI that creates engaging, concise interview questions."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

# Function to calculate match percentage
=======
# ✅ FIXED: OpenAI API Call for Job Fit Matching
>>>>>>> eecda2e (Fixed OpenAI API & Improved Resume Parsing)
def calculate_match_percentage(candidate_story, job_description):
    prompt = f"""
    Compare the following candidate story with the job description and provide a match percentage (0-100%) based on skills, experience, and alignment:
    
    Candidate Story:
    {candidate_story}
    
    Job Description:
    {job_description}
    """
<<<<<<< HEAD
    response = openai.ChatCompletions.create(
        model="gpt-4",
=======
    response = openai.client.completions.create(  # ✅ Updated API call
        model="gpt-4-turbo",
>>>>>>> eecda2e (Fixed OpenAI API & Improved Resume Parsing)
        messages=[{"role": "system", "content": "You are an AI that evaluates job fit and provides a match percentage."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# ✅ Streamlit UI Enhancements
st.set_page_config(page_title="Rising Stars - Super Stars, All Need Apply", layout="wide")
st.markdown("""
    <style>
        .big-title { text-align: center; font-size: 36px; font-weight: bold; color: #4A90E2; }
        .sub-title { text-align: center; font-size: 20px; color: #555; }
        .stButton>button { background-color: #4A90E2; color: white; border-radius: 8px; padding: 8px 16px; }
        .stTextInput>div>div>input { border-radius: 8px; }
    </style>
    
    <div class="big-title">🌟 Rising Stars - Super Stars, All Need Apply</div>
    <div class="sub-title">Designed for pre-IPO tech hiring directors who need top-tier talent insights.</div>
""", unsafe_allow_html=True)

# ✅ Sidebar for File Upload
st.sidebar.header("📂 Upload Your Resume")
st.sidebar.markdown("Drag and drop a file or browse")
uploaded_file = st.sidebar.file_uploader("Supported formats: PDF, DOC, DOCX", type=["pdf", "doc", "docx"])
parsed_text = parse_resume(uploaded_file)

role_detected = ""
role_specific_questions = ""
if parsed_text:
    role_detected = detect_role(parsed_text)
    job_family = get_job_family(role_detected)
    st.sidebar.subheader("🎯 Detected Job Role")
    st.sidebar.write(f"{role_detected} (Job Family: {job_family})")

# ✅ Job description input for match percentage
target_job_description = st.text_area("📄 Paste Job Description to Compare", placeholder="Paste job description here...")
if target_job_description:
    match_percentage = calculate_match_percentage(parsed_text, target_job_description)
    st.subheader(f"🔍 AI Match Score: {match_percentage}")

# Estimated completion time based on number of questions
estimated_time = min(10, len(role_specific_questions.split("?")) * 1.5)

# Main Form Layout
st.markdown("---")
st.subheader(f"💼 Candidate Information (Estimated Time: {int(estimated_time)} min)")
