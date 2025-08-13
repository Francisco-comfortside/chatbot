from typing import List, Dict, Any
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
    },
    {
        "type": "function",
        "function": {
            "name": "query_troubleshooting_info",
            "description": "Retrieve troubleshootin information from the database. This could include error codes and other ac troubleshooting related problems.",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {"type": "string", "description": "The user's troubleshooting question"},
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
    prior_messages: List[Dict[str, Any]],
    tool_messages: List[Dict[str, Any]]
) -> str:
    """
    Sends the prior messages + the assistant message with tool_calls
    + the tool response messages, to get the final model response.
    """
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=prior_messages + tool_messages,
        tools=tools,            # optionally include tools here again
        temperature=0.3
    )
    return response.choices[0].message.content