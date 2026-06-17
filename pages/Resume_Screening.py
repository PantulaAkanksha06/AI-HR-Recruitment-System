import os
import sqlite3
from typing import Optional

import pandas as pd
import streamlit as st
from backend.langfuse_config import langfuse

from backend.qdrant_manager import (
    create_collection,
    add_resume,
    get_collection_info,
)


from backend.matcher import (
    get_resume_embedding,
)

from dotenv import load_dotenv
from st_aggrid import AgGrid, GridOptionsBuilder

from backend.resume_parser import extract_resume_text
from backend.matcher import calculate_match_score

from backend.ranking import (
    analyze_resume_ai,
    extract_candidate_email,
    extract_candidate_name,
    generate_dashboard_summary,
    estimate_experience,
)



from backend.email_sender import (
    send_email,
)
from backend.email_generator import (
    generate_professional_email,
)


# ==================================================
# CONFIGURATION
# ==================================================

load_dotenv()

DB_PATH = "database/candidates.db"

SHORTLIST_THRESHOLD = 70

# ==================================================
# DATABASE FUNCTIONS
# ==================================================


def get_db_connection():

    os.makedirs("database", exist_ok=True)

    return sqlite3.connect(DB_PATH)

def create_database():

    create_query = """
   CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name TEXT,
    candidate_email TEXT,
    score REAL,
    experience TEXT,
    job_description TEXT,
    candidate_details TEXT,
    analysis TEXT,
    summary TEXT,
    status TEXT,
    email_sent INTEGER DEFAULT 0
    )
    """

    # Columns added in later versions that
    # may be missing from an existing table.
    migrations = [
        "ALTER TABLE candidates ADD COLUMN summary TEXT",
        "ALTER TABLE candidates ADD COLUMN status TEXT",
        "ALTER TABLE candidates ADD COLUMN email_sent INTEGER DEFAULT 0",
        "ALTER TABLE candidates ADD COLUMN experience TEXT",
    ]

    with get_db_connection() as conn:

        conn.execute(create_query)

        for migration in migrations:

            try:
                conn.execute(migration)

            except sqlite3.OperationalError:
                # Column already exists — safe to ignore.
                pass

        conn.commit()


def save_candidate(
    candidate_name,
    candidate_email,
    score,
    experience,
    job_description,
    candidate_details,
    analysis,
    summary,
    status,
    email_sent,
):

    query = """
    INSERT INTO candidates (
    candidate_name,
    candidate_email,
    score,
    experience,
    job_description,
    candidate_details,
    analysis,
    summary,
    status,
    email_sent
)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    with get_db_connection() as conn:

        conn.execute(
            query,
            (
                candidate_name,
                candidate_email,
                score,
                experience,
                job_description,
                candidate_details,
                analysis,
                summary,
                status,
                email_sent,
            ),
        )

        conn.commit()


# ==================================================
# EMAIL VALIDATION
# ==================================================


def is_valid_email(
    email: Optional[str]
):

    if not email:
        return False

    invalid_values = {
        "not found",
        "none",
        "n/a",
        "",
    }

    return (
        "@" in email
        and email.strip().lower()
        not in invalid_values
    )


# ==================================================
# EMAIL FUNCTIONS
# ==================================================


def send_candidate_email(
    candidate_name,
    candidate_email,
    match_score,
    status,
):

    subject = (
    "Interview Invitation"
    if status == "Shortlisted"
    else "Application Update"
    )

    email_body = generate_professional_email(
        candidate_name=candidate_name,
        position="Job Application",
        score=match_score,
        status=status,
    )

    try:

        send_email(
            sender_email=os.getenv(
                "EMAIL_ADDRESS"
            ),
            sender_password=os.getenv(
                "EMAIL_PASSWORD"
            ),
            receiver_email=candidate_email,
            subject=subject,
            body=email_body,
        )

        st.success(
            f"📧 Email sent to {candidate_email}"
        )

        return True

    except Exception as error:

        st.error(
            f"Email sending failed: {error}"
        )

        return False


# ==================================================
# RESUME ANALYSIS
# ==================================================


def analyze_candidate(
    uploaded_file,
    job_description,
):
    langfuse.trace(
        name=f"Candidate Processing - {uploaded_file.name}"
    )

    resume_text = extract_resume_text(
        uploaded_file
    )

    
    resume_embedding = get_resume_embedding(
        resume_text
    )

    candidate_name = extract_candidate_name(
        resume_text
        
    )

    candidate_email = extract_candidate_email(
        resume_text
    )
    candidate_id = abs(
        hash(
            candidate_name 
            + candidate_email 
            + uploaded_file.name
            + str(len(resume_text))
        )
    )
    experience = estimate_experience(
        resume_text
    )


    # ----------------------------------
    # Email Validation
    # ----------------------------------

    if not is_valid_email(candidate_email):

        st.warning(
            f"Email not found in {candidate_name}'s resume."
        )

        candidate_email = "Pending"

        st.info(
            "⚠️ Email not found. Candidate saved as Pending. "
            "You can send email later from Dashboard."
        )

    else:

        st.success(
            f"📧 Email Found: {candidate_email}"
        )

    # ----------------------------------
    # Match Score
    # ----------------------------------

    match_score = calculate_match_score(
        resume_text,
        job_description,
    )

    add_resume(
        candidate_id,
        resume_embedding,
        candidate_name,
        candidate_email,
        uploaded_file.name,
    )

    st.success(
        f"🎯 Match Score: {match_score:.2f}%"
    )

    st.info(
        f"💼 Estimated Experience: {experience} Years"
    )

    st.markdown(
        f"""
        <div style="
        padding:15px;
        border-radius:10px;
        background:#1E293B;
        margin-bottom:10px;
        ">
        <h4>{candidate_name}</h4>
        <p>📧 {candidate_email}</p>
        <p>💼 {experience}</p>
        <p>🎯 {match_score}% Match</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ----------------------------------
    # AI Analysis
    # ----------------------------------

    analysis = analyze_resume_ai(
        resume_text,
        job_description,
    )

    summary = generate_dashboard_summary(
        resume_text,
        job_description,
    )

    st.subheader(
        "🤖 AI Recruiter Analysis"
    )

    st.markdown(analysis)

    # ----------------------------------
    # Status
    # ----------------------------------

    status = (
        "Shortlisted"
        if match_score >= SHORTLIST_THRESHOLD
        else "Rejected"
    )

    st.info(
        f"Status: {status}"
    )

    # ----------------------------------
    # Send Email
    # ----------------------------------

    if candidate_email == "Pending":

        email_sent = 0

        st.warning(
            "📭 Email skipped — no valid address on file."
        )

    else:

        email_sent = (
            1
            if send_candidate_email(
                candidate_name,
                candidate_email,
                match_score,
                status,
            )
            else 0
        )

    # ----------------------------------
    # Save Candidate
    # ----------------------------------

    save_candidate(
        candidate_name,
        candidate_email,
        match_score,
        experience,
        job_description,
        resume_text,
        analysis,
        summary,
        status,
        email_sent,
    )

    

    langfuse.flush()

    st.success(
        "✅ Candidate stored successfully."
    )


# ==================================================
# DASHBOARD FUNCTIONS
# ==================================================


def load_dashboard_data():

    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql_query(
        """
        SELECT
            candidate_name,
            candidate_email,
            score,
            experience,
            summary,
            status,
            email_sent
        FROM candidates
        ORDER BY score DESC
        """,
        conn,
    )

    conn.close()

    return df


def update_candidate_email(
    candidate_name,
    candidate_email,
):

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        """
        UPDATE candidates
        SET candidate_email = ?
        WHERE candidate_name = ?
        """,
        (
            candidate_email,
            candidate_name,
        ),
    )

    conn.commit()
    conn.close()


def mark_email_sent(
    candidate_name,
):

    conn = sqlite3.connect(DB_PATH)

    conn.execute(
        """
        UPDATE candidates
        SET email_sent = 1
        WHERE candidate_name = ?
        """,
        (candidate_name,),
    )

    conn.commit()
    conn.close()


def render_dashboard():

    st.header(
        "📊 Recruitment Dashboard"
    )
    
    st.markdown("""
    <style>
    div[data-testid="metric-container"] {
        background-color: #111827;
        border: 1px solid #334155;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}
</style>
""", unsafe_allow_html=True)
    
    if st.button(
        "🔄 Refresh Dashboard"
    ):
        st.rerun()

    df = load_dashboard_data()

    if df.empty:

        st.warning(
            "No candidates found."
        )

        return

    # ----------------------------------
    # Recommended Candidate
    # ----------------------------------

    best_candidate = df.iloc[0]

    st.info(
        f"""
    ⭐ Recommended Candidate

    Name: {best_candidate['candidate_name']}
    Score: {best_candidate['score']}%
    Experience: {best_candidate['experience']}

    Reason:
    Highest overall match score.    
    """
    )
    # ----------------------------------
    # Pending Email Badge
    # ----------------------------------

    df["email_status"] = df[
        "email_sent"
    ].apply(
        lambda x:
        "✅ Sent"
        if x == 1
        else "📭 Pending"
    )

    # ----------------------------------
    # KPI Cards
    # ----------------------------------

    st.subheader(
        "📈 Recruitment Overview"
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    with col1:

        st.metric(
            "Total Candidates",
            len(df),
        )

    with col2:

        st.metric(
            "Shortlisted",
            len(
                df[
                    df["score"]
                    >= SHORTLIST_THRESHOLD
                ]
            ),
        )

    with col3:

        st.metric(
            "Rejected",
            len(
                df[
                    df["score"]
                    < SHORTLIST_THRESHOLD
                ]
            ),
        )

    with col4:

        st.metric(
            "Average Score",
            f"{df['score'].mean():.1f}%",
        )
    

   

    st.divider()

    

    # ----------------------------------
    # Candidates Awaiting Email
    # ----------------------------------

    st.subheader(
        "📭 Candidates Awaiting Email"
    )

    pending_df = df[
        df["email_sent"] == 0
    ]

    if not pending_df.empty:

        for index, row in pending_df.iterrows():

            st.write(
                f"### {row['candidate_name']}"
            )

            new_email = st.text_input(
                f"Enter Email for {row['candidate_name']}",
                key=f"pending_{index}"
            )

            if st.button(
                f"Send Email to {row['candidate_name']}",
                key=f"send_{index}"
            ):

                if not is_valid_email(
                    new_email
                ):

                    st.error(
                        "Please enter a valid email."
                    )

                else:

                    success = send_candidate_email(
                        row["candidate_name"],
                        new_email,
                        row["score"],
                        row["status"],
                    )

                    if success:

                        update_candidate_email(
                            row["candidate_name"],
                            new_email,
                        )

                        mark_email_sent(
                            row["candidate_name"]
                        )

                        st.success(
                            "Email sent successfully."
                        )

                        st.rerun()

    else:

        st.success(
            "No candidates awaiting email."
        )

    st.divider()

    # ----------------------------------
    # Candidate Table
    # ----------------------------------

    st.subheader(
        "📋 Candidate Database"
    )

    display_df = df[
        [
            "candidate_name",
            "candidate_email",
            "experience",
            "score",
            "status",
            "email_status",
            "summary",
        ]
    ]

    display_df.columns = [
        "Candidate Name",
        "Email",
        "Experience",
        "Score",
        "Status",
        "Email Sent",
        "AI Summary",
    ]

    gb = GridOptionsBuilder.from_dataframe(
        display_df
    )

    gb.configure_pagination(
        paginationAutoPageSize=False,
        paginationPageSize=10,
    )

    gb.configure_default_column(
        sortable=True,
        filter=True,
        resizable=True,
    )

    gb.configure_column(
        "Score",
        header_name="Match Score (%)",
    )

    gb.configure_column(
        "Email Sent",
        header_name="Email Sent",
    )

    gb.configure_column(
        "AI Summary",
        header_name="AI Summary",
        wrapText=True,
        autoHeight=True,
    )

    grid_options = gb.build()

    AgGrid(
        display_df,
        gridOptions=grid_options,
        height=450,
        fit_columns_on_grid_load=True,
        theme="streamlit",
        enable_enterprise_modules=False,
    )


# ==================================================
# MAIN APP
# ==================================================


def main():

    st.set_page_config(
        page_title="AI HR Recruitment System",
        page_icon="🤖",
        layout="wide",
    )

    create_database()
    create_collection()

    st.title(
        "🤖 AI HR Recruitment System"
    )

    tab1, tab2 = st.tabs(
        [
            "📄 Resume Screening",
            "📊 Dashboard",
        ]
    )

    # ==================================
    # TAB 1
    # ==================================

    with tab1:

        uploaded_files = st.file_uploader(
            "Upload Resume(s)",
            type=[
                "pdf",
                "docx",
                "txt",
            ],
            accept_multiple_files=True,
        )

        job_description = st.text_area(
            "Job Description",
            height=150
        )

        if st.button(
            "Analyze Candidates"
        ):

            if not uploaded_files:

                st.error(
                    "Please upload at least one resume."
                )

                return

            if not job_description.strip():

                st.error(
                    "Please enter a job description."
                )

                return

            total_resumes = len(
                uploaded_files
            )

            with st.spinner(
                f"Analyzing "
                f"{total_resumes} "
                f"resume(s)..."
                
            ):

                for index, uploaded_file in enumerate(
                    uploaded_files,
                    start=1,
                ):

                    st.divider()

                    st.subheader(
                        f"Resume {index} "
                        f"of {total_resumes}"
                    )

                    st.write(
                        uploaded_file.name
                    )

                    try:

                        analyze_candidate(
                            uploaded_file,
                            job_description,
                        )

                    except Exception as error:

                        st.error(
                            f"Error processing "
                            f"{uploaded_file.name}: "
                            f"{error}"
                        )

            st.success(
                f"✅ Finished processing "
                f"{total_resumes} "
                f"resume(s)"
            )

    # ==================================
    # TAB 2
    # ==================================

    with tab2:

        render_dashboard()


# ==================================================
# RUN APP
# ==================================================

if __name__ == "__main__":
    main()