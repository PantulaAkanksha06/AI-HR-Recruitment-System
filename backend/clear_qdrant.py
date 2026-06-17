from qdrant_client import QdrantClient
from qdrant_client.models import (
    FilterSelector,
    Filter
)
from dotenv import load_dotenv
import os

# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

# ==========================================
# CONNECT TO QDRANT
# ==========================================

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "resumes"

# ==========================================
# DELETE ALL POINTS
# ==========================================

def clear_collection():

    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=FilterSelector(
            filter=Filter()
        )
    )

    print(
        f"All points deleted from '{COLLECTION_NAME}' collection."
    )


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":

    clear_collection()