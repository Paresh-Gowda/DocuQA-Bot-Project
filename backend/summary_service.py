from langchain_core.prompts import ChatPromptTemplate
from llm_service import get_llm
from pdf_service import load_pdf, split_documents
def generate_summary(pdf_path: str):
    documents = load_pdf(pdf_path)
    chunks = split_documents(documents)
    context = "\n\n".join(
        chunk.page_content for chunk in chunks
    )
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        """
        You are DocuQA, an AI document assistant.

        Summarize the following document clearly and concisely.

        Focus on:
        - Main purpose
        - Important points
        - Key information
        - Useful conclusions

        Do not add information that is not present in the document.

        Document:
        {context}

        Summary:
        """
    )
    formatted_prompt = prompt.invoke({
        "context": context
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