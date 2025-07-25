from typing import Optional, Dict

# Metadata fields expected from Pinecone
METADATA_FIELDS = [
    "brand_name",
    "content",
    "content_type",
    "description",
    "document_name",
    "document_type",
    "model_name",
    "model_number",
    "page",
    "section_index",
    "tags",
    "title",
]

def build_filters(
    model_name: Optional[str] = None,
    model_number: Optional[str] = None,
    # error_code: Optional[str] = None
) -> Optional[Dict[str, Dict[str, str]]]:
    
    filters = {}
    if model_name:
        filters["metadata.model_name"] = {"$eq": model_name.title()}
    if model_number:
        filters["metadata.model_number"] = {"$in": model_number.upper()}
    # if model_number:
    #     filters["metadata.error_code"] = {"$eq": error_code}
    return filters or None