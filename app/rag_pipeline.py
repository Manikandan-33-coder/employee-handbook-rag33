
# =========================================================
# app/rag_pipeline.py
# =========================================================

import time
import traceback

from groq import Groq

from app.config import GROQ_API_KEY, GROQ_MODEL
from app.prompts import RAG_PROMPT


# =========================================================
# Validate Groq Configuration
# =========================================================

if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is not configured."
    )


# =========================================================
# Create Groq Client Once
# =========================================================

print("=" * 60)
print("Initializing Groq LLM")
print(f"Groq Model : {GROQ_MODEL}")
print("=" * 60)

groq_client = Groq(
    api_key=GROQ_API_KEY
)


# =========================================================
# Generate Answer
# =========================================================

def generate_answer(
    question: str,
    retriever
) -> str:

    total_start = time.perf_counter()


    # =====================================================
    # 1. Retrieve Relevant Documents
    # =====================================================

    retrieval_start = time.perf_counter()

    try:

        documents = retriever.invoke(
            question
        )

    except Exception as e:

        print("\n" + "=" * 60)
        print("RETRIEVER ERROR")
        print(f"Error: {e}")
        traceback.print_exc()
        print("=" * 60)

        raise RuntimeError(
            f"Failed to retrieve documents: {e}"
        ) from e


    retrieval_time = (
        time.perf_counter()
        - retrieval_start
    )


    print("\n" + "=" * 60)
    print("RAG REQUEST")
    print(f"Question         : {question}")
    print(
        f"Retrieval Time   : "
        f"{retrieval_time:.2f} seconds"
    )
    print(
        f"Chunks Retrieved : "
        f"{len(documents)}"
    )


    # =====================================================
    # 2. Check Retrieved Documents
    # =====================================================

    if not documents:

        total_time = (
            time.perf_counter()
            - total_start
        )

        print("No relevant documents found.")
        print(
            f"Total Time       : "
            f"{total_time:.2f} seconds"
        )
        print("=" * 60)

        return (
            "I could not find this information "
            "in the Employee Handbook."
        )


    # =====================================================
    # 3. Prepare Context
    # =====================================================

    context = "\n\n".join(
        document.page_content
        for document in documents
        if getattr(
            document,
            "page_content",
            None
        )
    )


    print(
        f"Context Length   : "
        f"{len(context)} characters"
    )


    # =====================================================
    # 4. Create LangChain Prompt
    # =====================================================

    try:

        prompt_value = RAG_PROMPT.invoke(
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
    # 5. Convert LangChain Messages to Groq Messages
    # =====================================================

    try:

        messages = []

        for message in prompt_value.to_messages():

            # LangChain message types:
            #
            # SystemMessage -> system
            # HumanMessage  -> user
            # AIMessage     -> assistant

            if message.type == "system":
                role = "system"

            elif message.type == "human":
                role = "user"

            elif message.type == "ai":
                role = "assistant"

            else:
                role = "user"


            messages.append(
                {
                    "role": role,
                    "content": str(
                        message.content
                    ),
                }
            )

    except Exception as e:

        print("\n" + "=" * 60)
        print("MESSAGE CONVERSION ERROR")
        print(f"Error: {e}")
        traceback.print_exc()
        print("=" * 60)

        raise RuntimeError(
            f"Failed to prepare Groq messages: {e}"
        ) from e


    # =====================================================
    # 6. Generate Answer Using Groq
    # =====================================================

    llm_start = time.perf_counter()

    try:

        response = (
            groq_client.chat.completions.create(
                model=GROQ_MODEL,
                messages=messages,
                temperature=0.0,
                max_completion_tokens=300,
                stream=False,
            )
        )

    except Exception as e:

        llm_time = (
            time.perf_counter()
            - llm_start
        )

        print("\n" + "=" * 60)
        print("GROQ LLM ERROR")
        print(f"Model       : {GROQ_MODEL}")
        print(
            f"LLM Time    : "
            f"{llm_time:.2f} seconds"
        )
        print(f"Error       : {e}")
        traceback.print_exc()
        print("=" * 60)

        raise RuntimeError(
            f"Failed to generate answer using Groq: {e}"
        ) from e


    llm_time = (
        time.perf_counter()
        - llm_start
    )


    # =====================================================
    # 7. Extract Answer
    # =====================================================

    try:

        answer = (
            response
            .choices[0]
            .message
            .content
        )

    except Exception as e:

        print("\n" + "=" * 60)
        print("GROQ RESPONSE ERROR")
        print(f"Error: {e}")
        traceback.print_exc()
        print("=" * 60)

        raise RuntimeError(
            "Groq returned an invalid response."
        ) from e


    if not answer:

        raise RuntimeError(
            "Groq returned an empty response."
        )


    answer = str(answer).strip()


    # =====================================================
    # 8. Total Time
    # =====================================================

    total_time = (
        time.perf_counter()
        - total_start
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


    return answer

