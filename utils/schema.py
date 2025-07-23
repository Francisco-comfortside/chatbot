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
    error_code_only: bool = False
) -> Optional[Dict[str, Dict[str, str]]]:
    if error_code_only:
        return None  # No filtering for error code lookups

    filters = {}
    if model_name:
        filters["metadata.model_name"] = {"$eq": model_name}
    if model_number:
        filters["metadata.model_number"] = {"$eq": model_number}
    return filters or None