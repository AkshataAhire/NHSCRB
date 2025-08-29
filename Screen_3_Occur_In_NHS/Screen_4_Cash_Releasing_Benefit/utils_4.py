# utils_4.py — Stage 4 helpers: “Cash-releasing benefits”

import json
from typing import Dict, Any, Optional

def safe_json_loads(s: str) -> Optional[Dict[str, Any]]:
    if not s:
        return None
    s = s.strip()
    try:
        return json.loads(s)
    except Exception:
        start, end = s.find("{"), s.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(s[start:end+1])
            except Exception:
                return None
    return None

def build_user_prompt(unique_id: str, title: str, abstract: str, metadata: Dict[str, Any]) -> str:
    """Build prompt to highlight financial/costing clues."""
    lines = [f"ARTICLE ID: {unique_id}"]
    if title: lines.append(f"Title: {title}")
    if abstract:
        lines.append("Abstract:")
        lines.append(str(abstract)[:4000])

    lines.append(
        "\nTASK: Decide if the intervention described has clear CASH-RELEASING BENEFITS "
        "according to defined criteria (explicit budget reduction, baseline+counterfactual, "
        "sustainable in-year, auditable, no cost shifting). Return STRICT JSON."
    )
    return "\n".join(lines)

def normalize_result(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map GPT JSON → Stage 4 results:
      include_stage4, reason_stage4, cash_release_elements, confidence_stage4
    """
    include = bool(obj.get("include", False))
    reason = str(obj.get("reason", ""))[:250]
    elements = obj.get("cash_release_elements", [])
    if not isinstance(elements, list):
        elements = [str(elements)]
    confidence = float(obj.get("confidence", 0.0))

    if confidence < 0 or confidence > 1:
        confidence = 0.0

    # If elements empty → safer to force exclude
    if not elements or include is False:
        include = False

    return {
        "include_stage4": include,
        "reason_stage4": reason,
        "cash_release_elements": "; ".join(elements),
        "confidence_stage4": confidence,
    }
