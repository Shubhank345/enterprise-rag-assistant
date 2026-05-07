from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from dotenv import load_dotenv

import os

# Load environment variables
load_dotenv()

# Get API Key
groq_api_key = os.getenv("GROQ_API_KEY")


# LOAD DOCUMENTS
def load_documents(files):

    docs = []

    for file_path in files:

        # PDF Files
        if file_path.endswith(".pdf"):

            loader = PyPDFLoader(file_path)

        # TXT Files
        else:

            loader = TextLoader(
                file_path,
                encoding="utf-8"
            )

        loaded_docs = loader.load()

        docs.extend(loaded_docs)

    return docs


# BUILD QA CHAIN
def build_qa_chain(files):

    # Load Documents
    docs = load_documents(files)

    # Text Splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    split_docs = splitter.split_documents(docs)

    # Embedding Model
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Vector Database
    vector_db = FAISS.from_documents(
        split_docs,
        embedding_model
    )

    # Retriever
    retriever = vector_db.as_retriever(
        search_kwargs={"k": 5}
    )

    # Groq LLM
    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name="llama-3.1-8b-instant",
        temperature=0.2
    )

    # QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain
