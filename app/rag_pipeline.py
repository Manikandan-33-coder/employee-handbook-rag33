# app/rag_pipeline.py

import time

from langchain_ollama import ChatOllama

from app.config import LLM_MODEL, OLLAMA_BASE_URL
from app.prompts import RAG_PROMPT


# Create LLM once
llm = ChatOllama(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0
)


def generate_answer(question, retriever):

    # Total timer
    total_start = time.perf_counter()

    # ---------------------------------------------------------
    # 1. Retrieve relevant chunks
    # ---------------------------------------------------------

    retrieval_start = time.perf_counter()

    documents = retriever.invoke(question)

    retrieval_time = time.perf_counter() - retrieval_start

    print("\n" + "=" * 60)
    print(f"Retrieval Time   : {retrieval_time:.2f} seconds")
    print(f"Chunks Retrieved : {len(documents)}")


    # ---------------------------------------------------------
    # 2. Prepare context
    # ---------------------------------------------------------

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    print(f"Context Length   : {len(context)} characters")


    # ---------------------------------------------------------
    # 3. Create prompt
    # ---------------------------------------------------------

    prompt = RAG_PROMPT.invoke(
        {
            "context": context,
            "question": question
        }
    )


    # ---------------------------------------------------------
    # 4. Generate answer
    # ---------------------------------------------------------

    llm_start = time.perf_counter()

    response = llm.invoke(prompt)

    llm_time = time.perf_counter() - llm_start


    # ---------------------------------------------------------
    # 5. Total time
    # ---------------------------------------------------------

    total_time = time.perf_counter() - total_start

    print(f"LLM Time         : {llm_time:.2f} seconds")
    print(f"Total Time       : {total_time:.2f} seconds")
    print("=" * 60)


    return response.content