import streamlit as st
import openai
import pandas as pd
from dotenv import load_dotenv
import os
from fpdf import FPDF

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Function to generate candidate profile using OpenAI
def generate_profile(responses):
    prompt = f"""
    You are a hiring director at a fast-growing pre-IPO tech company looking for top-tier talent. Generate a structured and detailed candidate profile that includes:
    - A compelling professional summary highlighting expertise and achievements
    - Technical stack and hard skills relevant to the role
    - Soft skills that enhance leadership, collaboration, and innovation
    - A section where the candidate showcases their unique strengths and differentiators
    - An overall assessment of their fit for high-impact roles in scaling tech organizations
    
    Candidate Information:
    {responses}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI that creates high-caliber candidate profiles for pre-IPO tech companies."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Function to generate a PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", style='B', size=16)
        self.cell(200, 10, "Candidate Portfolio", ln=True, align='C')
        self.ln(10)
    
    def chapter_title(self, title):
        self.set_font("Arial", style='B', size=12)
        self.cell(0, 10, title, ln=True, align='L')
        self.ln(4)
    
    def chapter_body(self, body):
        self.set_font("Arial", size=12)
        self.multi_cell(0, 10, body)
        self.ln()
    
    def generate_pdf(self, profile_data):
        self.add_page()
        for section, content in profile_data.items():
            self.chapter_title(section)
            self.chapter_body(content)
        return self.output(dest='S').encode('latin1')

# Streamlit UI Enhancements
st.set_page_config(page_title="BeyondResumes - AI Candidate Portfolio", layout="centered")
st.title("🚀 AI Candidate Portfolio Generator")
st.write("### Designed for pre-IPO tech hiring directors who need top-tier talent insights.")

with st.form("candidate_form"):
    name = st.text_input("📝 Full Name", placeholder="John Doe")
    role = st.text_input("💼 Desired Role", placeholder="Software Engineer")
    tech_stack = st.text_area("🖥️ Tech Stack (Languages, Frameworks, Tools)", placeholder="Python, React, Kubernetes, AWS, etc.")
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
            "Career Highlights": achievements
        }
        profile_output = generate_profile(candidate_data)
        
        st.subheader("📌 High-Impact Candidate Portfolio")
        st.write(profile_output)
        
        # Generate and allow PDF download
        pdf = PDF()
        pdf_content = pdf.generate_pdf(candidate_data)
        st.download_button(
            label="📥 Download Portfolio as PDF",
            data=pdf_content,
            file_name=f"{name}_portfolio.pdf",
            mime="application/pdf"
        )
        
        # Allow user to download as Text File
        st.download_button(
            label="📥 Download Portfolio as Text File",
            data=profile_output,
            file_name=f"{name}_portfolio.txt",
            mime="text/plain"
        )
