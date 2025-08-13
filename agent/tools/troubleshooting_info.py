from typing import Optional
from utils.schema import build_filters
from retriever.pinecone_retriever import retrieve_relevant_chunks

def query_troubleshooting_info(question: str) -> dict:
    print("Tool called: query_troubleshooting_info")
    chunks = retrieve_relevant_chunks(question)

    contents = [chunk.metadata.get("content", "") for chunk in chunks]
    final_answer = "\n\n".join(contents)
    return {
        "final_answer": final_answer,
        "context_chunks": chunks
    }