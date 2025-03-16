import streamlit as st
import openai
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Function to generate candidate profile using OpenAI
def generate_profile(responses):
    prompt = f"""
    Generate a structured, professional candidate profile based on the following information:
    {responses}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI that creates structured candidate profiles."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.set_page_config(page_title="BeyondResumes - AI Candidate Portfolio")
st.title("AI Candidate Portfolio Generator")
st.write("Create a structured, AI-powered candidate portfolio that highlights your skills and achievements.")

with st.form("candidate_form"):
    name = st.text_input("Full Name", placeholder="John Doe")
    role = st.text_input("Desired Role", placeholder="Software Engineer")
    experience = st.text_area("Describe your past work experience", placeholder="Provide a brief overview of your work experience...")
    skills = st.text_area("List your key skills", placeholder="Python, Project Management, AI Research, etc.")
    achievements = st.text_area("Highlight your top achievements", placeholder="Led a team of 5 engineers to develop an AI-powered chatbot...")
    
    submitted = st.form_submit_button("Generate Portfolio")

if submitted:
    if not name or not role or not experience or not skills or not achievements:
        st.warning("Please fill in all fields before submitting.")
    else:
        candidate_data = {
            "Name": name,
            "Desired Role": role,
            "Experience": experience,
            "Skills": skills,
            "Achievements": achievements
        }
        profile_output = generate_profile(candidate_data)
        
        st.subheader("Generated Candidate Portfolio")
        st.write(profile_output)
        
        # Allow user to download their profile
        st.download_button(
            label="Download Portfolio as Text File",
            data=profile_output,
            file_name=f"{name}_portfolio.txt",
            mime="text/plain
        )
        
