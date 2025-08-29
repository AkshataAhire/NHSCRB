# main_3.py — Stage 3: Occurs in NHS / health & social care / community health settings

import os
import time
import argparse
import pandas as pd

from openai_client import create_openai_client, call_gpt_api
from utils_3 import build_user_prompt, safe_json_loads, normalize_result

DEFAULT_INPUT = "data/sample_articles.csv"
DEFAULT_OUTPUT = "data/screen_stage3_occurs_in_nhs.csv"
DEFAULT_SYSTEM = "system_prompt_3.txt"
DEFAULT_MODEL = "gpt-4o"

def read_system_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def main():
    parser = argparse.ArgumentParser(
        description="Stage 3 screening: occurs in NHS / health & social care / community health settings"
    )
    parser.add_argument("--input", default=DEFAULT_INPUT)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--system", default=DEFAULT_SYSTEM)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--sleep", type=float, default=0.0)
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    if args.limit:
        df = df.head(args.limit)

    system_prompt = read_system_prompt(args.system)
    client = create_openai_client()

    rows = []
    for idx, row in df.iterrows():
        uid = row["Unique_ID"]
        title = row.get("Title", "")
        abstract = row.get("Abstract", "")
        metadata = {k: (None if pd.isna(v) else v) for k, v in row.to_dict().items()}

        user_prompt = build_user_prompt(uid, title, abstract, metadata)
        raw = call_gpt_api(client, system_prompt, user_prompt, model=args.model)

        parsed = safe_json_loads(raw) or {}
        normalized = normalize_result(parsed)
        normalized["Unique_ID"] = uid
        rows.append(normalized)

        if args.sleep > 0:
            time.sleep(args.sleep)

    res = pd.DataFrame(rows)
    out = df.merge(res, on="Unique_ID", how="left")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    out.to_csv(args.output, index=False)
    print(f"✅ Stage 3 screening complete. Wrote: {args.output}")

if __name__ == "__main__":
    main()
