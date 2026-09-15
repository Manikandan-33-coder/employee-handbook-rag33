# tests/test_question.py

from app.retriever import get_retriever
from app.rag_pipeline import generate_answer


def test_question(question):
    """
    Test the RAG system with a user question.
    """

    # Get the retriever
    retriever = get_retriever()

    # Generate the answer
    answer = generate_answer(
        question=question,
        retriever=retriever
    )

    print("\n" + "=" * 60)
    print("QUESTION:")
    print(question)

    print("\nANSWER:")
    print(answer)

    print("=" * 60)


if __name__ == "__main__":

    question = "What is the notice period?"

    test_question(question)