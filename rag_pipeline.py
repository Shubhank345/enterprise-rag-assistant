from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

from langchain_ollama import ChatOllama

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA


# LOAD DOCUMENTS
def load_documents(files):

    docs = []

    for file_path in files:

        # PDF FILES
        if file_path.endswith(".pdf"):

            loader = PyPDFLoader(file_path)

        # TEXT FILES
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

    # Load documents
    docs = load_documents(files)

    # Text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    split_docs = splitter.split_documents(docs)

    # Embeddings
    embedding_model = OllamaEmbeddings(
        model="mistral"
    )

    # Vector DB
    vector_db = FAISS.from_documents(
        split_docs,
        embedding_model
    )

    # Retriever
    retriever = vector_db.as_retriever(
        search_kwargs={"k": 5}
    )

    # LLM
    llm = ChatOllama(
        model="mistral",
        temperature=0.2
    )

    # QA Chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain