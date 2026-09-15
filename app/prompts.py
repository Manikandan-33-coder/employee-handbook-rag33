# app/prompts.py

from langchain_core.prompts import ChatPromptTemplate


SYSTEM_PROMPT = """
You are the MvM Technologies Employee Handbook Assistant.

Answer only from the provided context.

Rules:
- Do not invent information.
- If the answer is not in the context, say:
  "I could not find this information in the Employee Handbook."
- Give a direct answer in 1 to 3 sentences.
- Use exact dates, numbers, and policy names from the context.
"""


RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_PROMPT
        ),
        (
            "human",
            """Context:
{context}

Question:
{question}

Answer briefly."""
        )
    ]
)
