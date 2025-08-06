# # from langchain_community.chat_models import ChatOpenAI
# from langchain_openai import ChatOpenAI
# from langchain.schema import HumanMessage, SystemMessage
# from typing import List, Optional
# from config import OPENAI_API_KEY, OPENAI_MODEL, SYSTEM_PROMPT

# llm = ChatOpenAI(
#     openai_api_key=OPENAI_API_KEY,
#     model=OPENAI_MODEL,
#     temperature=0.3,
# )

# def generate_response(
#     user_input: str,
#     context_chunks: Optional[List[str]] = None
# ) -> str:
#     context_text = "\n\n".join(context_chunks) if context_chunks else ""
    
#     prompt = f"""User query: {user_input}"""

#     if context_chunks:
#         prompt = (
#             "You have access to the following reference content:\n\n"
#             f"{context_text}\n\n"
#             "Answer the user's question using this content as support."
#             "\n\n" + prompt
#         )

#     messages = [
#         SystemMessage(content=SYSTEM_PROMPT),
#         HumanMessage(content=prompt)
#     ]

#     response = llm.invoke(messages)
#     return response.content.strip()



# openai_toolcaller.py
import json
from typing import List, Optional, Dict, Any
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

tools = [
    {
        "type": "function",
        "function": {
            "name": "query_product_info",
            "description": "Search technical documentation and manuals for the given question",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The user's support question"},
                    "model_name": {"type": "string", "description": "The name of the product model"},
                    "model_number": {"type": "string", "description": "The number of the product model"}
                },
                "required": ["question"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_warranty_info",
            "description": "Retrieve general warranty policy information from the database. Applies to all products.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The user's warranty question"},
                },
                "required": ["question"]
            }
        }
    }
]


def call_openai_with_tools(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    """Calls OpenAI with tool-calling enabled"""
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.3
    )
    return response.choices[0].message


def followup_with_tool_response(
    prior_messages: List[Dict[str, str]],
    tool_messages: List[Dict[str, str]]
) -> str:
    """
    Feeds multiple tool responses back to OpenAI for final generation.
    Each tool response must include: tool_call_id, name, and content.
    """
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=prior_messages + tool_messages
    )
    return response.choices[0].message.content