import re
from typing import Dict, Optional, Tuple
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from config import SYSTEM_PROMPT, OPENAI_MODEL, OPENAI_API_KEY
import json

# Basic error code pattern (e.g., E1, E12, F5)
ERROR_CODE_PATTERN = r"\b[E|F]\d{1,2}\b"
KNOWN_MODELS = [
    "astoria", "astoria pro", "olivia", "peaq", "air handler unit", "ahu",
    "ceiling cassette", "four-way ceiling cassette", "one way cassette",
    "high static slim duct", "medium static slim duct",
    "floor ceiling console", "mia", "outdoor multi-zone hyper", "outdoor multi-zone regular"
]

llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model=OPENAI_MODEL,
    temperature=0,
)

def extract_error_code(text: str) -> Optional[str]:
    match = re.search(ERROR_CODE_PATTERN, text.upper())
    return match.group() if match else None

def extract_model_name(text: str) -> Optional[str]:
    text_upper = text.upper()
    for model in KNOWN_MODELS:
        pattern = re.escape(model.upper())
        if re.search(rf'\b{pattern}\b', text_upper):
            return model
    return None

def extract_model_number(text: str) -> Optional[str]:
    return None

def analyze_query(user_input: str, memory: list) -> Dict[str, Optional[str]]:
    """
    Analyzes the query and returns intent and filtering info.
    """

    # Simple pre-check for error codes and model names
    error_code = extract_error_code(user_input)
    model_name = extract_model_name(user_input)
    
    # Look for model name/number in memory
    model_number = None
    for turn in reversed(memory):
        if not model_name and turn.get("model_name"):
            model_name = turn["model_name"]
        if not model_number and turn.get("model_number"):
            model_number = turn["model_number"]
        if model_name and model_number:
            break

    # Ask the model to classify the request
    system_prompt = "You are an AI that classifies customer support queries."
    analysis_prompt = (
        f"User query: {user_input}\n\n"
        "Decide if this is a social interaction (includes greetings, farewells, pleasantries, small talk, etc.), a complete support question (including mentioning an error code), or a query that is missing information.\n"
        "Extract model name and model number if present.\n"
        "Return JSON with:\n"
        "- intent: social_interaction | support_question | unknown\n"
        "- model_name (if any)\n"
        "- model_number (if any)\n"
        "do not include any markdown in the response. Return only the json object"
    )

    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=analysis_prompt)
    ])

    try:
        parsed = json.loads(response.content)  # LLM returns dict-like JSON
    except Exception:
        parsed = {"intent": "unknown"}

    # Merge with pre-extracted values    
    return {
        "intent": parsed.get("intent", "unknown"),
        "error_code": error_code,
        "model_name": model_name,
        "model_number": parsed.get("model_number") or model_number
    }