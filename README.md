# 🤖 DocuQA

DocuQA is an AI-powered document assistant that allows users to upload PDF documents, generate concise summaries, and ask questions about their documents. It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from uploaded documents before generating answers, making it easier to understand and interact with large documents.

The application is built with React and CSS on the frontend and Python, FastAPI, and LangChain on the backend. PDF documents are processed using PyPDF, split into smaller chunks, converted into embeddings using Hugging Face Sentence Transformers, and stored in Chroma for semantic search. Google Gemini is used as the language model to generate document-based summaries and answers.

DocuQA also supports multiple uploaded documents with document history, document selection, metadata tracking, and document deletion. The project demonstrates the implementation of an end-to-end RAG pipeline, combining document processing, vector search, embeddings, and an LLM into a practical AI application.