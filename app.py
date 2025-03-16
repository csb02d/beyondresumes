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
    response = openai.ChatCompletion.create(  # ✅ Fixed API call
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI that detects job roles from resume text."},
            {"role": "user", "content": prompt}
        ]
    )
    return response["choices"][0]["message"]["content"].strip()

# Function to calculate match percentage
def calculate_match_percentage(candidate_story, job_description):
    prompt = f"""
    Compare the following candidate story with the job description and provide a match percentage (0-100%) based on skills, experience, and alignment:
    
    Candidate Story:
    {candidate_story}
    
    Job Description:
    {job_description}
    """
    response = openai.ChatCompletion.create(  # ✅ Fixed API call
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are an AI that evaluates job fit and provides a match percentage."},
            {"role": "user", "content": prompt}
        ]
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
if parsed_text:
    role_detected = detect_role(parsed_text)
    job_family = get_job_family(role_detected)
    st.sidebar.subheader("🎯 Detected Job Role")
    st.sidebar.write(f"{role_detected} (Job Family: {job_family})")

# Job description input for match percentage
target_job_description = st.text_area("📄 Paste Job Description to Compare", placeholder="Paste job description here...")
if target_job_description:
    match_percentage = calculate_match_percentage(parsed_text, target_job_description)
    st.subheader(f"🔍 AI Match Score: {match_percentage}")