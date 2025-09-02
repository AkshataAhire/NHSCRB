# utils_5.py — Stage 5 helpers: “Uses comparison group AND measures primary outcomes (cost/impact)”

import json
from typing import Dict, Any, Optional, List

def safe_json_loads(s: str) -> Optional[Dict[str, Any]]:
    """Parse JSON robustly, falling back to the first {...} block."""
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

HINT_KEYS = (
    "design","method","methods","study_type","trial","arm","arms",
    "comparator","control","intervention","outcomes","endpoint","endpoints",
    "primary_outcome","secondary_outcome","measure","metrics"
)

def _shorten(v: Any, n: int = 4000) -> str:
    if v is None:
        return ""
    s = str(v)
    return s if len(s) <= n else s[:n] + "…"

def build_user_prompt(unique_id: str, title: str, abstract: str, metadata: Dict[str, Any]) -> str:
    """Build user prompt emphasizing design/comparator/outcomes clues."""
    lines = [f"ARTICLE ID: {unique_id}"]
    if title:
        lines.append(f"Title: {title}")

    if metadata:
        hints = {k: str(metadata[k])[:200] for k in HINT_KEYS if k in metadata and metadata[k] not in (None, "")}
        if hints:
            lines.append(f"Potential design/outcome hints (raw metadata): {hints}")

    if abstract:
        lines.append("Abstract:")
        lines.append(_shorten(abstract, 4000))

    lines.append(
        "\nTASK: Decide if the study uses a comparison group AND measures primary cost/impact outcomes. "
        "Return STRICT JSON per schema."
    )
    return "\n".join(lines)

# --- Normalization helpers ---

def _norm_bool(x: Any) -> bool:
    if isinstance(x, bool):
        return x
    s = str(x).strip().lower()
    return s in {"true","1","yes","y"}

_COMPARATOR_MAP = {
    "usual": "Usual/Standard care", "standard": "Usual/Standard care",
    "bau": "BAU", "business as usual": "BAU",
    "no intervention": "No intervention/Do nothing", "do nothing": "No intervention/Do nothing",
    "placebo": "Placebo", "control": "Other", "comparator": "Other",
    "active": "Active comparator"
}

def _normalize_comparator(v: Any) -> str:
    if v is None:
        return "Unknown"
    s = str(v).lower()
    for k, mapped in _COMPARATOR_MAP.items():
        if k in s:
            return mapped
    return "Other" if s and s != "unknown" else "Unknown"

_ALLOWED_OUTCOMES = {"cost","qaly","clinical","utilization","time","safety","pro","impact","other"}

def _normalize_outcomes(v: Any) -> List[str]:
    if v is None:
        return []
    if isinstance(v, list):
        items = [str(x).lower().strip() for x in v]
    else:
        items = [str(v).lower().strip()]
    # tokenize on commas if needed
    norm = []
    for item in items:
        for token in [t.strip() for t in item.split(",") if t.strip()]:
            norm.append(token)
    # map common synonyms
    mapped = []
    for t in norm:
        if "qaly" in t or "utility" in t:
            mapped.append("qaly")
        elif "cost" in t or "economic" in t or "budget" in t:
            mapped.append("cost")
        elif "readmission" in t or "admission" in t or "utilization" in t or "throughput" in t or "use" in t:
            mapped.append("utilization")
        elif "length of stay" in t or "los" in t or "time" in t:
            mapped.append("time")
        elif "mortality" in t or "morbidity" in t or "clinical" in t or "effectiveness" in t or "efficacy" in t:
            mapped.append("clinical")
        elif "safety" in t or "adverse" in t:
            mapped.append("safety")
        elif "prom" in t or "pro" in t or "hrqol" in t or "quality of life" in t:
            mapped.append("pro")
        elif "impact" in t or "effect" in t or "outcome" in t:
            mapped.append("impact")
        else:
            mapped.append("other")
    # keep only allowed, dedupe preserving order
    out = []
    for t in mapped:
        if t in _ALLOWED_OUTCOMES and t not in out:
            out.append(t)
    return out

def _clamp_conf(x: Any) -> float:
    try:
        v = float(x)
    except Exception:
        return 0.0
    return 0.0 if v < 0 else 1.0 if v > 1 else v

def normalize_result(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map model JSON -> Stage-4 columns.
      include_stage4, reason_stage4, has_comparator, detected_comparator,
      has_primary_outcomes, detected_outcomes, confidence_stage4

    Safety: require BOTH has_comparator and has_primary_outcomes to be True; else include=False.
    """
    include = bool(obj.get("include", False))
    reason = str(obj.get("reason", ""))[:250]

    has_comparator = _norm_bool(obj.get("has_comparator", False))
    detected_comparator = _normalize_comparator(obj.get("detected_comparator", "Unknown"))

    has_primary_outcomes = _norm_bool(obj.get("has_primary_outcomes", False))
    detected_outcomes = _normalize_outcomes(obj.get("detected_outcomes", []))

    confidence = _clamp_conf(obj.get("confidence", 0.0))

    if not (has_comparator and has_primary_outcomes):
        include = False

    return {
        "include_stage4": include,
        "reason_stage4": reason,
        "has_comparator": has_comparator,
        "detected_comparator": detected_comparator,
        "has_primary_outcomes": has_primary_outcomes,
        "detected_outcomes": detected_outcomes,
        "confidence_stage4": confidence,
    }
