import os
import shutil
import uuid
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from rag_service import create_rag_chain, ask_question
app = FastAPI(title="DocuQA API")
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