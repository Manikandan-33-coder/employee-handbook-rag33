
# =========================================================
# app/config.py
# =========================================================

from pathlib import Path
import os

from dotenv import load_dotenv


# =========================================================
# 1. Project Base Directory
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =========================================================
# 2. Load Environment Variables
# =========================================================

# Loads variables from .env when running locally.
# On Render, environment variables configured in the
# Render dashboard are also available through os.getenv().
load_dotenv(BASE_DIR / ".env")


# =========================================================
# 3. Employee Handbook PDF
# =========================================================

PDF_PATH = (
    BASE_DIR
    / "data"
    / "MvM_Technologies_Employee_Handbook.pdf"
)


# =========================================================
# 4. FAISS Vector Database
# =========================================================

FAISS_PATH = (
    BASE_DIR
    / "vector_db"
    / "faiss_index"
)


# =========================================================
# 5. Embedding Model
# =========================================================

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2"
)


# =========================================================
# 6. LLM Configuration
# =========================================================

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "qwen2.5:1.5b"
)


# IMPORTANT:
# Do NOT rely on localhost for a cloud deployment unless
# Ollama is running inside the same Render service.
#
# For local development:
#     OLLAMA_BASE_URL=http://localhost:11434
#
# For Render:
#     Set OLLAMA_BASE_URL to a reachable Ollama server URL
#     in Render Environment Variables.
OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)


# =========================================================
# 7. Text Splitting Configuration
# =========================================================

CHUNK_SIZE = int(
    os.getenv(
        "CHUNK_SIZE",
        "400"
    )
)

CHUNK_OVERLAP = int(
    os.getenv(
        "CHUNK_OVERLAP",
        "50"
    )
)


# =========================================================
# 8. Retrieval Configuration
# =========================================================

TOP_K = int(
    os.getenv(
        "TOP_K",
        "2"
    )
)

