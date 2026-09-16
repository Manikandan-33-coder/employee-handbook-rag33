
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

    # Create FAISS vector store
    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    # Make sure the parent directory exists
    FAISS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ---------------------------------------------------------
    # IMPORTANT
    #
    # FAISS.save_local("vector_db/faiss_index")
    # creates:
    #
    # vector_db/
    # └── faiss_index/
    #     ├── index.faiss
    #     └── index.pkl
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # FAISS_PATH points to the directory:
    #
    # vector_db/faiss_index/
    #
    # Therefore the actual files are:
    #
    # vector_db/faiss_index/index.faiss
    # vector_db/faiss_index/index.pkl
    # ---------------------------------------------------------

    index_directory = Path(FAISS_PATH)

    index_file = index_directory / "index.faiss"
    metadata_file = index_directory / "index.pkl"

    print("=" * 60)
    print("Checking FAISS vector store...")
    print(f"FAISS directory : {index_directory}")
    print(f"FAISS index     : {index_file}")
    print(f"FAISS metadata  : {metadata_file}")

    # Check FAISS index
    if not index_file.exists():

        raise FileNotFoundError(
            f"FAISS index file not found: {index_file}"
        )

    # Check metadata
    if not metadata_file.exists():

        raise FileNotFoundError(
            f"FAISS metadata file not found: {metadata_file}"
        )

    print("FAISS files found.")
    print("Loading FAISS vector store...")

    # Load FAISS index
    vectorstore = FAISS.load_local(
        str(FAISS_PATH),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    print("FAISS vector store loaded successfully.")
    print("=" * 60)

    return vectorstore

