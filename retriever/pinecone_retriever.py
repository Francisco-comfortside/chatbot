from typing import List, Optional
# from langchain_community.vectorstores import Pinecone as lang_cone
from langchain_pinecone import PineconeVectorStore
# from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
from config import PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME, OPENAI_API_KEY, PINECONE_NAMESPACE
from pinecone import Pinecone, ServerlessSpec
import os

pc = Pinecone(
    api_key=PINECONE_API_KEY,
    # environment=os.getenv("PINECONE_ENVIRONMENT")
)

index = pc.Index(PINECONE_INDEX_NAME)

embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)


# Create LangChain Pinecone retriever
vectorstore = PineconeVectorStore(
    index=index, 
    embedding = embedding_model, 
    text_key = "content",
    namespace = PINECONE_NAMESPACE
)

def retrieve_relevant_chunks(query: str, filters: Optional[dict] = None, k: int = 3) -> List[str]:
    """
    Returns the top-k relevant content strings matching the query.
    Applies metadata filters if provided.
    """
    results = vectorstore.similarity_search(
        query=query,
        k=k,
        filter=filters if filters else None
    )
    return [r.page_content for r in results]