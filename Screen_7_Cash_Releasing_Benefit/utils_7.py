# utils_6.py — Stage 6 helpers (Cash-releasing benefits with 5 core criteria)

import json
from typing import Dict, Any, Optional

# -----------------------------
# Robust JSON parsing
# -----------------------------
def safe_json_loads(s: str) -> Optional[Dict[str, Any]]:
    """
    Parse a JSON object from a model string response.
    Falls back to extracting the first {...} block if needed.
    """
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


# -----------------------------
# Inclusion logic
# -----------------------------
# Five core criteria + one auxiliary signal
CORE_KEYS = [
    "has_direct_budget_reduction",
    "has_route_to_baseline_removal",
    "has_baseline_and_counterfactual",
    "is_realised_and_sustainable",
    "no_cost_shift_or_harm",
]
AUX_KEY = "cash_releasing_phrase_present"
ALL_KEYS = CORE_KEYS + [AUX_KEY]

def _b(x: Any) -> bool:
    """Coerce to boolean (only literal 'true' -> True)."""
    return str(x).strip().lower() == "true"

def _clamp(p: Any) -> float:
    """Clamp confidence to [0,1]."""
    try:
        v = float(p)
    except Exception:
        return 0.0
    return max(0.0, min(1.0, v))

def derive_include(flags: Dict[str, bool], mode: str = "moderate") -> bool:
    """
    Decide inclusion from flags.

    Modes:
      - strict: require ALL five core criteria True.
      - moderate (default): require
            (has_direct_budget_reduction OR cash_releasing_phrase_present) AND
            (has_route_to_baseline_removal OR has_baseline_and_counterfactual) AND
            no_cost_shift_or_harm
        Rationale: abstracts rarely contain full realisation detail; we still need a credible route and no harm.
      - signal: include if (has_direct_budget_reduction OR cash_releasing_phrase_present)
    """
    cond_cash = flags.get("has_direct_budget_reduction", False) or flags.get(AUX_KEY, False)
    cond_route = flags.get("has_route_to_baseline_removal", False) or flags.get("has_baseline_and_counterfactual", False)
    cond_noharm = flags.get("no_cost_shift_or_harm", False)

    if mode == "strict":
        return all(flags.get(k, False) for k in CORE_KEYS)

    if mode == "signal":
        return cond_cash

    # moderate
    return cond_cash and cond_route and cond_noharm


# -----------------------------
# Prompt builder
# -----------------------------
def build_user_prompt(unique_id: str, title: str, abstract: str, metadata: Dict[str, Any]) -> str:
    """
    Build the per-article user prompt. Keep it compact; abstracts can be long.
    """
    lines = [f"ARTICLE ID: {unique_id}"]
    if title:
        lines.append(f"Title: {title}")
    if abstract:
        lines.append("Abstract:")
        lines.append(str(abstract)[:4000])  # cap to keep token usage sensible

    lines.append("\nTASK: Evaluate cash-releasing benefits per the JSON checklist.")
    return "\n".join(lines)


# -----------------------------
# Normalization
# -----------------------------
def normalize_result(obj: Dict[str, Any], mode: str = "moderate") -> Dict[str, Any]:
    """
    Map GPT JSON -> Stage 4 outputs:
      include_stage4, reason_stage4, cash_release_flags, confidence_stage4
    """
    flags = {k: _b(obj.get(k, False)) for k in ALL_KEYS}
    include = derive_include(flags, mode=mode)
    reason = str(obj.get("reason", ""))[:250]
    confidence = _clamp(obj.get("confidence", 0.0))

    positives = [k for k, v in flags.items() if v]

    return {
        "include_stage4": include,
        "reason_stage4": reason,
        "cash_release_flags": "; ".join(positives),
        "confidence_stage4": confidence,
    }

