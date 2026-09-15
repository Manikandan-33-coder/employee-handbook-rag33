# app/config.py

from pathlib import Path
import os

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


PDF_PATH = (
    BASE_DIR
    / "data"
    / "MvM_Technologies_Employee_Handbook.pdf"
)

FAISS_PATH = (
    BASE_DIR
    / "vector_db"
    / "faiss_index"
)


EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


CHUNK_SIZE = 400
CHUNK_OVERLAP = 50
TOP_K = 2
