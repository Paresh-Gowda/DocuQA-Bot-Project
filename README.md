# 🤖 DocuQA

DocuQA is an AI-powered document assistant that allows users to upload PDF documents, generate summaries, and ask questions about their documents. The project is designed to make it easier to understand and interact with information from large documents.

The frontend has been completed using React, including the PDF upload interface, summary section, chat interface, styling, and footer. The backend has been set up using Python, FastAPI, and LangChain, with PDF extraction, text chunking, Hugging Face embeddings, Chroma vector storage, semantic retrieval, and Gemini LLM integration implemented and tested.

The next phase is to combine these components into an end-to-end RAG pipeline and connect the backend APIs with the React frontend. This will make PDF uploading, document summarization, and question answering fully functional.