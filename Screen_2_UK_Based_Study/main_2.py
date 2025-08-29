# main_2.py
# Stage 2 screening: "Is a UK study or applied to a UK setting (incl. NHS / England / Wales / Scotland / NI)?"

import os
import time
import argparse
import pandas as pd

from openai_client import create_openai_client, call_gpt_api
from utils_2 import build_user_prompt, safe_json_loads, normalize_result

DEFAULT_INPUT = "data/sample_articles.csv"
DEFAULT_OUTPUT = "data/screen_stage2_uk.csv"
DEFAULT_SYSTEM_PROMPT = "system_prompt_2.txt"
DEFAULT_MODEL = "gpt-4o"

def read_system_prompt(path: str) -> str:
    """Load the system prompt text that defines the screening rule & JSON schema."""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    # ---- 1) CLI args ----
    parser = argparse.ArgumentParser(
        description="Stage 2 screening: UK study / applied to a UK setting"
    )
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Path to input CSV")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Path to output CSV")
    parser.add_argument("--system", default=DEFAULT_SYSTEM_PROMPT, help="Path to system prompt text file")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model name")
    parser.add_argument("--limit", type=int, default=None, help="Process only first N rows (for testing)")
    parser.add_argument("--sleep", type=float, default=0.0, help="Delay (seconds) between API calls")
    args = parser.parse_args()

    # ---- 2) Load data ----
    df = pd.read_csv(args.input)
    if args.limit:
        df = df.head(args.limit)

    # ---- 3) Prep prompt + API client ----
    system_prompt = read_system_prompt(args.system)
    client = create_openai_client()

    results = []

    # ---- 4) Iterate rows ----
    for idx, row in df.iterrows():
        # Required columns in sample_articles.csv
        uid = row["id"]
        title = row.get("Title", "")
        abstract = row.get("Abstract", "")

        # Pass the whole row as metadata (strings only)
        metadata = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}

        # Build per-row user prompt focused on UK setting detection
        user_prompt = build_user_prompt(
            unique_id=uid,
            title=title,
            abstract=abstract,
            metadata=metadata
        )

        # Call GPT
        raw = call_gpt_api(
            client=client,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=args.model
        )

        # Parse & normalize model output
        parsed = safe_json_loads(raw) or {}
        normalized = normalize_result(parsed)
        normalized["Unique_ID"] = uid

        results.append(normalized)

        if args.sleep > 0:
            time.sleep(args.sleep)

    # ---- 5) Merge results back to input ----
    res_df = pd.DataFrame(results)
    merged = df.merge(res_df, on="Unique_ID", how="left")

    # ---- 6) Save ----
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    merged.to_csv(args.output, index=False)
    print(f"✅ Stage 2 screening complete. Wrote: {args.output}")

if __name__ == "__main__":
    main()
