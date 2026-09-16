
# =========================================================
# main.py
# =========================================================

from contextlib import asynccontextmanager
import traceback

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

        print("=" * 60)
        print("STARTUP ERROR")
        print(f"Error type : {type(e).__name__}")
        print(f"Error      : {e}")
        traceback.print_exc()
        print("=" * 60)

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
    lifespan=lifespan,
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "https://employee-handbook-rag33-7.onrender.com",
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],

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
        "retriever_loaded": retriever is not None,
    }


# =========================================================
# Ask Question
# =========================================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()


    # -----------------------------------------------------
    # Validate question
    # -----------------------------------------------------

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )


    # -----------------------------------------------------
    # Check RAG system
    # -----------------------------------------------------

    if retriever is None:

        raise HTTPException(
            status_code=503,
            detail="RAG system is not ready.",
        )


    # -----------------------------------------------------
    # Generate answer
    # -----------------------------------------------------

    try:

        print("\n" + "=" * 60)
        print("ASK REQUEST")
        print(f"Question: {question}")
        print("=" * 60)

        answer = generate_answer(
            question=question,
            retriever=retriever,
        )

        return {
            "question": question,
            "answer": answer,
        }


    except Exception as e:

        # Keep detailed error in Render logs
        print("\n" + "=" * 60)
        print("ASK ERROR")
        print(f"Error type : {type(e).__name__}")
        print(f"Error      : {e}")
        traceback.print_exc()
        print("=" * 60)


        # Safe message for API users
        raise HTTPException(
            status_code=500,
            detail="Failed to generate answer.",
        )

