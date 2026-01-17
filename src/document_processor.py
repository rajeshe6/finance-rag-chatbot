from pathlib import Path
from bs4 import BeautifulSoup
import re
from typing import List, Dict
from tqdm import tqdm
import json

from config import RAW_DATA_DIR, PROCESSED_DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP

class DocumentProcessor:
    
    def __init__(self):
        print(" Document Processor initialized")
        self.chunk_size = CHUNK_SIZE
        self.chunk_overlap = CHUNK_OVERLAP
    
    def clean_html(self, html_content: str) -> str:
        soup = BeautifulSoup(html_content, 'lxml')
        
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def chunk_text(self, text: str, metadata: Dict) -> List[Dict]:
        chunks = []
        words = text.split()
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk_words = words[i:i + self.chunk_size]
            chunk_text = ' '.join(chunk_words)
            
            if len(chunk_text.strip()) > 100:
                chunk_data = {
                    'text': chunk_text,
                    'metadata': {
                        **metadata,
                        'chunk_id': len(chunks),
                        'start_word': i,
                        'end_word': min(i + self.chunk_size, len(words))
                    }
                }
                chunks.append(chunk_data)
        
        return chunks
    
    def extract_metadata(self, file_path: Path) -> Dict:
        parts = file_path.parts
        
        ticker = parts[-4] if len(parts) >= 4 else "UNKNOWN"
        filing_type = parts[-3] if len(parts) >= 3 else "UNKNOWN"
        accession = parts[-2] if len(parts) >= 2 else "UNKNOWN"
        filename = file_path.name
        
        metadata = {
            'ticker': ticker,
            'filing_type': filing_type,
            'accession_number': accession,
            'filename': filename,
            'source_file': str(file_path)
        }
        
        return metadata
    
    def process_file(self, file_path: Path) -> List[Dict]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            metadata = self.extract_metadata(file_path)
            clean_text = self.clean_html(html_content)
            chunks = self.chunk_text(clean_text, metadata)
            
            return chunks
            
        except Exception as e:
            print(f" Error processing {file_path.name}: {str(e)}")
            return []
    
    def process_all_filings(self) -> List[Dict]:
        print(f"\n{'='*60}")
        print(" Processing SEC Filings")
        print(f"{'='*60}\n")
        
        html_files = list(RAW_DATA_DIR.rglob("*.html"))
        
        if not html_files:
            print(" No HTML files found!")
            print(f" Checked directory: {RAW_DATA_DIR}")
            return []
        
        print(f" Found {len(html_files)} HTML files")
        
        all_chunks = []
        
        for file_path in tqdm(html_files, desc="Processing files"):
            chunks = self.process_file(file_path)
            all_chunks.extend(chunks)
        
        output_file = PROCESSED_DATA_DIR / "processed_chunks.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_chunks, f, indent=2)
        
        print(f"\n{'='*60}")
        print(" PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f" Files processed: {len(html_files)}")
        print(f" Total chunks created: {len(all_chunks)}")
        print(f" Saved to: {output_file}")
        print(f"{'='*60}\n")
        
        return all_chunks

def main():
    processor = DocumentProcessor()
    chunks = processor.process_all_filings()
    
    if chunks:
        print(f" Processing complete! Created {len(chunks)} chunks")
        
        print("\n Sample chunk:")
        print(f"Company: {chunks[0]['metadata']['ticker']}")
        print(f"Filing: {chunks[0]['metadata']['filing_type']}")
        print(f"Text preview: {chunks[0]['text'][:200]}...")
    else:
        print(" No chunks created. Check if files were downloaded correctly.")

if __name__ == "__main__":
    main()
