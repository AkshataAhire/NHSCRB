import os
import time
import argparse
import pandas as pd

# Import helper functions
from openai_client import create_openai_client, call_gpt_api
from utils_1 import build_user_prompt, safe_json_loads, normalize_result

# Default file paths (can be overridden via CLI args)
DEFAULT_INPUT = "data/sample_articles.csv"
DEFAULT_OUTPUT = "data/screen_stage1.csv"
DEFAULT_SYSTEM_PROMPT = "system_prompt_1.txt"

def read_system_prompt(path: str) -> str:
    """
    Load the system prompt text from file.
    The system prompt defines the model's role and instructions.
    """
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    # ---- 1. Parse command line arguments ----
    parser = argparse.ArgumentParser(description="Stage 1 screening: English + 2019–2025")
    parser.add_argument("--input", default=DEFAULT_INPUT, help="Input CSV file with articles")
    parser.add_argument("--output", default=DEFAULT_OUTPUT, help="Output CSV file for results")
    parser.add_argument("--system", default=DEFAULT_SYSTEM_PROMPT, help="System prompt text file")
    parser.add_argument("--model", default="gpt-4o", help="OpenAI model to use")
    parser.add_argument("--limit", type=int, default=None, help="Process only the first N rows (for testing)")
    parser.add_argument("--sleep", type=float, default=0.0, help="Delay in seconds between API calls (avoid rate limits)")
    args = parser.parse_args()

    # ---- 2. Load input data ----
    df = pd.read_csv(args.input)
    if args.limit:  # for testing smaller batches
        df = df.head(args.limit)

    # ---- 3. Load system prompt and create API client ----
    system_prompt = read_system_prompt(args.system)
    client = create_openai_client()

    results = []

    # ---- 4. Loop through articles row by row ----
    for idx, row in df.iterrows():
        uid = row["Unique_ID"]              # unique identifier for tracking
        year = row.get("Year", "")          # publication year (if present)
        title = row.get("Title", "")        # article title
        abstract = row.get("Abstract", "")  # article abstract

        # Build the user-specific prompt for this article
        user_prompt = build_user_prompt(uid, year, title, abstract)

        # Send request to OpenAI API
        raw = call_gpt_api(client, system_prompt, user_prompt, model=args.model)

        # Parse and normalize model response
        parsed = safe_json_loads(raw) or {}
        normalized = normalize_result(parsed)
        normalized["Unique_ID"] = uid  # keep track of the article

        # Store results
        results.append(normalized)

        # Optional sleep for rate-limiting
        if args.sleep > 0:
            time.sleep(args.sleep)

    # ---- 5. Merge results back into original dataframe ----
    res_df = pd.DataFrame(results)
    merged = df.merge(res_df, on="Unique_ID", how="left")

    # ---- 6. Save merged dataframe to CSV ----
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    merged.to_csv(args.output, index=False)

    print(f"✅ Stage 1 screening complete. Wrote: {args.output}")

# Entry point when script is run directly
if __name__ == "__main__":
    main()
