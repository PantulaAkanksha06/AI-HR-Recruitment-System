from sentence_transformers import SentenceTransformer, util

# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def get_embedding(text):
    """
    Generate embedding vector for Qdrant storage/search.
    Returns a Python list.
    """

    if not text:
        return []

    return model.encode(text).tolist()


def calculate_match_score(
    resume_text,
    job_description
):
    """
    Calculate semantic similarity score
    between resume and job description.
    """

    if not resume_text or not job_description:
        return 0.0

    resume_embedding = model.encode(
        resume_text,
        convert_to_tensor=True
    )

    jd_embedding = model.encode(
        job_description,
        convert_to_tensor=True
    )

    score = util.cos_sim(
        resume_embedding,
        jd_embedding
    )

    return round(
        float(score[0][0]) * 100,
        2
    )


def get_resume_embedding(resume_text):
    """
    Wrapper function for resume embeddings.
    """

    return get_embedding(resume_text)


def get_jd_embedding(job_description):
    """
    Wrapper function for JD embeddings.
    """

    return get_embedding(job_description)