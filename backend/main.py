import os
import shutil
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_service import create_rag_chain, ask_question
from summary_service import generate_summary
app = FastAPI(title="DocuQA API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
class QuestionRequest(BaseModel):
    question: str
@app.get("/")
def root():
    return {"message": "DocuQA API is running"}
@app.get("/api/health")
def health():
    return {"status": "healthy"}
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
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        vector_store, llm, prompt = create_rag_chain(file_path)
        return {
            "message": "PDF uploaded successfully",
            "file_id": file_id,
            "chunks": len(vector_store.get()["ids"])
        }
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.post("/api/question")
async def ask_document_question(request: QuestionRequest):
    try:
        if not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty."
            )
        pdf_files = os.listdir(UPLOAD_DIR)
        if not pdf_files:
            raise HTTPException(
                status_code=404,
                detail="No uploaded PDF found."
            )
        pdf_path = os.path.join(
            UPLOAD_DIR,
            pdf_files[-1]
        )
        vector_store, llm, prompt = create_rag_chain(pdf_path)
        answer = ask_question(
            vector_store,
            llm,
            prompt,
            request.question
        )
        return {
            "question": request.question,
            "answer": answer
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
@app.post("/api/summary")
async def summarize_document():
    try:
        pdf_files = os.listdir(UPLOAD_DIR)
        if not pdf_files:
            raise HTTPException(
                status_code=404,
                detail="No uploaded PDF found."
            )
        pdf_path = os.path.join(
            UPLOAD_DIR,
            pdf_files[-1]
        )
        summary = generate_summary(pdf_path)
        return {
            "summary": summary
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )