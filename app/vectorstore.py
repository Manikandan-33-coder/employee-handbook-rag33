
# =========================================================
# app/vectorstore.py
# =========================================================

from pathlib import Path

from langchain_community.vectorstores import FAISS

from app.config import FAISS_PATH


# =========================================================
# Create Vector Store
# =========================================================

def create_vectorstore(chunks, embeddings):
    """
    Create a FAISS vector store from document chunks
    and their embeddings, then save it locally.
    """

    if not chunks:
        raise ValueError(
            "No document chunks were provided to create the vector store."
        )

    if embeddings is None:
        raise ValueError(
            "Embedding model is required to create the vector store."
        )

    print("=" * 60)
    print("Creating FAISS vector store...")
    print(f"Number of chunks : {len(chunks)}")
    print(f"FAISS path       : {FAISS_PATH}")

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    # Ensure parent directory exists
    FAISS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Save FAISS index locally
    vectorstore.save_local(
        str(FAISS_PATH)
    )

    print("FAISS vector store created successfully.")
    print("=" * 60)

    return vectorstore


# =========================================================
# Load Vector Store
# =========================================================

def load_vectorstore(embeddings):
    """
    Load the previously saved FAISS vector store.
    """

    if embeddings is None:
        raise ValueError(
            "Embedding model is required to load the vector store."
        )

    # FAISS.save_local() creates:
    #
    # vector_db/faiss_index/
    #     index.faiss
    #     index.pkl
    #
    index_file = Path(
        str(FAISS_PATH) + ".faiss"
    )

    pickle_file = Path(
        str(FAISS_PATH) + ".pkl"
    )

    if not index_file.exists():
        raise FileNotFoundError(
            f"FAISS index file not found: {index_file}"
        )

    if not pickle_file.exists():
        raise FileNotFoundError(
            f"FAISS metadata file not found: {pickle_file}"
        )

    print("=" * 60)
    print("Loading FAISS vector store...")
    print(f"FAISS path : {FAISS_PATH}")

    vectorstore = FAISS.load_local(
        str(FAISS_PATH),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    print("FAISS vector store loaded successfully.")
    print("=" * 60)

    return vectorstore

