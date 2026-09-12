import json
import os
from datetime import datetime
DOCUMENTS_FILE = "documents.json"
def load_documents():
    if not os.path.exists(DOCUMENTS_FILE):
        return {}
    with open(DOCUMENTS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
def save_documents(documents):
    with open(DOCUMENTS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            documents,
            file,
            indent=4
        )
def add_document(
    file_id,
    filename,
    pages,
    chunks
):
    documents = load_documents()
    documents[file_id] = {
        "file_id": file_id,
        "filename": filename,
        "pages": pages,
        "chunks": chunks,
        "uploaded_at": datetime.now().isoformat()
    }
    save_documents(documents)
def get_document(file_id):
    documents = load_documents()
    return documents.get(file_id)
def delete_document(file_id):
    documents = load_documents()
    if file_id in documents:
        del documents[file_id]
        save_documents(documents)
        return True
    return False