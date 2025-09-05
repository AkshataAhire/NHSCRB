# main_7.py — Stage 7: Cash-releasing benefits
# Uses a checklist (5 core criteria + 1 auxiliary phrase flag) and tiered inclusion logic.

import os
import time
import argparse
import pandas as pd

from openai_client import create_openai_client, call_gpt_api
from utils_7 import build_user_prompt, safe_json_loads, normalize_result

# ---- Defaults ----
DEFAULT_INPUT = "data/sample_articles.csv"
DEFAULT_OUTPUT = "data/screen_stage6_cash.csv"
DEFAULT_SYSTEM = "system_prompt_7.txt"
DEFAULT_MODEL = "gpt-4o"

def read_system_prompt(path: str) -> str:
    """Load the system prompt text that defines the checklist and JSON schema."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    # ---- 1. CLI args ----
    parser = argparse.ArgumentParser(description="Stage 7 screening: Cash-releasing benefits")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to input CSV")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path to output CSV")
    parser.add_argument("--system", default=DEFAULT_SYSTEM, help="Path to system prompt file")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model name")
    parser.add_argument("--limit", type=int, default=None, help="Process only first N rows (for testing)")
    parser.add_argument("--sleep", type=float, default=0.0, help="Delay (seconds) between API calls")
    args = parser.parse_args()

    # ---- 2. Load input ----
    df = pd.read_csv(args.input)
    if args.limit:
        df = df.head(args.limit)

    # ---- 3. Prep system prompt + API client ----
    system_prompt = read_system_prompt(args.system)
    client = create_openai_client()

    # Optional runtime behaviour for inclusion rule:
    #   STAGE7_MODE in {"strict", "moderate", "signal"} (default "moderate")
    stage7_mode = os.getenv("STAGE7_MODE", "strict").lower()

    results = []

    # ---- 4. Iterate over rows ----
    for _, row in df.iterrows():
        uid = row["id"]
        title = row.get("Title", "")
        abstract = row.get("Abstract", "")
        # Include full row as metadata if you want to surface hints later (not used directly here)
        metadata = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}

        # Build user prompt
        user_prompt = build_user_prompt(uid, title, abstract, metadata)

        # Call GPT API
        raw = call_gpt_api(
            client=client,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=args.model,
        )

        # Parse + normalize output
        parsed = safe_json_loads(raw) or {}
        normalized = normalize_result(parsed, mode=stage7_mode)
        normalized["id"] = uid

        results.append(normalized)

        if args.sleep > 0:
            time.sleep(args.sleep)

    # ---- 5. Merge results back ----
    res_df = pd.DataFrame(results)
    merged = df.merge(res_df, on="id", how="left")

    # ---- 6. Save ----
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    merged.to_csv(args.output, index=False)
    print(f"Stage 7 screening complete. Wrote: {args.output} (mode={stage7_mode})")

if __name__ == "__main__":
    main()




