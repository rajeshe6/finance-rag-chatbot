import streamlit as st
import requests
from typing import List, Dict
import time

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Finance RAG Chatbot",
    page_icon="",
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .answer-box {
        background-color: #e8f4f8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 5px solid #0068c9;
    }
</style>
""", unsafe_allow_html=True)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'api_healthy' not in st.session_state:
    try:
        response = requests.get(f"{API_URL}/")
        st.session_state.api_healthy = response.status_code == 200
    except:
        st.session_state.api_healthy = False

st.markdown('<div class="main-header"> Finance RAG Chatbot</div>', unsafe_allow_html=True)
st.markdown("---")

with st.sidebar:
    st.header(" Settings")
    
    if st.session_state.api_healthy:
        st.success(" API Connected")
    else:
        st.error(" API Disconnected")
        st.info("Run: `python src/api.py`")
    
    if st.session_state.api_healthy:
        try:
            response = requests.get(f"{API_URL}/companies")
            companies = response.json()['companies']
        except:
            companies = []
    else:
        companies = []
    
    st.subheader(" Company Filter")
    selected_company = st.selectbox(
        "Select a company (optional)",
        ["All Companies"] + companies
    )
    
    n_results = st.slider(
        " Number of sources",
        min_value=3,
        max_value=10,
        value=5
    )
    
    st.subheader(" Database Stats")
    if st.session_state.api_healthy:
        try:
            response = requests.get(f"{API_URL}/stats")
            stats = response.json()
            st.metric("Total Chunks", stats['total_chunks'])
            st.info(f"**LLM:** {stats['llm_model']}")
            st.info(f"**Embeddings:** {stats['embedding_model']}")
        except:
            st.warning("Could not load stats")
    
    if st.button(" Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

st.header(" Chat")

for chat in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(chat['question'])
    
    with st.chat_message("assistant"):
        st.markdown(f'<div class="answer-box">{chat["answer"]}</div>', unsafe_allow_html=True)
        
        with st.expander(" View Sources"):
            for i, source in enumerate(chat['sources'], 1):
                st.markdown(f"""
                <div class="source-box">
                    <strong>Source {i}:</strong> {source['ticker']} - {source['filing_type']}<br>
                    <em>{source['text'][:300]}...</em>
                </div>
                """, unsafe_allow_html=True)

user_question = st.chat_input("Ask a question about SEC filings...")

if user_question:
    if not st.session_state.api_healthy:
        st.error(" API is not running! Start it with: `python src/api.py`")
    else:
        with st.chat_message("user"):
            st.write(user_question)
        
        with st.chat_message("assistant"):
            with st.spinner(" Thinking..."):
                try:
                    ticker = None if selected_company == "All Companies" else selected_company
                    
                    response = requests.post(
                        f"{API_URL}/query",
                        json={
                            "question": user_question,
                            "ticker": ticker,
                            "n_results": n_results
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.markdown(f'<div class="answer-box">{result["answer"]}</div>', unsafe_allow_html=True)
                        
                        with st.expander(" View Sources"):
                            for i, source in enumerate(result['sources'], 1):
                                st.markdown(f"""
                                <div class="source-box">
                                    <strong>Source {i}:</strong> {source['ticker']} - {source['filing_type']}<br>
                                    <em>{source['text'][:300]}...</em>
                                </div>
                                """, unsafe_allow_html=True)
                        
                        st.session_state.chat_history.append({
                            'question': user_question,
                            'answer': result['answer'],
                            'sources': result['sources']
                        })
                    else:
                        st.error(f" Error: {response.status_code}")
                        
                except Exception as e:
                    st.error(f" Error: {str(e)}")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    Powered by Llama 3.1 8B + E5-Large + ChromaDB
</div>
""", unsafe_allow_html=True)
