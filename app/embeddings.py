
# =========================================================
# app/embeddings.py
# =========================================================

from langchain_huggingface import HuggingFaceEmbeddings

from app.config import EMBEDDING_MODEL


# =========================================================
# Create Embedding Model
# =========================================================

def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Create and return the Hugging Face embedding model.
    """

    print("=" * 60)
    print("Loading embedding model...")
    print(f"Embedding Model : {EMBEDDING_MODEL}")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        encode_kwargs={
            "normalize_embeddings": True
        },
    )

    print("Embedding model loaded successfully.")
    print("=" * 60)

    return embeddings

