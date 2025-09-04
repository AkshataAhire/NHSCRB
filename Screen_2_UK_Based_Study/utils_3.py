# utils_3.py — Stage 3 helpers: “Occurs in NHS / health & social care / community health settings”

import json
import re
from typing import Dict, Any, Optional

def safe_json_loads(s: str) -> Optional[Dict[str, Any]]:
    """Parse JSON robustly (fallback to first {...} block)."""
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

def _shorten(v: Any, n: int = 4000) -> str:
    if v is None:
        return ""
    s = str(v)
    return s if len(s) <= n else s[:n] + "…"

# A few likely metadata keys to surface if present
HINT_KEYS = (
    "setting","location","context","service","care_level","site","country",
    "organisation","organization","provider","department"
)

def build_user_prompt(unique_id: str, title: str, abstract: str, metadata: Dict[str, Any]) -> str:
    """Build the per-article user prompt emphasizing care setting clues."""
    lines = [f"ARTICLE ID: {unique_id}"]
    if title: lines.append(f"Title: {title}")

    if metadata:
        hints = {k: str(metadata[k])[:200] for k in HINT_KEYS if k in metadata and metadata[k] not in (None, "")}
        if hints:
            lines.append(f"Potential setting hints (raw metadata): {hints}")

    if abstract:
        lines.append("Abstract:")
        lines.append(_shorten(abstract, 4000))

    lines.append(
        "\nTASK: Decide if the study occurs in NHS / Health & Social Care services / Community Health "
        "(incl. hospitals, primary care, clinics, patients' homes). Return STRICT JSON per schema."
    )
    return "\n".join(lines)

# ------------------ FIXED CONTEXT NORMALIZER ------------------

_WORD = lambda pat: re.compile(rf"\b({pat})\b", re.IGNORECASE)

_NHS_PAT = _WORD(r"nhs|nhs\s+trust|foundation\s+trust|ics|icb|ccg")
_SOCIAL_PAT = _WORD(r"health\s*&\s*social\s*care|health\s+and\s+social\s+care|social\s+care|domiciliary\s+care|care\s+home|nursing\s+home")
_COMM_PAT = _WORD(
    r"community|primary\s*care|general\s*practice|gp|family\s*practice|"
    r"hospital|inpatient|outpatient|ambulatory|clinic|ward|accident\s*&?\s*emergency|a&e|ed|icu|nicu|"
    r"maternity|antenatal|postnatal|obstetric|midwif(e|ery)|"
    r"physiotherap(y|ist)|rehab(ilitation)?|"
    r"home\s*care|home\s*health|patients?'?\s*home(s)?|"
    r"dental|dentistr(y|ist)|orthodontic"
)

_VALID = {
    "nhs": "NHS",
    "health & social care": "Health & Social Care",
    "health and social care": "Health & Social Care",
    "social care": "Health & Social Care",
    "community health": "Community Health",
    "not applicable": "Not applicable",
    "unknown": "Unknown",
}

_NOT_APPL_PAT = re.compile(r"^\s*(not\s*applicable|n/?a|none)\s*$", re.IGNORECASE)

def _normalize_detected_context(v: Any) -> str:
    """Map free-text context to canonical labels with safe word-boundary matching and priority."""
    if v is None:
        return "Unknown"
    s = str(v).strip()

    # exact labels first
    key = s.lower()
    if key in _VALID:
        return _VALID[key]

    # explicit "Not applicable"
    if _NOT_APPL_PAT.match(s):
        return "Not applicable"

    # priority: NHS > Health & Social Care > Community Health
    if _NHS_PAT.search(s):
        return "NHS"
    if _SOCIAL_PAT.search(s):
        return "Health & Social Care"
    if _COMM_PAT.search(s):
        return "Community Health"

    return "Unknown"

# -------------------------------------------------------------

def _clamp_conf(x: Any) -> float:
    try:
        v = float(x)
    except Exception:
        return 0.0
    return 0.0 if v < 0 else 1.0 if v > 1 else v

def normalize_result(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map model JSON -> Stage 3 columns.
      include_stage3, reason_stage3, detected_context, confidence_stage3
    Safety: if detected_context is 'Not applicable' or 'Unknown', force include=False.
    """
    include = bool(obj.get("include", False))
    reason = str(obj.get("reason", ""))[:250]
    detected_context = _normalize_detected_context(obj.get("detected_context", "Unknown"))
    confidence = _clamp_conf(obj.get("confidence", 0.0))

    if detected_context in {"Not applicable", "Unknown"}:
        include = False

    return {
        "include_stage3": include,
        "reason_stage3": reason,
        "detected_context": detected_context,
        "confidence_stage3": confidence,
    }
