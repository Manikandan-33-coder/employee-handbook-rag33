# app/retriever.py

from app.config import TOP_K
from app.vectorstore import load_vectorstore
from app.embeddings import get_embeddings


def get_retriever():
    """
    Load the FAISS vector store and return a retriever.
    """

    # Create embedding model
    embeddings = get_embeddings()

    # Load existing FAISS vector store
    vectorstore = load_vectorstore(embeddings)

    # Convert vector store into a retriever
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": TOP_K
        }
    )

    return retriever