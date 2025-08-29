import os
import time
import argparse
import pandas as pd

from openai_client import create_openai_client, call_gpt_api
from utils_1 import build_user_prompt, safe_json_loads, normalize_result

DEFAULT_INPUT = "data/sample_articles.csv"
DEFAULT_OUTPUT = "data/screen_stage1.csv"
DEFAULT_SYSTEM_PROMPT = "system_prompt_1.txt"

def read_system_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(description="Stage 1 screening: English + 2019–2025")
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--system", default=DEFAULT_SYSTEM_PROMPT)
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--sleep", type=float, default=0.0)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    if args.limit:
        df = df.head(args.limit)

    system_prompt = read_system_prompt(args.system)
    client = create_openai_client()

    results = []
    for idx, row in df.iterrows():
        uid = row["id"]
        year = row.get("Year", "")
        title = row.get("Title", "")
        abstract = row.get("Abstract", "")

        user_prompt = build_user_prompt(uid, year, title, abstract)
        raw = call_gpt_api(client, system_prompt, user_prompt, model=args.model)

        parsed = safe_json_loads(raw) or {}
        normalized = normalize_result(parsed)
        normalized["id"] = uid

        results.append(normalized)

        if args.sleep > 0:
            time.sleep(args.sleep)

    res_df = pd.DataFrame(results)
    merged = df.merge(res_df, on="id", how="left")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    merged.to_csv(args.output, index=False)
    print(f"✅ Stage 1 screening complete. Wrote: {args.output}")

if __name__ == "__main__":
    main()

