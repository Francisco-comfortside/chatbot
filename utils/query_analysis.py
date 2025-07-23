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

    # Simple pre-check for error codes
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
        "Decide if this is a greeting, a complete support question, or missing info.\n"
        "Extract model name and model number if present.\n"
        "Return JSON with:\n"
        "- intent: greeting | support_question | unknown\n"
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



# KNOWN_MODELS = {
#     "astoria", "astoria pro", "olivia", "peaq", "air handler unit", "ahu",
#     "ceiling cassette", "four-way ceiling cassette", "one way cassette",
#     "high static slim duct", "medium static slim duct",
#     "floor ceiling console", "mia", "outdoor multi-zone hyper", "outdoor multi-zone regular"
# }

# ERROR_CODE_PATTERN = r'\b(E|P|F)?\d{2,3}\b'

# def analyze_query(user_input: str, chat_history: list[dict]) -> Tuple[bool, bool, str, str]:
#     """
#     Analyze whether RAG is needed, whether it's an error code lookup,
#     and extract model name and number if present.
#     """

#     # 1. Detect if the input is an error code lookup
#     error_codes = re.findall(ERROR_CODE_PATTERN, user_input.upper())
#     error_code_only = bool(error_codes)

#     if error_code_only:
#         return True, True, None, None  # Only need to RAG on error code, no filters

#     # 2. Detect model number (e.g. CH-18LMIA-O)
#     model_number = None
#     tokens = re.findall(r'\b[A-Z]{2,4}-\d{2,4}[A-Z]*-?O?\b', user_input.upper())
#     for t in tokens:
#         if t.endswith("O"):  # Only count if it's an Outdoor unit
#             model_number = t
#             break

#     # 3. Detect model name from known list
#     lower_input = user_input.lower()
#     model_name = None
#     for name in KNOWN_MODELS:
#         if name in lower_input:
#             model_name = name.title()
#             break

#     # 4. Use OpenAI function calling to determine intent
#     product_query_tool = {
#         "type": "function",
#         "function": {
#             "name": "should_query_product_database",
#             "description": "Determine whether the database query should be made, ONLY IF the user has provided BOTH a clear product-related request AND either a valid model name or a model number.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "should_query": {"type": "boolean", "description": "Whether to query"},
#                     "reason": {"type": "string", "description": "Why this decision"},
#                     "follow_up": {"type": "string", "description": "Question to ask the user"},
#                 },
#                 "required": ["should_query", "reason"]
#             }
#         }
#     }
#     analysis_prompt = (
#         f"User query: {user_input}\n\n"
#         "Decide if this is a greeting, a complete support question, or missing info.\n"
#         "Extract model name and model number if present.\n"
#         "Return JSON with:\n"
#         "- intent: greeting | support_question | unknown\n"
#         "- model_name (if any)\n"
#         "- model_number (if any)\n"
#     )
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "system", "content": SYSTEM_PROMPT}]
#                  + chat_history
#                  + [{"role": "user", "content": user_input}],
#         tools=[product_query_tool],
#         tool_choice={"type": "function", "function": {"name": "should_query_product_database"}}
#     )

#     tool_call = response.choices[0].message.tool_calls[0]
#     args = json.loads(tool_call.function.arguments)
#     should_query = args.get("should_query", False)

#     return should_query, False, model_name, model_number
    