from fastapi import FastAPI
app = FastAPI(title="DocuQA API")
@app.get("/")
def root():
    return {"message": "DocuQA API is running"}
@app.get("/api/health")
def health():
    return {"status": "healthy"}