import streamlit as st
import openai
import pandas as pd
import os
import docx2txt
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from fpdf import FPDF
import time

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Function to parse resumes and detect role
def parse_resume(uploaded_file):
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()
        
        if file_extension == "pdf":
            pdf_reader = PdfReader(uploaded_file)
            text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        elif file_extension in ["doc", "docx"]:
            text = docx2txt.process(uploaded_file)
        else:
            text = None
        
        return text
    return None

# Function to detect job role from resume text
def detect_role(parsed_text):
    prompt = f"""
    Analyze the following resume text and extract the most relevant job title:
    {parsed_text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI that detects job roles from resume text."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

# Function to generate tailored questions
def generate_role_specific_questions(role, seniority):
    prompt = f"""
    Generate a set of interview questions for a {seniority} {role} that tell a compelling story about their experience, leadership, and skills. Ensure the questionnaire can be completed in under 10 minutes.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI that creates engaging, concise interview questions."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

# Streamlit UI Enhancements
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

# Sidebar for File Upload
st.sidebar.header("📂 Upload Your Resume")
st.sidebar.markdown("Drag and drop a file or browse")
uploaded_file = st.sidebar.file_uploader("Supported formats: PDF, DOC, DOCX", type=["pdf", "doc", "docx"])
parsed_text = parse_resume(uploaded_file)

role_detected = ""
role_specific_questions = ""
if parsed_text:
    role_detected = detect_role(parsed_text)
    st.sidebar.subheader("🎯 Detected Job Role")
    st.sidebar.write(role_detected)
    
    seniority = st.sidebar.selectbox("Select Seniority Level", ["Entry-Level", "Mid-Level", "Senior", "Director", "Executive"])
    role_specific_questions = generate_role_specific_questions(role_detected, seniority)
    st.sidebar.subheader("📝 AI-Generated Interview Questions")
    st.sidebar.write(role_specific_questions)

# Estimated completion time based on number of questions
estimated_time = min(10, len(role_specific_questions.split("?")) * 1.5)

# Main Form Layout
st.markdown("---")
st.subheader(f"💼 Candidate Information (Estimated Time: {int(estimated_time)} min)")
with st.form("candidate_form"):
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        name = st.text_input("📝 Full Name", placeholder="John Doe")
        role = st.text_input("💼 Detected Role", value=role_detected, disabled=True)
        tech_stack = st.text_area("🖥️ Tech Stack", placeholder="Python, React, Kubernetes, AWS, etc.", height=100)
    
    with col2:
        experience = st.text_area("📜 Work Experience Summary", placeholder="Provide a concise summary of your most impactful roles and projects...", height=100)
        skills = st.text_area("🛠️ Hard & Soft Skills", placeholder="Leadership, Distributed Systems, Agile Methodologies, Public Speaking, etc.", height=100)
        achievements = st.text_area("🏆 Career Highlights & Differentiators", placeholder="Led Series B growth strategy, scaled engineering team from 10 to 100, secured $50M in funding...", height=100)
    
    submitted = st.form_submit_button("✨ Generate Portfolio")

if submitted:
    if not name or not tech_stack or not experience or not skills or not achievements:
        st.warning("⚠️ Please fill in all fields before submitting.")
    else:
        candidate_data = {
            "Name": name,
            "Role": role_detected,
            "Tech Stack": tech_stack,
            "Experience Summary": experience,
            "Skills & Competencies": skills,
            "Career Highlights": achievements,
            "AI-Generated Interview Questions": role_specific_questions
        }
        
        st.subheader("📌 High-Impact Candidate Portfolio")
        st.write(candidate_data)
