import re
from typing import Dict, Optional, Tuple
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from config import SYSTEM_PROMPT, OPENAI_MODEL, OPENAI_API_KEY
import json

KNOWN_MODEL_NAMES = ['Universal Floor Ceiling', 'Regular Multi-Zone', 'Smart Wired Thermostat(120)', 'Universal Remote With Humidity Sensor', 'Smart Thermostat', 'PEAQ Air Handler Unit', 'One Way Cassette', 'Mini Floor Console', 'Auxiliary Heater', 'Smart Kit', 'PEAQ Air Handler Outdoor Unit', 'Olivia', 'Hyper Multi-Zone', 'Olivia Midnight', 'Universal Remote Without Humidity Control', 'Floor Ceiling', 'Astoria', 'Ceilling Cassette', 'Slim Duct (High Static)', 'slim duct', 'Ceiling Cassette', 'Universal Remote With Humidity Control', 'Slim Duct (Medium Static)', 'PEAQ Auxiliary Heater', 'Multi-Zone Outdoor Unit', 'Astoria Pro', 'Multi-Position Air Handler Unit', 'Air Handler Unit', 'Slim Duct', 'MIA NY', 'PEAQ']
KNOWN_MODEL_NUMBERS = ['CH-R09MOLVWM-230VI', 'CH-RHP48LCU-230VO', 'CH-RHP48LCU-230VO, CH-RH48LCCT', 'CH-RH12MASTWM-230VI', 'CH-RSH18MFC', 'CH-RSH06-12MCT1W\n(Dip Switch 9)', 'CH-RS18MAHU', 'CH-PQ48-230VO, CH-PQ48AHU', 'CH-RSH06-12MCT1W\n(Dip Switch 12)', 'CH-R12MOLVWM-230VI', 'CH-RLS24MIA-230VI', 'CH-R48MES-230VO non', 'CH-R60LCU-230VO', 'CH-R60MES-230VO non', 'CH-RB09MOLVWM-230VI', 'CH-RVHP55M-230VO (Non-ducted)', 'CH-PQ36-230VO', 'CH-RES09-230VO, CH-RH09MASTWM-230VI', 'CH-RHP06F9-230VO', 'CH-RHP36M-230VO (Non-ducted)', 'CH-RS12MDT-MS', 'CH-PQ18-230VO, CH-PQ18AHU', 'CH-R36LCU-230VO, CH-RSH36LCCT', 'CH-RS24MDT-HS', 'CH-RHP18-230VO, CH-RS18MAHU', 'CH-RES18-230VO, CH-RSH18MCT1W', 'CH-RHP09-230VO, CH-RH09MCT', 'CH-RES12-230VO, CH-RSH09-12MCT', 'CH-RHP18-230VO', 'CH-RS36LCDT-HS', 'CH-RSH09-12MCT\n(Dip Switch 9)', 'CH-RB24MOLVWM-230VI', 'CH-R36LCU-230VO', 'CH-RES18-230VO, CH-RH18MCT', 'CH-R48LCU-230VO', 'CH-RES09-115VO', 'CH-PRO09MASTWM-230VI', 'CH-PQ55-230VO, CH-PQ55AHU', 'CH-RH09MASTWM-230VI', 'CH-RES09-230VO, CH-RSH09-12MCT', 'CH-RES18-230VO, CH-R18MOLVWM-230VI', 'CH-RES09-230VO, CH-RS06-12MDT- MS', 'CH-RES12-230VO, CH-RS06-12MDT- MS', 'CH-RES18-230VO, CH-RH18MASTWM-230VI', 'CH-PRO12MASTWM-230VI', 'CH-R24MOLVWM-230VI', 'CH-RES18-230VO, CH-PRO18MASTWM-230VI', 'CH-RS09MDT-MS', 'CH-RSH24MCT', 'CH-RS48LCAHU', 'CH-PRO15MASTWM-230V', 'CH-RHP12-230VO, CH-RH12MCT', 'CH-RVHP28M-230VO', 'CH-R36LCU-230VO, CH-RH36LCCT', 'CH-PRO33HASTWM-230VI', 'CH-RHP12-230VO, CH-RS06-12MDT- MS', 'CH-RLS09MIA-115VO', 'CH-R36MELVWM-230VI', 'CH-PQ48AHU', 'CH-RHP12-230VO, CH-RSH09-12MCT', 'CH-PQ18-230VO', 'CH-RES24-230VO, CH-R24MOLVWM-230VI', 'CH-RLS06MIA-115VI', 'CH-RHP06F9-230VO, CH-RSH06-12MCT1W', 'CH-RLS12MIA-115VI', 'CH-PQ24-230VO, CH-PQ24AHU', 'CH-RES24-230VO, CH-RSH24MCT', 'CH-RB12OLVWM-115VI', 'CH-RS48LCDT-HS', 'CH-R48MES-230VO', 'CH-R18MOLVWM-230VI', 'CH-RS60LCDT-HS', 'CH-RSH16MMC', 'CH-RHP28M-230VO (Ducted)', 'CH-PQ36-230VO, CH-PQ36AHU', 'CH-R48LCU-230VO, CH-RS48LCDT-HS', 'CH-RHP24-230VO, CH-PRO24MASTWM-230VI', 'CH-RLS18MIA-230VO', 'CH-RHP36M-230VO (Ducted)', 'CH-R60LCU-230VO, CH-RSH60LCFC', 'CH-R36MES-230VO, Non-ducted', 'CH-PRO36MAST-\nWM-230VI', 'CH-RVHP55M-230VO', 'CH-RES24-230VO, CH-RH24MASTWM-230VI', 'CH-RHP24-230VO, CH-RSH24MCT', 'CH-PRO30MASTWM-230VI', 'CH-RES12-230VO, CH-PRO12MASTWM-230VI', 'CH-RHP09-230VO', 'CH-RES12-230VO, CH-RH12MCT', 'CH-PQ18AHU', 'CH-RLS12MIA-230VO, CH-RLS12MIA-230VI', 'CH-RHP48LCU-230VO, CH-RS48LCDT-HS', 'CH-RHP12-230VO', 'CH-RHP12-230VO, CH-RH12MASTWM-230VI', 'CH-RH15MASTWM-230VI', 'CH-RHP18-230VO, CH-RH18MASTWM-230VI', 'CH-RHP15-230VO', 'CH-RHP36LCU-230VO', 'CH-RHP06F9-230VO, CH-PRO06MASTWM-230VI', 'CH-RSH06-12MCT1W\n(Dip Switch 6)', 'CH-RHP09-230VO, CH-RSH09-12MCT', 'CH-RES12-115VO, CH-R12OLVWM-115VI', 'CH-RES18-230VO, CH-RS18MDT-MS', 'CH-RES09-230VO, CH-R09MOLVWM-230VI', 'CH-RSH09MMC', 'CH-PQ33-230VO', 'CH-R18MES-230VO', 'CH-REL36-230VO, CH-R36MELVWM-230VI', 'CH-RES12-230VO, CH-RSH06-12MCT1W', 'CH-R06MOLVWM-230VI', 'CH-RHP19M-230VO (Non-ducted)', 'CH-RES24-230VO, CH-RS24MDT-HS', 'CH-RSH48LCCT', 'CH-RLS12MIA-115VO, CH-RLS12MIA-115VI', 'CH-RHP12-230VO, CH-RSH06-12MCT1W', 'CH-R60LCU-230VO, CH-RS60LCDT-HS', 'CH-RHP18-230VO, CH-RS18MDT-MS', 'CH-RSH60LCFC', 'CH-RVHP36M-230VO (Ducted)', 'CH-RHP55M-230VO (Ducted)', 'CH-RLS12MIA-230VI', 'CH-REL30-230VO', 'CH-RVHP28M-230VO (Non-ducted)', 'CH-RLS09MIA-230VO, CH-RLS09MIA-230VI', 'CH-RES09-230VO', 'CH-RES06-115VO', 'CH-RHP06F9-230VO, CH-RS06-12MDT- MS', 'CH-RS60LCAHU', 'CH-RHP33-230VO, CH-RH33HASTWM-230VI', 'CH-PQ55AHU', 'CH-RLS09MIA-230VI', 'CH-R60MES-230VO', 'CH-RS36LCAHU', 'CH-RHP18-230VO, CH-PRO18MASTWM-230VI', 'CH-RHP36LCU-230VO, CH-RS36LCAHU', 'CH-R33HOLVWM-230VI', 'CH-RSH09-12MCT\n(Dip Switch 12)', 'CH-RSH18MCT', 'CH-RLS06MIA-115VO, CH-RLS06MIA-115VI', 'CH-RHP36LCU-230VO, CH-RS36LCDT-HS', 'CH-RVHP48M-230VO (Non-ducted)', 'CH-RES24-230VO', 'CH-RVHP19M-230VO (Ducted)', 'CH-PRO24MASTWM-230VI', 'CH-RES12-115VO', 'CH-RSH18MCT1W', 'CH-RLS24MIA-230VO, CH-RLS24MIA-230VI', 'CH-RHP48LCU-230VO, CH-RSH48LCCT', 'CH-RS24MAHU', 'CH-RHP18-230VO, CH-RSH18MCT1W', 'CH-RH33HASTWM-230VI', 'CH-RES09-115VO, CH-R09OLVWM-115VI', 'CH-RVHP48M-230VO', 'CH-R12OLVWM-115VI', 'CH-RSH24MFC', 'CH-PQ24AHU', 'CH-RES12-230VO, CH-RH12MASTWM-230VI', 'CH-RES09-230VO, CH-RH09MCT', 'CH-RLS12MIA-230VO', 'CH-RHP19M-230VO (Ducted)', 'CH-RHP09-230VO, CH-PRO09MASTWM-230VI', 'CH-RLS18MIA-230VI', 'CH-RVHP36M-230VO', 'CH-RHP28M-230VO (Non-ducted)', 'CH-PQ48-230VO', 'CH-RH36MASTWM-230VI', 'CH-RB06MOLVWM-230VI', 'CH-RLS24MIA-230VO', 'CH-RH24MASTWM-230VI', 'CH-R28MES-230VO', 'CH-REL36-230VO', 'CH-RHP24-230VO, CH-RH24MASTWM-230VI', 'CH-R28MES-230VO non', 'CH-RVHP19M-230VO', 'CH-RHP36LCU-230VO, CH-RSH36LCCT', 'CH-RHP33-230VO', 'CH-PRO06MASTWM-230VI', 'CH-R48LCU-230VO, CH-RH48LCCT', 'CH-RB18MOLVWM-230VI', 'CH-PRO18MASTWM-230VI', 'CH-PQ33-230VO, CH-PQ33AHU', 'CH-RLS09MIA-115VI', 'CH-RH06MASTWM-230VI', 'CH-RES09-230VO, CH-RSH06-12MCT1W', 'CH-RES12-230VO', 'CH-PQ36AHU', 'CH-PQ24-230VO', 'CH-RB12MOLVWM-230VI', 'CH-RES24-230VO, CH-RH24MCT', 'CH-RVHP28M-230VO (Ducted)', 'CH-RES09-230VO, CH-PRO09MASTWM-230VI', 'CH-RS06MDT-MS', 'CH-RES12-230VO, CH-R12MOLVWM-230VI', 'CH-REL36-230VO, CH-RH36MASTWM-230VI', 'CH-RHP24-230VO, CH-RS24MDT-HS', 'CH-REL30-230VO, CH-PRO30MASTWM-230VI', 'CH-REL36-230VO, CH-PRO36MASTWM-230VI', 'CH-RVHP19M-230VO (Non-ducted)', 'CH-RES18-230VO, CH-RSH18MCT', 'CH-R18MES-230VO non', 'CH-RHP09-230VO, CH-RSH06-12MCT1W', 'CH-RHP60LCU-230VO', 'CH-RHP36LCU-230VO, CH-RH36LCCT', 'CH-RVHP55M-230VO (Ducted)', 'CH-RVHP36M-230VO (Non-ducted)', 'CH-RHP18-230VO, CH-RSH18MCT', 'CH-R36LCU-230VO, CH-RS36LCDT-HS', 'CH-R06OLVWM-115VI', 'CH-PQ33AHU', 'CH-RHP09-230VO, CH-RS06-12MDT- MS', 'CH-PQ55-230VO', 'CH-RVHP48M-230VO (Ducted)', 'CH-RHP48M-230VO (Non-ducted)', 'CH-RHP24-230VO', 'CH-RHP55M-230VO (Non-ducted)', 'CH-RHP60LCU-230VO, CH-RS60LCAHU', 'CH-RH18MASTWM-230VI', 'CH-RSH36LCFC', 'CH-RHP24-230VO, CH-RH24MCT', 'CH-R30MELVWM-230VI', 'CH-RH30MASTWM-230VI', 'CH-RS30MAHU', 'CH-RSH36LCCT', 'CH-R09OLVWM-115VI', 'CH-RSH48LCFC', 'CH-RES18-230VO', 'CH-R36MES-230VO', 'CH-RHP18-230VO, CH-RH18MCT', 'CH-RHP48M-230VO (Ducted)', 'CH-RSH12MMC', 'CH-RHP60LCU-230VO, CH-RS60LCDT-HS', 'CH-RLS12MIA-115VO', 'CH-RLS09MIA-230VO', 'CH-RLS09MIA-115VO, CH-RLS09MIA-115VI', 'CH-RHP09-230VO, CH-RH09MASTWM-230VI', 'CH-RHP33-230VO, CH-PRO33HASTWM-230VI', 'CH-REL30-230VO, CH-R30MELVWM-230VI', 'CH-R48LCU-230VO, CH-RSH48LCCT', 'CH-RLS06MIA-115VO', 'CH-RB09OLVWM-115VI', 'CH-RES24-230VO, CH-PRO24MASTWM-230VI', 'CH-RS18MDT-MS', 'CH-REL30-230VO, CH-RH30MASTWM-230VI']
llm = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model=OPENAI_MODEL,
    temperature=0,
)

def extract_model_name(text: str) -> Optional[str]:
    text_upper = text.upper()
    for model in KNOWN_MODEL_NAMES:
        pattern = re.escape(model.upper())
        if re.search(rf'\b{pattern}\b', text_upper):
            return model
    return None

def extract_model_number(text: str) -> Optional[str]:
    text_upper = text.upper()
    for model in KNOWN_MODEL_NUMBERS:
        pattern = re.escape(model.upper())
        if re.search(rf'\b{pattern}\b', text_upper):
            return model
    return None

def analyze_query(user_input: str, memory: list) -> Dict[str, Optional[str]]:
    """
    Analyzes the query and returns intent and filtering info.
    """        
    # Simple pre-check for error codes and model names
    model_name = extract_model_name(user_input)
    model_number = extract_model_number(user_input)

    # Look for model name, model number and error code in memory
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
        "Decide if this is a social interaction (includes greetings, farewells, pleasantries, small talk, etc.), a complete support question, or a query that is missing information.\n"
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

    print("intent: ", parsed.get("intent"))
    print("model name: ", model_name)
    # Merge with pre-extracted values    
    return {
        "intent": parsed.get("intent", "unknown"),
        "model_name": model_name,
        "model_number": model_number
    }