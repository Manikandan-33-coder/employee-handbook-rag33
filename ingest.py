# ingest.py

from app.document_loader import load_handbook
from app.text_splitter import split_documents
from app.embeddings import get_embeddings
from app.vectorstore import create_vectorstore


def main():
    print("=" * 60)
    print("EMPLOYEE HANDBOOK - RAG INGESTION")
    print("=" * 60)

    # ---------------------------------------------------------
    # 1. Load the PDF
    # ---------------------------------------------------------

    print("\n[1/4] Loading Employee Handbook...")

    documents = load_handbook()

    print(f"Loaded {len(documents)} pages.")


    # ---------------------------------------------------------
    # 2. Split documents into chunks
    # ---------------------------------------------------------

    print("\n[2/4] Splitting document into chunks...")

    chunks = split_documents(documents)

    print(f"Created {len(chunks)} chunks.")


    # ---------------------------------------------------------
    # 3. Create embedding model
    # ---------------------------------------------------------

    print("\n[3/4] Creating embedding model...")

    embeddings = get_embeddings()

    print("Embedding model loaded successfully.")


    # ---------------------------------------------------------
    # 4. Create and save FAISS vector store
    # ---------------------------------------------------------

    print("\n[4/4] Creating FAISS vector store...")

    create_vectorstore(
        chunks=chunks,
        embeddings=embeddings
    )

    print("\nFAISS index created successfully.")
    print("Saved inside: vector_db/faiss_index/")


if __name__ == "__main__":
    main()