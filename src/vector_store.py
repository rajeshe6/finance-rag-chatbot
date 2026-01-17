from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import json
from tqdm import tqdm
from typing import List, Dict
import time

from config import (
    PROCESSED_DATA_DIR, 
    VECTOR_DB_DIR, 
    EMBEDDING_MODEL
)

class VectorStoreManager:
    
    def __init__(self):
        print(" Initializing Vector Store Manager...")
        
        print(f" Loading embedding model: {EMBEDDING_MODEL}")
        print(" First time will take 2-3 minutes to download...")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        print(" Embedding model loaded!")
        
        print(f" Initializing ChromaDB at: {VECTOR_DB_DIR}")
        self.client = chromadb.PersistentClient(
            path=str(VECTOR_DB_DIR),
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.collection_name = "sec_filings"
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"description": "SEC 10-K and 10-Q filings"}
        )
        print(f" Collection '{self.collection_name}' ready!")
    
    def generate_embedding(self, text: str) -> List[float]:
        prefixed_text = f"passage: {text}"
        embedding = self.embedding_model.encode(prefixed_text)
        return embedding.tolist()
    
    def load_processed_chunks(self) -> List[Dict]:
        chunks_file = PROCESSED_DATA_DIR / "processed_chunks.json"
        
        if not chunks_file.exists():
            print(f" No processed chunks found at {chunks_file}")
            return []
        
        with open(chunks_file, 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        
        print(f" Loaded {len(chunks)} chunks")
        return chunks
    
    def add_chunks_to_vectorstore(self, chunks: List[Dict], batch_size: int = 10):
        print(f"\n{'='*60}")
        print(" Creating Embeddings & Storing in Vector DB")
        print(f"{'='*60}\n")
        
        total_chunks = len(chunks)
        
        for i in tqdm(range(0, total_chunks, batch_size), desc="Processing batches"):
            batch = chunks[i:i + batch_size]
            
            ids = []
            texts = []
            embeddings = []
            metadatas = []
            
            for idx, chunk in enumerate(batch):
                chunk_id = f"{chunk['metadata']['ticker']}_{chunk['metadata']['filing_type']}_{i+idx}"
                
                ids.append(chunk_id)
                texts.append(chunk['text'])
                
                embedding = self.generate_embedding(chunk['text'])
                embeddings.append(embedding)
                
                metadata = {
                    'ticker': chunk['metadata']['ticker'],
                    'filing_type': chunk['metadata']['filing_type'],
                    'accession_number': chunk['metadata']['accession_number'],
                    'chunk_id': str(chunk['metadata']['chunk_id']),
                    'filename': chunk['metadata']['filename']
                }
                metadatas.append(metadata)
            
            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )
            
            time.sleep(0.1)
        
        total_docs = self.collection.count()
        print(f"\n{'='*60}")
        print(" VECTOR STORE SUMMARY")
        print(f"{'='*60}")
        print(f" Chunks embedded and stored: {total_chunks}")
        print(f" Total documents in DB: {total_docs}")
        print(f" Database location: {VECTOR_DB_DIR}")
        print(f"{'='*60}\n")
    
    def test_query(self, query: str, n_results: int = 3):
        print(f"\n Testing query: '{query}'")
        
        query_embedding = self.embedding_model.encode(f"query: {query}").tolist()
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        print(f"\n Top {n_results} results:")
        for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
            print(f"\n--- Result {i} ---")
            print(f"Company: {metadata['ticker']}")
            print(f"Filing: {metadata['filing_type']}")
            print(f"Text: {doc[:200]}...")

def main():
    manager = VectorStoreManager()
    
    chunks = manager.load_processed_chunks()
    
    if not chunks:
        print(" No chunks to process!")
        return
    
    manager.add_chunks_to_vectorstore(chunks)
    
    print("\n" + "="*60)
    print(" TESTING VECTOR STORE")
    print("="*60)
    manager.test_query("What is the total revenue?")
    manager.test_query("Cloud computing services")
    
    print("\n Vector store setup complete!")

if __name__ == "__main__":
    main()
