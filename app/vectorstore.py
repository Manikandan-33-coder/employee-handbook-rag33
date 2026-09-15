# app/vectorstore.py

from langchain_community.vectorstores import FAISS

from app.config import FAISS_PATH


def create_vectorstore(chunks, embeddings):
    """
    Create a FAISS vector store from document chunks
    and their embeddings.
    """

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )

    # Save FAISS index locally
    FAISS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    vectorstore.save_local(str(FAISS_PATH))

    return vectorstore


def load_vectorstore(embeddings):
    """
    Load the previously saved FAISS vector store.
    """

    vectorstore = FAISS.load_local(
        str(FAISS_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )

    return vectorstore