from pdf_service import load_pdf, split_documents
from vector_service import create_vector_store
documents = load_pdf("sample.pdf")
chunks = split_documents(documents)
vector_store = create_vector_store(chunks)
print("Vector database created successfully!")
print(f"Chunks stored: {len(chunks)}")