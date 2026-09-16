
# =========================================================
# app/rag_pipeline.py
# =========================================================

import time
import traceback

from langchain_ollama import ChatOllama

from app.config import LLM_MODEL, OLLAMA_BASE_URL
from app.prompts import RAG_PROMPT


# =========================================================
# Create LLM once
# =========================================================

print("=" * 60)
print("Initializing Ollama LLM")
print(f"LLM Model       : {LLM_MODEL}")
print(f"Ollama Base URL : {OLLAMA_BASE_URL}")
print("=" * 60)


llm = ChatOllama(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)


# =========================================================
# Generate Answer
# =========================================================

def generate_answer(question: str, retriever) -> str:

    total_start = time.perf_counter()

    # =====================================================
    # 1. Retrieve Relevant Documents
    # =====================================================

    retrieval_start = time.perf_counter()

    try:

        documents = retriever.invoke(question)

    except Exception as e:

        print("\n" + "=" * 60)
        print("RETRIEVER ERROR")
        print(f"Error: {e}")
        traceback.print_exc()
        print("=" * 60)

        raise RuntimeError(
            f"Failed to retrieve documents: {e}"
        ) from e

    retrieval_time = time.perf_counter() - retrieval_start

    print("\n" + "=" * 60)
    print("RAG REQUEST")
    print(f"Question         : {question}")
    print(f"Retrieval Time   : {retrieval_time:.2f} seconds")
    print(f"Chunks Retrieved : {len(documents)}")


    # =====================================================
    # 2. Check Retrieved Documents
    # =====================================================

    if not documents:

        total_time = time.perf_counter() - total_start

        print("No documents retrieved.")
        print(f"Total Time       : {total_time:.2f} seconds")
        print("=" * 60)

        return (
            "I could not find relevant information in the "
            "Employee Handbook for this question."
        )


    # =====================================================
    # 3. Prepare Context
    # =====================================================

    context = "\n\n".join(
        document.page_content
        for document in documents
        if getattr(document, "page_content", None)
    )

    print(f"Context Length   : {len(context)} characters")


    # =====================================================
    # 4. Create Prompt
    # =====================================================

    try:

        prompt = RAG_PROMPT.invoke(
            {
                "context": context,
                "question": question,
            }
        )

    except Exception as e:

        print("\n" + "=" * 60)
        print("PROMPT ERROR")
        print(f"Error: {e}")
        traceback.print_exc()
        print("=" * 60)

        raise RuntimeError(
            f"Failed to create prompt: {e}"
        ) from e


    # =====================================================
    # 5. Generate Answer with Ollama
    # =====================================================

    llm_start = time.perf_counter()

    try:

        response = llm.invoke(prompt)

    except Exception as e:

        llm_time = time.perf_counter() - llm_start

        print("\n" + "=" * 60)
        print("LLM ERROR")
        print(f"LLM Model       : {LLM_MODEL}")
        print(f"Ollama URL      : {OLLAMA_BASE_URL}")
        print(f"LLM Time        : {llm_time:.2f} seconds")
        print(f"Error           : {e}")
        traceback.print_exc()
        print("=" * 60)

        raise RuntimeError(
            f"Failed to generate answer using Ollama: {e}"
        ) from e


    llm_time = time.perf_counter() - llm_start


    # =====================================================
    # 6. Validate LLM Response
    # =====================================================

    answer = getattr(response, "content", None)

    if not answer:

        raise RuntimeError(
            "LLM returned an empty response."
        )


    answer = str(answer).strip()


    # =====================================================
    # 7. Total Time
    # =====================================================

    total_time = time.perf_counter() - total_start

    print(f"LLM Time         : {llm_time:.2f} seconds")
    print(f"Total Time       : {total_time:.2f} seconds")
    print("=" * 60)


    return answer

