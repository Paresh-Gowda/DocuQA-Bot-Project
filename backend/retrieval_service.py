def retrieve_documents(vector_store, question: str):
    results = vector_store.similarity_search(
        question,
        k=2
    )
    return results