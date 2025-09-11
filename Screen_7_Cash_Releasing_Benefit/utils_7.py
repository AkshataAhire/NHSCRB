# utils_7.py — Stage 7 helpers: “Explicit cash-releasing saving / positive ROI”

import json
import re
from typing import Dict, Any, Optional, List

# -------------------- Robust JSON loader --------------------

def safe_json_loads(s: str) -> Optional[Dict[str, Any]]:
    """Parse JSON robustly, falling back to the first {...} block (if needed)."""
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

# -------------------- Cue detection --------------------

# Only patterns that imply explicit, cash-releasing savings / positive ROI
# (intentionally narrow and high-precision)
_CASH_SAVING_CUES = {
    r"\bin[- ]year cost saving(s)?\b": "in_year_cost_saving",
    r"\bin[- ]year negative net budget impact\b": "in_year_negative_net_budget_impact",
    r"\bnegative net budget impact\b": "negative_net_budget_impact",
    r"\b(net|overall|total)\s+saving(s)?\b": "net_saving",
    r"\bexpenditure reduction(s)?\b": "expenditure_reduction",
    r"\bcash[- ]releasing saving(s)?\b": "cash_releasing_saving",
    r"\bbudget impact:\s*negative\b": "negative_budget_impact_colon_form",
    r"\b(net|budget)\s*benefit(s)?\b": "net_or_budget_benefit",  # keep; often used synonymously with net saving
    r"\b(costs?\s*(avoided|reduced|lower(ed)?)\s*(with|vs|versus)\s*[A-Za-z].*)\b": "comparative_cost_reduction_phrase"
}

def _find_cues(text: Any, patterns: Dict[str, str], max_hits: int = 12) -> List[str]:
    """Return a small set of cue labels present in text (case-insensitive). NaN-safe."""
    if not isinstance(text, str) or not text:
        return []
    hits: List[str] = []
    low = text.lower()
    for pat, label in patterns.items():
        try:
            if re.search(pat, low):
                hits.append(label)
                if len(hits) >= max_hits:
                    break
        except re.error:
            # ignore malformed regex at runtime
            continue
    # dedupe preserving order
    out: List[str] = []
    for h in hits:
        if h not in out:
            out.append(h)
    return out

def _shorten(v: Any, n: int = 4000) -> str:
    if v is None:
        return ""
    s = str(v)
    return s if len(s) <= n else s[:n] + "…"

# -------------------- Prompt builder --------------------

def build_user_prompt(unique_id: str, title: Any, abstract: Any, metadata: Dict[str, Any]) -> str:
    """
    Build the user prompt for Stage 7.
    Very focused: only asks the model to judge whether the article explicitly demonstrates
    cash-releasing saving / positive ROI using the allowed phrasings.
    """
    title = title if isinstance(title, str) else ""
    abstract = abstract if isinstance(abstract, str) else ""

    lines = [f"ARTICLE ID: {unique_id}"]
    if title:
        lines.append(f"Title: {title}")

    # Provide the abstract (shortened if huge)
    if abstract:
        lines.append("Abstract:")
        lines.append(_shorten(abstract, 4000))

        # Surface detected cues to guide the model
        cues = _find_cues(abstract, _CASH_SAVING_CUES)
        if cues:
            lines.append(f"\nDetected cash-saving cues: {sorted(set(cues))}")

    # Stage-7 rule recap + strict schema
    lines.append(
        "\nDECISION RULE (Stage 7): INCLUDE only if the article explicitly demonstrates "
        "cash-releasing saving or positive ROI using language such as:\n"
        "- in-year cost saving\n"
        "- in-year negative net budget impact\n"
        "- negative net budget impact\n"
        "- net saving / net benefit\n"
        "- expenditure reduction\n"
        "- cash-releasing saving\n\n"
        "EXCLUDE if the article only reports cost-effectiveness (ICER/QALY), efficiency, utilisation, "
        "or clinical outcomes without explicit cash-releasing saving.\n"
        "If unclear/ambiguous, EXCLUDE.\n"
    )
    lines.append(
        "Return STRICT JSON only:\n"
        "{\n"
        '  "include": true | false,\n'
        '  "reason": "short one-line justification",\n'
        '  "cash_saving_terms": ["net saving","expenditure reduction"] | [],\n'
        '  "confidence": 0.0-1.0\n'
        "}"
    )
    return "\n".join(lines)

# -------------------- Normalization --------------------

def _clamp_conf(x: Any) -> float:
    try:
        v = float(x)
    except Exception:
        return 0.0
    return 0.0 if v < 0 else 1.0 if v > 1 else v

_ALLOWED_TERM_LABELS = {
    "in_year_cost_saving",
    "in_year_negative_net_budget_impact",
    "negative_net_budget_impact",
    "net_saving",
    "expenditure_reduction",
    "cash_releasing_saving",
    "negative_budget_impact_colon_form",
    "net_or_budget_benefit",
    "comparative_cost_reduction_phrase",
}

_CANONICAL_TERM_MAP = {
    "in_year_cost_saving": "in-year cost saving",
    "in_year_negative_net_budget_impact": "in-year negative net budget impact",
    "negative_net_budget_impact": "negative net budget impact",
    "net_saving": "net saving",
    "expenditure_reduction": "expenditure reduction",
    "cash_releasing_saving": "cash-releasing saving",
    "negative_budget_impact_colon_form": "negative net budget impact",
    "net_or_budget_benefit": "net benefit",
    "comparative_cost_reduction_phrase": "comparative cost reduction",
}

def normalize_result(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Map model JSON -> Stage-7 columns.
      include_stage7, reason_stage7, cash_saving_terms, confidence_stage7

    Safety: we only accept include=True as provided by the model; we do NOT infer it.
    We still clamp confidence and sanitize terms.
    """
    include = bool(obj.get("include", False))
    reason = str(obj.get("reason", ""))[:240]

    terms_in = obj.get("cash_saving_terms", [])
    if isinstance(terms_in, str):
        terms_in = [terms_in]
    terms_norm: List[str] = []
    # Normalize both known labels and free-text
    for t in terms_in or []:
        t_low = str(t).strip().lower()
        # If it's one of our internal labels, map to canonical phrase
        if t_low in _ALLOWED_TERM_LABELS:
            can = _CANONICAL_TERM_MAP.get(t_low, t_low)
            if can not in terms_norm:
                terms_norm.append(can)
        else:
            # Otherwise keep the free-text phrase (e.g., “net saving”, “expenditure reduction”)
            if t_low and t_low not in terms_norm:
                terms_norm.append(t_low)

    confidence = _clamp_conf(obj.get("confidence", 0.0))

    return {
        "include_stage7": include,
        "reason_stage7": reason,
        "cash_saving_terms": terms_norm,
        "confidence_stage7": confidence,
    }
