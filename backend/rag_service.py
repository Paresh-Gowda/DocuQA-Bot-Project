from langchain_core.prompts import ChatPromptTemplate
from llm_service import get_llm
from pdf_service import load_pdf, split_documents
from vector_service import create_vector_store
def create_rag_chain(pdf_path: str):
    documents = load_pdf(pdf_path)
    chunks = split_documents(documents)
    vector_store = create_vector_store(chunks)
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        """
        You are DocuQA, an AI document assistant.

        Answer the user's question using only the provided document context.
        If the answer cannot be found in the context, say that the information
        is not available in the document.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
    )
    return vector_store, llm, prompt
def ask_question(vector_store, llm, prompt, question: str):
    documents = vector_store.similarity_search(question, k=2)

    context = "\n\n".join(
        document.page_content for document in documents
    )
    formatted_prompt = prompt.invoke({
        "context": context,
        "question": question
    })
    response = llm.invoke(formatted_prompt)
    content = response.content
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict)
        )
    return str(content)