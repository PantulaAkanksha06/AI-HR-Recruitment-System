from groq import Groq
import time
from dotenv import load_dotenv
import time
import os

# ==========================================
# Load Environment Variables
# ==========================================

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL_NAME = "llama-3.3-70b-versatile"


# ==========================================
# Common LLM Function
# ==========================================

def generate_response(
    prompt: str,
    trace_name: str = "AI HR Recruitment"
) -> str:

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

# ==========================================
# Candidate Details
# ==========================================

def extract_candidate_details(
    resume_text: str
) -> str:

    prompt = f"""
Extract the following information from the resume.

Resume:
{resume_text}

Return in this format:

Name:
Email:
Phone:
Skills:
Education:
Experience:
Projects:
Certifications:
"""

    return generate_response(prompt)


# ==========================================
# Candidate Name
# ==========================================

def extract_candidate_name(
    resume_text: str
) -> str:

    prompt = f"""
Extract ONLY the candidate's full name.

Resume:
{resume_text}

Return only the name.

If name is unavailable return:
Unknown Candidate
"""

    return generate_response(prompt)


# ==========================================
# Candidate Email
# ==========================================

def extract_candidate_email(
    resume_text: str
) -> str:

    prompt = f"""
Extract ONLY the candidate's email address.

Resume:
{resume_text}

Return ONLY the email.

If email is unavailable return:
NOT FOUND
"""

    return generate_response(prompt)


# ==========================================
# Resume Analysis
# ==========================================

def analyze_resume_ai(
    resume_text: str,
    job_description: str
) -> str:

    prompt = f"""
You are an HR recruiter.

Analyze the candidate's resume
against the job description.

JOB DESCRIPTION:
{job_description}

RESUME:
{resume_text}

Return ONLY in this format:

Strengths:
• point
• point
• point

Weaknesses:
• point
• point

Hiring Recommendation:
Shortlisted OR Rejected

Final Score:
number

Rules:
- Maximum 3 strengths
- Maximum 2 weaknesses
- One line per point
- No paragraphs
- No explanations
- Keep response under 100 words
"""

    return generate_response(prompt)


# ==========================================
# Dashboard Summary
# ==========================================

def generate_dashboard_summary(
    resume_text: str,
    job_description: str
) -> str:

    prompt = f"""
Resume:
{resume_text}

Job Description:
{job_description}

Generate a VERY SHORT HR summary.

Rules:
- One sentence only
- Maximum 15 words
- Mention key strength
- Mention major weakness
- No bullet points
- No headings

Example:

Strong Python skills. Limited FastAPI experience.

Another Example:

Good ML knowledge. Needs more industry experience.
"""

    return generate_response(prompt)


# ==========================================
# Testing
# ==========================================

if __name__ == "__main__":

    sample_resume = """
John Doe
john@gmail.com

Skills:
Python
SQL
Machine Learning

Projects:
Plant Disease Detection
AI Resume Screening
"""

    sample_jd = """
Looking for a Python Developer
with SQL and Machine Learning
experience.
"""

    print(
        extract_candidate_name(
            sample_resume
        )
    )

    print(
        extract_candidate_email(
            sample_resume
        )
    )

    print(
        extract_candidate_details(
            sample_resume
        )
    )

    print(
        analyze_resume_ai(
            sample_resume,
            sample_jd
        )
    )

    print(
        generate_dashboard_summary(
            sample_resume,
            sample_jd
        )
    )
def estimate_experience(
    resume_text: str
) -> str:

    prompt = f"""
You are an HR recruiter.

Analyze the resume and estimate
the candidate's total professional
experience.

Resume:
{resume_text}

Rules:
- Return ONLY a number.
- Example:
0
1
2
3.5
5

If candidate is a fresher return:
0
"""

    return generate_response(prompt)