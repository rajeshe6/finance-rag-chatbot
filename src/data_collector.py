from sec_edgar_downloader import Downloader
from pathlib import Path
import time
from tqdm import tqdm
from config import RAW_DATA_DIR, TECH_COMPANIES, FILING_TYPES

class SECDataCollector:
    
    def __init__(self, company_name="FinanceRAGBot", email="your.email@example.com"):
        self.downloader = Downloader(company_name, email, str(RAW_DATA_DIR))
        print(f" SEC Downloader initialized")
        print(f" Download location: {RAW_DATA_DIR}")
    
    def download_company_filings(self, ticker, filing_type="10-K", num_filings=3):
        try:
            print(f"\n Downloading {num_filings} {filing_type} filings for {ticker}...")
            
            self.downloader.get(
                filing_type,
                ticker,
                limit=num_filings,
                download_details=True
            )
            
            print(f" {ticker} {filing_type} downloaded successfully!")
            return True
            
        except Exception as e:
            print(f" Error downloading {ticker} {filing_type}: {str(e)}")
            return False
    
    def download_all_companies(self, num_filings_per_type=2):
        print(f"\n{'='*60}")
        print(f" Starting download for {len(TECH_COMPANIES)} companies")
        print(f" Filing types: {FILING_TYPES}")
        print(f" Filings per type: {num_filings_per_type}")
        print(f"{'='*60}\n")
        
        total_downloads = len(TECH_COMPANIES) * len(FILING_TYPES)
        successful = 0
        failed = 0
        
        with tqdm(total=total_downloads, desc="Overall Progress") as pbar:
            for ticker in TECH_COMPANIES:
                for filing_type in FILING_TYPES:
                    success = self.download_company_filings(
                        ticker, 
                        filing_type, 
                        num_filings_per_type
                    )
                    
                    if success:
                        successful += 1
                    else:
                        failed += 1
                    
                    pbar.update(1)
                    
                    time.sleep(0.5)
        
        print(f"\n{'='*60}")
        print(f" DOWNLOAD SUMMARY")
        print(f"{'='*60}")
        print(f" Successful: {successful}/{total_downloads}")
        print(f" Failed: {failed}/{total_downloads}")
        print(f" Files saved to: {RAW_DATA_DIR}")
        print(f"{'='*60}\n")

def main():
    collector = SECDataCollector(
        company_name="FinanceRAGBot",
        email="rajeshvirgome@gmail.com"  
    )
    
    print("\n FULL MODE: Downloading all 35 tech companies")
    print(" Total filings to download: ~140 (2 per filing type per company)")
    print("\n You can press Ctrl+C to cancel anytime\n")
    
    response = input("Continue? (yes/no): ").strip().lower()
    
    if response not in ['yes', 'y']:
        print("\n Download cancelled")
        return
    
    collector.download_all_companies(num_filings_per_type=2)
    
    print("\n Full download complete!")
    print(f" Check your files: {RAW_DATA_DIR}")
    
    
if __name__ == "__main__":
    main()
