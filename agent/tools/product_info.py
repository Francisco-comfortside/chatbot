from typing import Optional
from utils.schema import build_filters
from retriever.pinecone_retriever import retrieve_relevant_chunks

def query_product_info(question: str, model_name: Optional[str] = None, model_number: Optional[str] = None) -> dict:
    print("Tool called: query_product_info with filters:")
    filters = build_filters(model_name=model_name, model_number=model_number)
    print(filters)
    chunks = retrieve_relevant_chunks(question, filters)

    contents = [chunk.metadata.get("content", "") for chunk in chunks]
    final_answer = "\n\n".join(contents)
    return {
        "final_answer": final_answer,
        "context_chunks": chunks
    }