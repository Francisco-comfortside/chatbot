from typing import Optional, Dict


def build_filters(
    model_name: Optional[str] = None,
    model_number: Optional[str] = None,
) -> Optional[Dict[str, Dict[str, str]]]:
    
    filters = {}
    if model_name:
        filters["model_name"] = {"$in": [model_name]}
    if model_number:
        filters["model_number"] = {"$in": [model_number]}
    return filters or None