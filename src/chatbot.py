from rag_engine import RAGEngine
from config import TECH_COMPANIES
import sys

class FinanceChatbot:
    
    def __init__(self):
        print("\n" + "="*60)
        print(" FINANCE RAG CHATBOT")
        print("="*60)
        print("Powered by: Llama 3.1 8B + E5-Large + ChromaDB")
        print("Data: SEC 10-K & 10-Q Filings")
        print("="*60 + "\n")
        
        self.engine = RAGEngine()
        
        print("\n Chatbot ready! Ask me anything about:")
        print("   Company financials (revenue, profits, etc.)")
        print("   Product information")
        print("   Business segments")
        print("   Comparisons between companies")
        print("\n Available companies: AAPL, MSFT (test mode)")
        print("="*60 + "\n")
    
    def display_help(self):
        print("\n" + "="*60)
        print(" HELP - How to use this chatbot")
        print("="*60)
        print("\n BASIC QUERIES:")
        print("  - What is Microsoft's revenue?")
        print("  - Tell me about Apple's products")
        print("  - What are MSFT's operating expenses?")
        
        print("\n COMPANY-SPECIFIC QUERIES:")
        print("  Use @TICKER to filter by company:")
        print("  - @AAPL What is the iPhone revenue?")
        print("  - @MSFT Tell me about cloud services")
        
        print("\n COMPARATIVE QUERIES:")
        print("  - Compare revenue between AAPL and MSFT")
        print("  - How do Apple and Microsoft differ?")
        
        print("\n COMMANDS:")
        print("  - help    : Show this help message")
        print("  - list    : List available companies")
        print("  - clear   : Clear screen")
        print("  - quit    : Exit chatbot")
        print("="*60 + "\n")
    
    def list_companies(self):
        print("\n" + "="*60)
        print(" AVAILABLE COMPANIES (Test Mode: Only AAPL, MSFT)")
        print("="*60)
        print("\nCurrently loaded companies:")
        print("  AAPL - Apple Inc.")
        print("  MSFT - Microsoft Corporation")
        print("\n To add all 35 companies, run the full data download")
        print("="*60 + "\n")
    
    def parse_query(self, user_input: str):
        if '@' in user_input:
            parts = user_input.split('@', 1)
            if len(parts) == 2:
                ticker_and_question = parts[1].split(None, 1)
                if len(ticker_and_question) == 2:
                    ticker = ticker_and_question[0].upper()
                    question = ticker_and_question[1]
                    return question, ticker
        
        return user_input, None
    
    def run(self):
        print(" Type 'help' for commands, 'quit' to exit\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n Goodbye! Thanks for using Finance RAG Chatbot!")
                    break
                
                elif user_input.lower() == 'help':
                    self.display_help()
                    continue
                
                elif user_input.lower() == 'list':
                    self.list_companies()
                    continue
                
                elif user_input.lower() == 'clear':
                    print("\n" * 50)
                    continue
                
                question, ticker = self.parse_query(user_input)
                
                result = self.engine.query(question, ticker=ticker)
                
                print("\n" + "-"*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n Goodbye!")
                break
            
            except Exception as e:
                print(f"\n Error: {str(e)}")
                print("Please try again or type 'help' for assistance.\n")

def main():
    try:
        chatbot = FinanceChatbot()
        chatbot.run()
    except KeyboardInterrupt:
        print("\n\n Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n Failed to initialize chatbot: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
