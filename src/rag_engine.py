from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import ollama
from typing import List, Dict
import json

from config import (
    VECTOR_DB_DIR,
    EMBEDDING_MODEL,
    LLM_MODEL,
    TOP_K_RESULTS
)

class RAGEngine:
    
    def __init__(self):
        print(" Initializing RAG Engine...")
        
        print(f" Loading embedding model: {EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        print(" Embedding model loaded!")
        
        print(f" Connecting to ChromaDB...")
        self.client = chromadb.PersistentClient(
            path=str(VECTOR_DB_DIR),
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_collection("sec_filings")
        print(f" Connected! Found {self.collection.count()} documents")
        
        print(f" Testing Ollama connection...")
        try:
            ollama.list()
            print(f" Ollama connected! Using model: {LLM_MODEL}")
        except Exception as e:
            print(f" Ollama connection failed: {e}")
            print("Make sure Ollama is running!")
    
    def retrieve_context(self, query: str, n_results: int = TOP_K_RESULTS, 
                        ticker: str = None) -> List[Dict]:
        query_embedding = self.embedding_model.encode(f"query: {query}").tolist()
        
        where_filter = {"ticker": ticker} if ticker else None
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )
        
        context_chunks = []
        for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
            context_chunks.append({
                'text': doc,
                'ticker': metadata['ticker'],
                'filing_type': metadata['filing_type'],
                'accession': metadata['accession_number']
            })
        
        return context_chunks
    
    def generate_prompt(self, query: str, context_chunks: List[Dict]) -> str:
        context_text = ""
        for i, chunk in enumerate(context_chunks, 1):
            context_text += f"\n--- Context {i} ---\n"
            context_text += f"Company: {chunk['ticker']}\n"
            context_text += f"Filing: {chunk['filing_type']}\n"
            context_text += f"Content: {chunk['text']}\n"
        
        prompt = f"""You are a financial analyst assistant. Answer the question based on the provided SEC filing excerpts.

CONTEXT FROM SEC FILINGS:
{context_text}

QUESTION: {query}

INSTRUCTIONS:
1. Answer the question using ONLY the information from the context above
2. Be specific and cite which company and filing type you're referencing
3. If the context doesn't contain enough information, say so
4. Use numbers and facts from the filings when available
5. Keep your answer concise but informative

ANSWER:"""
        
        return prompt
    
    def generate_answer(self, prompt: str) -> str:
        try:
            response = ollama.generate(
                model=LLM_MODEL,
                prompt=prompt
            )
            return response['response']
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def query(self, question: str, ticker: str = None, n_results: int = TOP_K_RESULTS) -> Dict:
        print(f"\n{'='*60}")
        print(f" Question: {question}")
        if ticker:
            print(f" Company Filter: {ticker}")
        print(f"{'='*60}\n")
        
        print(" Retrieving relevant context...")
        context_chunks = self.retrieve_context(question, n_results, ticker)
        print(f" Found {len(context_chunks)} relevant chunks")
        
        print("\n Sources:")
        for i, chunk in enumerate(context_chunks, 1):
            print(f"  {i}. {chunk['ticker']} - {chunk['filing_type']}")
        
        prompt = self.generate_prompt(question, context_chunks)
        
        print("\n Generating answer with Llama 3.1...")
        answer = self.generate_answer(prompt)
        
        print(f"\n{'='*60}")
        print(" ANSWER:")
        print(f"{'='*60}")
        print(answer)
        print(f"{'='*60}\n")
        
        return {
            'question': question,
            'answer': answer,
            'sources': context_chunks
        }

def main():
    engine = RAGEngine()
    
    print("\n" + "="*60)
    print(" TESTING RAG ENGINE")
    print("="*60)
    
    test_queries = [
        "What is Microsoft's total revenue?",
        "What are Apple's main products?",
        "Compare cloud services between MSFT and AAPL"
    ]
    
    for query in test_queries:
        print("\n" + "-"*30)
        engine.query(query)
        print("-"*30 + "\n")
        input("Press Enter to continue to next query...")

if __name__ == "__main__":
    main()
