"""
Configuration file for Finance RAG Chatbot
This stores all our settings in one place
"""

import os
from pathlib import Path

# Project Paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw_filings"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
VECTOR_DB_DIR = DATA_DIR / "vector_db"

# Create directories if they don't exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

# Model Configuration
EMBEDDING_MODEL = "intfloat/e5-large-v2"
LLM_MODEL = "llama3.1:8b"
OLLAMA_BASE_URL = "http://localhost:11434"

# Chunking Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval Configuration
TOP_K_RESULTS = 5

# Top 35 Tech Companies
TECH_COMPANIES = [
    "AAPL",   # Apple
    "MSFT",   # Microsoft
    "NVDA",   # NVIDIA
    "GOOGL",  # Alphabet (Google)
    "AMZN",   # Amazon
    "META",   # Meta (Facebook)
    "TSLA",   # Tesla
    "AVGO",   # Broadcom
    "ORCL",   # Oracle
    "ADBE",   # Adobe
    "CRM",    # Salesforce
    "CSCO",   # Cisco
    "ACN",    # Accenture
    "AMD",    # AMD
    "IBM",    # IBM
    "INTU",   # Intuit
    "NOW",    # ServiceNow
    "TXN",    # Texas Instruments
    "QCOM",   # Qualcomm
    "AMAT",   # Applied Materials
    "PANW",   # Palo Alto Networks
    "MU",     # Micron
    "INTC",   # Intel
    "ADI",    # Analog Devices
    "LRCX",   # Lam Research
    "KLAC",   # KLA Corporation
    "SNPS",   # Synopsys
    "CDNS",   # Cadence
    "MCHP",   # Microchip Technology
    "NXPI",   # NXP Semiconductors
    "MRVL",   # Marvell Technology
    "FTNT",   # Fortinet
    "WDAY",   # Workday
    "TEAM",   # Atlassian
    "SNOW",   # Snowflake
]

# SEC Filing Types
FILING_TYPES = ["10-K", "10-Q"]

print("Configuration loaded successfully!")
print(f"Project Root: {PROJECT_ROOT}")
print(f"Data Directory: {DATA_DIR}")
print(f"Companies to track: {len(TECH_COMPANIES)}")