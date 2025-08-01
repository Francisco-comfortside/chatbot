from typing import List, Optional
from langchain_pinecone.vectorstores import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from config import PINECONE_API_KEY, PINECONE_INDEX_NAME, OPENAI_API_KEY, PINECONE_NAMESPACE
from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(
    api_key=PINECONE_API_KEY,
)

index = pc.Index(PINECONE_INDEX_NAME)

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key=OPENAI_API_KEY
)


# Create LangChain Pinecone retriever
vectorstore = PineconeVectorStore(
    index=index, 
    embedding = embedding_model, 
    text_key = "content",
    namespace = PINECONE_NAMESPACE
)

def retrieve_relevant_chunks(query: str, filters: Optional[dict] = None, k: int = 5) -> List[str]:
    print(f"Retrieving chunks for query: {query}")
    openai_client = OpenAI(api_key=OPENAI_API_KEY)

    embedding = openai_client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    ).data[0].embedding
    response = index.query(
        vector=embedding,
        top_k=k,
        include_metadata=True,
        namespace=PINECONE_NAMESPACE,
        filter=filters
    )

    return [
        match for match in response.matches
    ]