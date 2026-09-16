```python
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

# Local development:
# Loads values from .env if that file exists.
#
# Render:
# Uses Environment Variables configured in the Render
# dashboard.

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
# 6. Groq LLM Configuration
# =========================================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
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
```
