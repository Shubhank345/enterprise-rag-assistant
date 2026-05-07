# Enterprise Multi-Document RAG Assistant

An Enterprise-grade Multi-Document Retrieval-Augmented Generation (RAG) Assistant built using FastAPI, Streamlit, LangChain, FAISS, and Groq.

This application allows users to upload multiple PDF/TXT documents and ask questions using AI-powered semantic search and retrieval.

---

## Features

- Multi-document upload support
- PDF and TXT document processing
- Semantic search using vector embeddings
- Retrieval-Augmented Generation (RAG)
- FastAPI backend
- Streamlit frontend
- FAISS vector database
- Groq LLM integration
- Source document retrieval
- Interactive chatbot interface

---

## Tech Stack

### Frontend
- Streamlit

### Backend
- FastAPI
- Uvicorn

### AI / GenAI
- LangChain
- Groq
- FAISS
- HuggingFace Embeddings

### Programming Language
- Python

---

## Project Architecture

```text
Streamlit Frontend
        ↓
FastAPI Backend
        ↓
LangChain RAG Pipeline
        ↓
FAISS Vector Database
        ↓
GROQ LLM
```

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/enterprise-rag-assistant.git
cd enterprise-rag-assistant
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Linux/Mac

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---


## Run Backend

```bash
uvicorn backend:app --reload
```

Backend runs on:

```text
http://127.0.0.1:8000
```

---

## Run Frontend

Open another terminal:

```bash
streamlit run app.py
```

Frontend runs on:

```text
http://localhost:8501
```

---

## API Documentation

FastAPI Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

## How It Works

1. Upload documents
2. Documents are processed and chunked
3. Embeddings are generated
4. FAISS vector database stores embeddings
5. User asks questions
6. Relevant chunks are retrieved
7. GROQ LLM generates contextual answers

---

## Example Questions

- What is this document about?
- Summarize the uploaded files
- Explain the key concepts
- What technologies are mentioned?

---


## Author

Shubhank Manhas

AI Student | GenAI Developer | FastAPI & RAG Enthusiast

---

