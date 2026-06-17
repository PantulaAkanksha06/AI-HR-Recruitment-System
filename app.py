import streamlit as st

from backend.qdrant_manager import create_collection

# Create Qdrant collection when app starts
create_collection()

st.set_page_config(
    page_title="AI HR Recruitment System",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<div style='text-align:center;padding:20px'>
    <h1>🤖 AI HR Recruitment System</h1>
    <h4>Intelligent Resume Screening & Candidate Evaluation Platform</h4>
</div>
""", unsafe_allow_html=True)

st.markdown("""
### AI Powered Recruitment Platform

Features:

✔ Resume Parsing

✔ Candidate Ranking

✔ Semantic Job Matching

✔ Professional Email Generation

✔ Recruitment Dashboard

Use the sidebar to navigate.
""")

st.success("System Ready")