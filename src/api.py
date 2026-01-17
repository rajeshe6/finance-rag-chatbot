"""
FastAPI Backend for Finance RAG Chatbot
REST API endpoints for querying SEC filings
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import uvicorn

from rag_engine import RAGEngine

app = FastAPI(
    title="Finance RAG API",
    description="REST API for querying SEC filings using RAG",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Initializing RAG Engine...")
rag_engine = RAGEngine()
print("RAG Engine ready!")

class QueryRequest(BaseModel):
    question: str
    ticker: Optional[str] = None
    n_results: int = 5

class Source(BaseModel):
    ticker: str
    filing_type: str
    text: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[Source]

@app.get("/")
def read_root():
    return {
        "message": "Finance RAG API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.post("/query", response_model=QueryResponse)
def query_filings(request: QueryRequest):
    try:
        result = rag_engine.query(
            question=request.question,
            ticker=request.ticker,
            n_results=request.n_results
        )
        
        sources = [
            Source(
                ticker=chunk['ticker'],
                filing_type=chunk['filing_type'],
                text=chunk['text'][:500]
            )
            for chunk in result['sources']
        ]
        
        return QueryResponse(
            question=result['question'],
            answer=result['answer'],
            sources=sources
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/companies")
def get_companies():
    from config import TECH_COMPANIES
    return {
        "companies": TECH_COMPANIES,
        "total": len(TECH_COMPANIES)
    }

@app.get("/stats")
def get_stats():
    try:
        count = rag_engine.collection.count()
        return {
            "total_chunks": count,
            "embedding_model": "intfloat/e5-large-v2",
            "llm_model": "llama3.1:8b",
            "vector_db": "ChromaDB"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )