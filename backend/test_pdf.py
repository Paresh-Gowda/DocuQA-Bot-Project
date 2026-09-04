from pdf_service import load_pdf, split_documents
pdf_path = "sample.pdf"
documents = load_pdf(pdf_path)
chunks = split_documents(documents)
print(f"Pages loaded: {len(documents)}")
print(f"Chunks created: {len(chunks)}")
for chunk in chunks[:3]:
    print("\n--- CHUNK ---")
    print(chunk.page_content[:500])