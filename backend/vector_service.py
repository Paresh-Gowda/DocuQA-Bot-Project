from langchain_chroma import Chroma
from embedding_service import get_embeddings
def create_vector_store(chunks, collection_name):
    embeddings = get_embeddings()
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_name=collection_name
    )
    return vector_store
def get_vector_store(collection_name):
    embeddings = get_embeddings()
    vector_store = Chroma(
        persist_directory="./chroma_db",
        collection_name=collection_name,
        embedding_function=embeddings
    )
    return vector_store
def delete_vector_store(collection_name):
    vector_store = get_vector_store(collection_name)
    vector_store.delete_collection()