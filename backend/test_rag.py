from rag_service import create_rag_chain, ask_question
vector_store, llm, prompt = create_rag_chain("sample.pdf")
question = "What is DocuQA designed to do?"
answer = ask_question(
    vector_store,
    llm,
    prompt,
    question
)
print("\n--- QUESTION ---")
print(question)
print("\n--- ANSWER ---")
print(answer)