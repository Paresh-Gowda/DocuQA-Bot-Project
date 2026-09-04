from embedding_service import get_embeddings
embeddings = get_embeddings()
text = "DocuQA is an AI-powered document assistant."
vector = embeddings.embed_query(text)
print("Embedding generated!")
print("Vector length:", len(vector))
print("First 5 values:", vector[:5])