import os
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from document_service import (
    add_document,
    get_document,
    load_documents,
    delete_document
)
from rag_service import create_rag_chain, get_rag_chain, ask_question
from vector_service import delete_vector_store
from summary_service import generate_summary
app = FastAPI(title="DocuQA API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_DIR = "uploads"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
os.makedirs(UPLOAD_DIR, exist_ok=True)
class QuestionRequest(BaseModel):
    question: str
    file_id: str
class SummaryRequest(BaseModel):
    file_id: str
@app.get("/")
def root():
    return {
        "message": "DocuQA API is running"
    }
@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }
@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )
    file_id = str(uuid.uuid4())
    file_path = os.path.join(
        UPLOAD_DIR,
        f"{file_id}.pdf"
    )
    try:
        file_size = 0
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                file_size += len(chunk)
                if file_size > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="PDF file is too large. Maximum size is 10 MB."
                    )
                buffer.write(chunk)
        vector_store, llm, prompt, pages, chunk_count = create_rag_chain(
            file_path,
            file_id
        )
        add_document(
            file_id=file_id,
            filename=file.filename or "uploaded_document.pdf",
            pages=pages,
            chunks=chunk_count
        )
        return {
            "message": "PDF uploaded successfully.",
            "file_id": file_id,
            "filename": file.filename or "uploaded_document.pdf",
            "pages": pages,
            "chunks": chunk_count
        }
    except HTTPException:
        if os.path.exists(file_path):
            os.remove(file_path)

        raise
    except Exception:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=500,
            detail="Failed to process PDF."
        )
    finally:
        await file.close()
@app.get("/api/documents")
async def get_documents():
    return list(load_documents().values())
@app.get("/api/documents/{file_id}")
async def get_single_document(file_id: str):
    document = get_document(file_id)
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )
    return document
@app.delete("/api/documents/{file_id}")
async def remove_document(file_id: str):
    document = get_document(file_id)
    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )
    file_path = os.path.join(
        UPLOAD_DIR,
        f"{file_id}.pdf"
    )
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        delete_vector_store(file_id)
        delete_document(file_id)
        return {
            "message": "Document deleted successfully."
        }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to delete document."
        )
@app.post("/api/question")
async def question(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )
    file_path = os.path.join(
        UPLOAD_DIR,
        f"{request.file_id}.pdf"
    )
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Document file not found."
        )
    try:
        vector_store, llm, prompt = get_rag_chain(
            request.file_id
        )
        answer = ask_question(
            vector_store,
            llm,
            prompt,
            request.question
        )
        return {
            "answer": answer
        }
    except Exception as e:
        error_message = str(e)
        if (
            "RESOURCE_EXHAUSTED" in error_message
            or "429" in error_message
        ):
            raise HTTPException(
                status_code=429,
                detail="AI service quota exceeded. Please try again later."
            )
        raise HTTPException(
            status_code=500,
            detail="Failed to generate an answer."
        )
@app.post("/api/summary")
async def summary(request: SummaryRequest):
    file_path = os.path.join(
        UPLOAD_DIR,
        f"{request.file_id}.pdf"
    )
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Document file not found."
        )
    try:
        result = generate_summary(file_path)
        return {
            "summary": result
        }
    except Exception as e:
        error_message = str(e)
        if (
            "RESOURCE_EXHAUSTED" in error_message
            or "429" in error_message
        ):
            raise HTTPException(
                status_code=429,
                detail="AI service quota exceeded. Please try again later."
            )
        raise HTTPException(
            status_code=500,
            detail="Failed to generate summary."
        )