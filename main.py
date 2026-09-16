# main.py

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.retriever import get_retriever
from app.rag_pipeline import generate_answer


# =========================================================
# Global Retriever
# =========================================================

retriever = None


# =========================================================
# Application Startup / Shutdown
# =========================================================

@asynccontextmanager
async def lifespan(app: FastAPI):

    global retriever

    print("=" * 60)
    print("Starting MvM Technologies Employee Handbook RAG")
    print("=" * 60)

    print("Loading FAISS vector store...")

    try:
        retriever = get_retriever()

        print("Retriever loaded successfully.")

    except Exception as e:

        print(f"Failed to load retriever: {e}")
        raise

    yield

    print("Application shutting down...")


# =========================================================
# FastAPI Application
# =========================================================

app = FastAPI(
    title="MvM Technologies Employee Handbook RAG",
    description="AI-powered Employee Handbook Assistant",
    version="1.0.0",
    lifespan=lifespan
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    # For development.
    # Later, replace "*" with your Render frontend URL.
    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =========================================================
# Request Model
# =========================================================

class QuestionRequest(BaseModel):
    question: str


# =========================================================
# Root Endpoint
# =========================================================

@app.get("/")
def root():

    return {
        "message": "MvM Technologies Employee Handbook RAG API is running."
    }


# =========================================================
# Health Check
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "retriever_loaded": retriever is not None
    }


# =========================================================
# Ask Question
# =========================================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    # Check empty question
    if not request.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )


    # Check retriever
    if retriever is None:

        raise HTTPException(
            status_code=503,
            detail="RAG system is not ready."
        )


    try:

        answer = generate_answer(
            question=request.question,
            retriever=retriever
        )

        return {
            "question": request.question,
            "answer": answer
        }


    except Exception as e:

        print(f"RAG error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to generate answer."
        )
