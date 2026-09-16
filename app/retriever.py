
# =========================================================
# app/retriever.py
# =========================================================

from app.config import TOP_K
from app.embeddings import get_embeddings
from app.vectorstore import load_vectorstore


# =========================================================
# Create Retriever
# =========================================================

def get_retriever():
    """
    Load the FAISS vector store and return a retriever.
    """

    print("=" * 60)
    print("Initializing retriever...")
    print(f"Top K : {TOP_K}")

    # -----------------------------------------------------
    # 1. Create embedding model
    # -----------------------------------------------------

    embeddings = get_embeddings()

    if embeddings is None:
        raise RuntimeError(
            "Failed to initialize embedding model."
        )

    # -----------------------------------------------------
    # 2. Load FAISS vector store
    # -----------------------------------------------------

    vectorstore = load_vectorstore(
        embeddings
    )

    if vectorstore is None:
        raise RuntimeError(
            "Failed to load FAISS vector store."
        )

    # -----------------------------------------------------
    # 3. Convert vector store to retriever
    # -----------------------------------------------------

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": TOP_K
        },
    )

    print("Retriever initialized successfully.")
    print("=" * 60)

    return retriever

