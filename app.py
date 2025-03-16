import streamlit as st
import openai
import pandas as pd
import os
import docx2txt
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from fpdf import FPDF

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Function to parse resumes
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

# Function to generate dynamic AI questions
def generate_dynamic_questions(parsed_text):
    prompt = f"""
    Based on the following resume text, generate three strategic interview questions to assess this candidate's skills, experience, and potential growth areas:
    {parsed_text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI that creates strategic interview questions for pre-IPO hiring directors."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Streamlit UI Enhancements
st.set_page_config(page_title="Rising Stars - Super Stars, All Need Apply", layout="wide")
st.title("🌟 Rising Stars - Super Stars, All Need Apply")
st.markdown("#### Designed for pre-IPO tech hiring directors who need top-tier talent insights.")

# Sidebar for File Upload
st.sidebar.header("📂 Upload Your Resume")
uploaded_file = st.sidebar.file_uploader("Supported formats: PDF, DOC, DOCX", type=["pdf", "doc", "docx"])
parsed_text = parse_resume(uploaded_file)

dynamic_questions = ""
if parsed_text:
    st.sidebar.subheader("📌 Extracted Resume Content")
    st.sidebar.text_area("", parsed_text, height=150)
    
    # Generate AI-powered interview questions
    dynamic_questions = generate_dynamic_questions(parsed_text)
    st.sidebar.subheader("🎯 AI-Generated Interview Questions")
    st.sidebar.write(dynamic_questions)

# Main Form Layout
st.markdown("---")
st.subheader("💼 Candidate Information")
with st.form("candidate_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("📝 Full Name", placeholder="John Doe")
        role = st.text_input("💼 Desired Role", placeholder="Software Engineer")
        tech_stack = st.text_area("🖥️ Tech Stack", placeholder="Python, React, Kubernetes, AWS, etc.")
    
    with col2:
        experience = st.text_area("📜 Work Experience Summary", placeholder="Provide a concise summary of your most impactful roles and projects...")
        skills = st.text_area("🛠️ Hard & Soft Skills", placeholder="Leadership, Distributed Systems, Agile Methodologies, Public Speaking, etc.")
        achievements = st.text_area("🏆 Career Highlights & Differentiators", placeholder="Led Series B growth strategy, scaled engineering team from 10 to 100, secured $50M in funding...")
    
    submitted = st.form_submit_button("✨ Generate Portfolio")

if submitted:
    if not name or not role or not tech_stack or not experience or not skills or not achievements:
        st.warning("⚠️ Please fill in all fields before submitting.")
    else:
        candidate_data = {
            "Name": name,
            "Desired Role": role,
            "Tech Stack": tech_stack,
            "Experience Summary": experience,
            "Skills & Competencies": skills,
            "Career Highlights": achievements,
            "AI-Generated Interview Questions": dynamic_questions
        }
        
        st.subheader("📌 High-Impact Candidate Portfolio")
        st.write(candidate_data)
        
        # Generate and allow PDF download
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", style='B', size=16)
        pdf.cell(200, 10, "Candidate Portfolio", ln=True, align='C')
        pdf.ln(10)
        for section, content in candidate_data.items():
            pdf.set_font("Arial", style='B', size=12)
            pdf.cell(0, 10, section, ln=True, align='L')
            pdf.ln(4)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, content)
            pdf.ln()
        pdf_content = pdf.output(dest='S').encode('latin1')
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Download Portfolio as PDF",
                data=pdf_content,
                file_name=f"{name}_portfolio.pdf",
                mime="application/pdf"
            )
        
        with col2:
            st.download_button(
                label="📥 Download Portfolio as Text File",
                data=str(candidate_data),
                file_name=f"{name}_portfolio.txt",
                mime="text/plain"
            )
