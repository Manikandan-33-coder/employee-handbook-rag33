# app/rag_pipeline.py

import os
import time

from google import genai

from app.config import GEMINI_MODEL
from app.prompts import SYSTEM_PROMPT


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured."
    )


client = genai.Client(
    api_key=api_key
)


def generate_answer(question, retriever):

    total_start = time.perf_counter()

    # ---------------------------------------------------------
    # 1. Retrieve relevant documents
    # ---------------------------------------------------------

    retrieval_start = time.perf_counter()

    documents = retriever.invoke(question)

    retrieval_time = (
        time.perf_counter() - retrieval_start
    )

    print("\n" + "=" * 60)
    print(
        f"Retrieval Time   : "
        f"{retrieval_time:.2f} seconds"
    )

    print(
        f"Chunks Retrieved : "
        f"{len(documents)}"
    )

    # ---------------------------------------------------------
    # 2. Build context
    # ---------------------------------------------------------

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    print(
        f"Context Length   : "
        f"{len(context)} characters"
    )

    # ---------------------------------------------------------
    # 3. Build prompt
    # ---------------------------------------------------------

    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer:
"""

    # ---------------------------------------------------------
    # 4. Gemini
    # ---------------------------------------------------------

    llm_start = time.perf_counter()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    llm_time = (
        time.perf_counter() - llm_start
    )

    total_time = (
        time.perf_counter() - total_start
    )

    print(
        f"LLM Time         : "
        f"{llm_time:.2f} seconds"
    )

    print(
        f"Total Time       : "
        f"{total_time:.2f} seconds"
    )

    print("=" * 60)

    return response.text
