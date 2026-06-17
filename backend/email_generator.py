import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_professional_email(
    candidate_name,
    position,
    score,
    status
):

    prompt = f"""
Generate a professional HR email.

Candidate Name: {candidate_name}
Position Applied For: {position}
Evaluation Score: {score}
Application Status: {status}

Company Name: AI Recruitment Solutions
HR Name: Akanksha Pantula

Rules:
- Do NOT use placeholders.
- Use the candidate's name.
- Be professional and polite.
- If shortlisted, congratulate the candidate and mention next steps.
- If rejected, be encouraging and respectful.
- Do not sound robotic.

End the email exactly as:

Best Regards,
Akanksha Pantula
HR Manager
AI Recruitment Solutions

Write a professional email.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content