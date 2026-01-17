Finance RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot for answering questions about financial data from SEC filings of 35 major technology companies.
The system runs entirely locally with no API costs.

Overview

This project indexes SEC 10-K and 10-Q filings and allows users to ask natural-language questions about company financials, risks, and business segments. Answers are generated using a local large language model with retrieval from a vector database to ensure responses are grounded in source documents.

Example questions:

What is NVIDIA's total revenue?

Compare cloud services between Microsoft and Oracle.

What are Tesla's main risk factors?

Key Features

Semantic search across SEC filings using vector embeddings

Coverage of 35 large technology companies

Multiple interaction methods:

Command-line chatbot

REST API built with FastAPI

Web interface built with Streamlit

Source-aware answers with SEC filing references

Fully local execution with no external API calls

Docker support for reproducible deployment

Tech Stack
Component	Technology
Language Model	Llama 3.1 8B (Ollama)
Embeddings	E5-Large-v2 (1024 dimensions)
Vector Database	ChromaDB
Backend	FastAPI
Frontend	Streamlit
Data Source	SEC EDGAR API
Language	Python 3.13
Project Structure
```
finance-rag-chatbot/
│
├── data/
│   ├── raw_filings/          # Downloaded SEC HTML filings (excluded from repo)
│   ├── processed/            # Cleaned and chunked documents
│   └── vector_db/            # ChromaDB persistence
│
├── src/
│   ├── config.py             # Configuration parameters
│   ├── data_collector.py     # SEC filing downloader
│   ├── document_processor.py # HTML cleaning and chunking
│   ├── vector_store.py       # Embedding generation and storage
│   ├── rag_engine.py         # Retrieval and generation logic
│   ├── chatbot.py            # CLI interface
│   ├── api.py                # FastAPI backend
│   └── app.py                # Streamlit web UI
│
├── Dockerfile.api
├── Dockerfile.streamlit
├── docker-compose.yml
├── requirements.txt
└── README.md
```
Getting Started
Prerequisites

macOS or Linux or windows

Python 3.13 or higher

Ollama installed

Clone the Repository
git clone https://github.com/rajeshe6/finance-rag-chatbot.git
cd finance-rag-chatbot

Set Up the Environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

Install Ollama and Pull the Model
ollama pull llama3.1:8b

Download SEC Filings
python3 src/data_collector.py


By default, this runs in test mode for a small subset of companies.
To download all filings, enable the full download section in data_collector.py.

Process the Documents
python3 src/document_processor.py


This step:

Removes HTML and boilerplate text

Chunks documents into overlapping segments

Extracts metadata such as company and filing type

Build the Vector Store
python3 src/vector_store.py


This step generates embeddings and stores them in ChromaDB.
Initial embedding generation may take time depending on hardware.

Running the Application
CLI Chatbot
python3 src/chatbot.py

Web Application

Start the API:

python3 src/api.py


Start the Streamlit UI:

streamlit run src/app.py


Open the browser at:

http://localhost:8501

Docker Deployment
docker-compose build
docker-compose up -d


Ollama must be running on the host machine, not inside Docker.

Example Interaction
User: What is Apple's total revenue?
Bot: According to Apple's 10-K filing, total revenue for fiscal year 2025 was $416.2 billion.

User: Compare cloud services between Microsoft and Oracle.
Bot: Microsoft's Intelligent Cloud segment reported $106.3B in revenue, while Oracle's cloud services segment showed continued growth driven by OCI adoption.

Dataset Details

Companies: 35 large technology firms

Filing types: 10-K and 10-Q

Total filings: 140

Total chunks: Approximately 7,000+

Vector store size varies based on filing length

Configuration

Key parameters can be adjusted in src/config.py:

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
TOP_K_RESULTS = 5
EMBEDDING_MODEL = "intfloat/e5-large-v2"
LLM_MODEL = "llama3.1:8b"

API Documentation

Once the API is running:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Available endpoints:

GET  /           Health check
POST /query      Query SEC filings
GET  /companies  List indexed companies
GET  /stats      Vector database statistics

What This Project Demonstrates

Practical implementation of Retrieval-Augmented Generation

Semantic search using vector databases

Large document processing and chunking strategies

Running modern LLMs locally without external APIs

Building production-style APIs with FastAPI

Creating interactive data applications with Streamlit

Containerized deployment with Docker

Future Improvements

Support for additional SEC filing types

Date-based and filing-type filters

Exportable chat history

Structured comparison tables and visualizations

Multi-turn conversational memory

Retrieval tuning based on query intent

Cloud deployment options

Authentication and user management

License

This project is licensed under the MIT License.

Contact

Rajesh Easwaramoorthy

rajeshe969@gmail.com

https://www.linkedin.com/in/rajeshe6/


Project repository:

https://github.com/rajeshe6/finance-rag-chatbot
