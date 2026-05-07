from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from rag_pipeline import build_qa_chain

import shutil
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_docs"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

qa_chain = None


@app.get("/")
def home():

    return {
        "message": "Enterprise RAG Assistant API Running"
    }


@app.post("/upload")
async def upload_files(
    files: list[UploadFile] = File(...)
):

    global qa_chain

    saved_files = []

    for file in files:

        # File validation
        if not file.filename.endswith(
            (".pdf", ".txt")
        ):
            continue

        file_path = os.path.join(
            UPLOAD_DIR,
            file.filename
        )

        # Save file
        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        saved_files.append(file_path)

    # Build RAG pipeline
    qa_chain = build_qa_chain(
        saved_files
    )

    return {
        "message": "Documents uploaded successfully",
        "files": saved_files
    }


@app.post("/ask")
def ask_question(query: dict):

    global qa_chain

    if qa_chain is None:

        return {
            "error": "Please upload documents first"
        }

    try:

        result = qa_chain.invoke({
            "query": query["question"]
        })

        sources = []

        for doc in result[
            "source_documents"
        ]:

            sources.append({
                "content": doc.page_content[:500],
                "metadata": doc.metadata
            })

        return {
            "answer": result["result"],
            "sources": sources
        }

    except Exception as e:

        return {
            "error": str(e)
        }
