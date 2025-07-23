# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from typing import List, Optional
from config import OPENAI_API_KEY, OPENAI_MODEL, SYSTEM_PROMPT

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model=OPENAI_MODEL,
    temperature=0.3,
)

def generate_response(
    user_input: str,
    context_chunks: Optional[List[str]] = None
) -> str:
    context_text = "\n\n".join(context_chunks) if context_chunks else ""
    
    prompt = f"""User query: {user_input}"""

    if context_chunks:
        prompt = (
            "You have access to the following reference content:\n\n"
            f"{context_text}\n\n"
            "Answer the user's question using this content as support."
            "\n\n" + prompt
        )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt)
    ]

    response = llm.invoke(messages)
    return response.content.strip()