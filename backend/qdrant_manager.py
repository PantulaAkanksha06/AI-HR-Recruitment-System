from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

from dotenv import load_dotenv
import os

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

# ==========================================
# QDRANT CONNECTION
# ==========================================

print("Qdrant URL:", os.getenv("QDRANT_URL"))

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

COLLECTION_NAME = "resumes"

# ==========================================
# CREATE COLLECTION
# ==========================================

def create_collection():

    collections = [
        collection.name
        for collection
        in client.get_collections().collections
    ]

    if COLLECTION_NAME not in collections:

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE,
            ),
        )

        print(
            f"Collection '{COLLECTION_NAME}' created."
        )

    else:

        print(
            f"Collection '{COLLECTION_NAME}' already exists."
        )


# ==========================================
# ADD RESUME TO QDRANT
# ==========================================

def add_resume(
    candidate_id,
    embedding,
    candidate_name,
    candidate_email,
    filename,
):

    print("Adding to Qdrant...")
    print("Embedding length:", len(embedding))

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=candidate_id,
                vector=embedding,
                payload={
                    "name": candidate_name,
                    "email": candidate_email,
                    "filename": filename,
                },
            )
        ],
    )

    print(
        f"Stored resume in Qdrant: {candidate_name}"
    )


# ==========================================
# SEARCH RESUMES
# ==========================================

def search_resumes(
    jd_embedding,
    limit=10,
):

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=jd_embedding,
        limit=limit,
    )

    return results


# ==========================================
# GET COLLECTION INFO
# ==========================================

def get_collection_info():

    return client.get_collection(
        collection_name=COLLECTION_NAME
    )