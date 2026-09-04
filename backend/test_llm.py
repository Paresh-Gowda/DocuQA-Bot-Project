from llm_service import get_llm
llm = get_llm()

response = llm.invoke(
    "What is RAG in one sentence?"
)
print(response.content)