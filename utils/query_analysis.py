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
# MODEL_NUMBER_PATTERN = r"\bCH-?[a-zA-Z0-9]{3,}\b"
KNOWN_MODEL_NUMBERS = 'CH-RHP18-230VO, CH-RH18MCT', 'CH-RES24-230VO, CH-R24MOLVWM-230VI', 'CH-RHP24-230VO, CH-RS24MDT-HS', 'CH-RHP09-230VO, CH-RSH09-12MCT', 'CH-RES24-230VO, CH-PRO24MASTWM-230VI', 'CH-RES18-230VO, CH-R18MOLVWM-230VI', 'CH-PRO18MASTWM-230VI', 'CH-RHP24-230VO, CH-PRO24MASTWM-230VI', 'CH-PQ24-230VO, CH-PQ24AHU', 'CH-RHP48LCU-230VO, CH-RS48LCDT-HS', 'CH-RHP12-230VO, CH-RS06-12MDT- MS', 'CH-RLS06MIA-115VO, CH-RLS06MIA-115VI', 'CH-RHP33-230VO, CH-RH33HASTWM-230VI', 'CH-RHP24-230VO, CH-RH24MASTWM-230VI', 'CH-RVHP28M-230VO (Non-ducted)', 'CH-RH06MASTWM-230VI', 'CH-RHP09-230VO, CH-RSH06-12MCT1W', 'CH-R60MES-230VO', 'CH-RHP36LCU-230VO, CH-RS36LCDT-HS', 'CH-R48MES-230VO non', 'CH-RHP48M-230VO (Non-ducted)', 'CH-RH24MASTWM-230VI', 'CH-RHP09-230VO, CH-RS06-12MDT- MS', 'CH-PQ18-230VO, CH-PQ18AHU', 'CH-RHP12-230VO, CH-RH12MASTWM-230VI', 'CH-RH09MASTWM-230VI', 'CH-RHP48LCU-230VO, CH-RH48LCCT', 'CH-RES09-115VO, CH-R09OLVWM-115VI', 'CH-PRO12MASTWM-230VI', 'CH-PQ55-230VO, CH-PQ55AHU', 'CH-RVHP55M-230VO (Non-ducted)', 'CH-R36LCU-230VO, CH-RSH36LCCT', 'CH-RHP19M-230VO (Non-ducted)', 'CH-PQ48-230VO, CH-PQ48AHU', 'CH-R28MES-230VO non', 'CH-RVHP36M-230VO (Non-ducted)', 'CH-REL30-230VO, CH-R30MELVWM-230VI', 'CH-RHP24-230VO, CH-RH24MCT', 'CH-REL30-230VO, CH-PRO30MASTWM-230VI', 'CH-R36MES-230VO, Non-ducted', 'CH-PQ36-230VO, CH-PQ36AHU', 'CH-RHP60LCU-230VO, CH-RS60LCDT-HS', 'CH-RLS09MIA-230VO, CH-RLS09MIA-230VI', 'CH-RVHP28M-230VO (Ducted)', 'CH-RHP33-230VO, CH-PRO33HASTWM-230VI', 'CH-REL30-230VO, CH-RH30MASTWM-230VI', 'CH-RHP18-230VO, CH-PRO18MASTWM-230VI', 'CH-R60LCU-230VO, CH-RSH60LCFC', 'CH-RHP19M-230VO (Ducted)', 'CH-RVHP48M-230VO (Non-ducted)', 'CH-RES18-230VO, CH-RSH18MCT', 'CH-RES24-230VO, CH-RSH24MCT', 'CH-RLS09MIA-115VO, CH-RLS09MIA-115VI', 'CH-R48LCU-230VO, CH-RH48LCCT', 'CH-RES12-230VO, CH-RSH09-12MCT', 'CH-RLS12MIA-230VO, CH-RLS12MIA-230VI', 'CH-RHP09-230VO, CH-RH09MASTWM-230VI', 'CH-RES24-230VO, CH-RH24MCT', 'CH-RES24-230VO, CH-RH24MASTWM-230VI', 'CH-RVHP19M-230VO (Ducted)', 'CH-RVHP55M-230VO (Ducted)', 'CH-RES12-230VO, CH-RH12MASTWM-230VI', 'CH-RHP48M-230VO (Ducted)', 'CH-RES12-230VO, CH-RSH06-12MCT1W', 'CH-RES18-230VO, CH-PRO18MASTWM-230VI', 'CH-R60LCU-230VO, CH-RS60LCDT-HS', 'CH-RHP60LCU-230VO, CH-RS60LCAHU', 'CH-RLS12MIA-115VO, CH-RLS12MIA-115VI', 'CH-REL36-230VO, CH-RH36MASTWM-230VI', 'CH-RVHP48M-230VO (Ducted)', 'CH-RHP36M-230VO (Ducted)', 'CH-PQ33-230VO, CH-PQ33AHU', 'CH-RHP18-230VO, CH-RS18MAHU', 'CH-PRO06MASTWM-230VI', 'CH-RHP55M-230VO (Non-ducted)', 'CH-RES18-230VO, CH-RS18MDT-MS', 'CH-REL36-230VO, CH-PRO36MASTWM-230VI', 'CH-PRO24MASTWM-230VI', 'CH-RES09-230VO, CH-RS06-12MDT- MS', 'CH-RES24-230VO, CH-RS24MDT-HS', 'CH-R60MES-230VO non', 'CH-RHP09-230VO, CH-PRO09MASTWM-230VI', 'CH-RES12-230VO, CH-RS06-12MDT- MS', 'CH-RES09-230VO, CH-RH09MASTWM-230VI', 'CH-RVHP36M-230VO (Ducted)', 'CH-RHP06F9-230VO, CH-RSH06-12MCT1W', 'CH-RHP18-230VO, CH-RS18MDT-MS', 'CH-RHP12-230VO, CH-RH12MCT', 'CH-RHP09-230VO, CH-RH09MCT', 'CH-RES12-230VO, CH-RH12MCT', 'CH-RES12-230VO, CH-R12MOLVWM-230VI', 'CH-RES12-230VO, CH-PRO12MASTWM-230VI', 'CH-RHP36LCU-230VO, CH-RSH36LCCT', 'CH-RHP28M-230VO (Non-ducted)', 'CH-RES09-230VO, CH-RSH06-12MCT1W', 'CH-R48MES-230VO', 'CH-R18MES-230VO non', 'CH-PRO09MASTWM-230VI', 'CH-RHP48LCU-230VO, CH-RSH48LCCT', 'CH-RES18-230VO, CH-RH18MCT', 'CH-RHP12-230VO, CH-RSH06-12MCT1W', 'CH-RH18MASTWM-230VI', 'CH-RHP36LCU-230VO, CH-RH36LCCT', 'CH-RHP18-230VO, CH-RH18MASTWM-230VI', 'CH-R28MES-230VO', 'CH-REL36-230VO, CH-R36MELVWM-230VI', 'CH-R36MES-230VO', 'CH-RVHP19M-230VO (Non-ducted)', 'CH-R48LCU-230VO, CH-RSH48LCCT', 'CH-RHP55M-230VO (Ducted)', 'CH-RES18-230VO, CH-RSH18MCT1W', 'CH-RLS24MIA-230VO, CH-RLS24MIA-230VI', 'CH-RHP12-230VO, CH-RSH09-12MCT', 'CH-RES18-230VO, CH-RH18MASTWM-230VI', 'CH-RHP28M-230VO (Ducted)', 'CH-RES09-230VO, CH-PRO09MASTWM-230VI', 'CH-RES09-230VO, CH-RH09MCT', 'CH-RHP24-230VO, CH-RSH24MCT', 'CH-RHP36LCU-230VO, CH-RS36LCAHU', 'CH-RES12-115VO, CH-R12OLVWM-115VI', 'CH-RHP18-230VO, CH-RSH18MCT', 'CH-R36LCU-230VO, CH-RH36LCCT', 'CH-RES09-230VO, CH-R09MOLVWM-230VI', 'CH-RES09-230VO, CH-RSH09-12MCT', 'CH-R36LCU-230VO, CH-RS36LCDT-HS', 'CH-R18MES-230VO', 'CH-RH12MASTWM-230VI', 'CH-RHP06F9-230VO, CH-PRO06MASTWM-230VI', 'CH-R48LCU-230VO, CH-RS48LCDT-HS', 'CH-RHP18-230VO, CH-RSH18MCT1W', 'CH-RHP06F9-230VO, CH-RS06-12MDT- MS', 'CH-RHP36M-230VO (Non-ducted)'


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
    text_upper = text.upper()
    for model in KNOWN_MODELS:
        pattern = re.escape(model.upper())
        if re.search(rf'\b{pattern}\b', text_upper):
            return model
    return None

def analyze_query(user_input: str, memory: list) -> Dict[str, Optional[str]]:
    """
    Analyzes the query and returns intent and filtering info.
    """

    # Simple pre-check for error codes and model names
    error_code = extract_error_code(user_input)
    model_name = extract_model_name(user_input)
    model_number = extract_model_number(user_input)

    # Look for model name, model number and error code in memory
    for turn in reversed(memory):
        if not model_name and turn.get("model_name"):
            model_name = turn["model_name"]
        if not model_number and turn.get("model_number"):
            model_number = turn["model_number"]
        if not error_code and turn.get("error_code"):
            error_code = turn["error_code"]
        if model_name and model_number and error_code:
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
        "model_number": model_number
    }