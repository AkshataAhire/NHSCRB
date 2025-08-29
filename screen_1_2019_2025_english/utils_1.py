import json
from typing import Dict, Any, Optional

def safe_json_loads(s: str) -> Optional[Dict[str, Any]]:
    """
    Safely parse JSON from the model output string.

    Why this exists:
    - Sometimes the model adds extra text before/after the JSON.
    - This function first tries to load the full string.
    - If that fails, it tries to extract the first {...} block.
    - Returns None if no valid JSON object is found.
    """
    if not s:
        return None
    s = s.strip()
    try:
        return json.loads(s)
    except Exception:
        # Try to extract substring between first '{' and last '}'
        start, end = s.find("{"), s.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(s[start:end+1])
            except Exception:
                return None
    return None


def build_user_prompt(unique_id: str, year: Any, title: str, abstract: str) -> str:
    """
    Construct the user prompt string that is sent to the model for one article.

    Args:
        unique_id: Unique identifier for the article (used to track results).
        year: Declared publication year (if available).
        title: Article title.
        abstract: Article abstract text.

    Returns:
        str: Formatted text containing metadata + task instructions.
    """
    lines = []
    lines.append(f"ARTICLE ID: {unique_id}")
    if year:
        lines.append(f"Declared year: {year}")
    if title:
        lines.append(f"Title: {title}")
    if abstract:
        lines.append(f"Abstract: {abstract}")  # could truncate if abstracts are very long

    # Append task instructions (schema defined in system_prompt.txt)
    lines.append(
        "\nTASK: Determine if the article is in English and published 2019–2025, "
        "return STRICT JSON per schema."
    )
    return "\n".join(lines)


def normalize_result(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Standardize and clean the model's JSON response into consistent fields.

    Args:
        obj: Raw parsed JSON dictionary from the model.

    Returns:
        dict: Normalized dictionary with guaranteed keys:
            - include_stage1 (bool)
            - reason_stage1 (short justification)
            - detected_language (string)
            - publication_year (int or None)
            - confidence_stage1 (float)
    """
    return {
        "include_stage1": bool(obj.get("include", False)),
        "reason_stage1": str(obj.get("reason", ""))[:250],  # cap to 250 chars
        "detected_language": str(obj.get("detected_language", "Unknown")),
        "publication_year": obj.get("publication_year", None),
        "confidence_stage1": obj.get("confidence", 0.0)
    }
