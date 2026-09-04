from pdf_service import load_pdf, split_documents
from vector_service import create_vector_store
from retrieval_service import retrieve_documents
documents = load_pdf("sample.pdf")
chunks = split_documents(documents)
vector_store = create_vector_store(chunks)
question = "What is DocuQA designed to do?"
results = retrieve_documents(vector_store, question)
print(f"Relevant chunks found: {len(results)}")
for result in results:
    print("\n--- RETRIEVED CHUNK ---")
    print(result.page_content)