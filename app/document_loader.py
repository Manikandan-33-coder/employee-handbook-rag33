# app/document_loader.py

from langchain_community.document_loaders import PyPDFLoader

from app.config import PDF_PATH


def load_handbook():
    """
    Load the Employee Handbook PDF.

    Returns:
        list: A list of LangChain Document objects.
    """

    loader = PyPDFLoader(str(PDF_PATH))

    documents = loader.load()

    return documents