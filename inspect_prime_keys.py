#!/usr/bin/env python3
"""
Inspect and map prime_ledger.ndjson schema keys.
"""
import json
from pathlib import Path

ndjson_file = Path("./06_strata_data/prime_ledger.ndjson")
if not ndjson_file.exists():
    print(f"File not found: {ndjson_file}")
    exit(1)

with open(ndjson_file, "r", encoding="utf-8") as f:
    sample = [json.loads(line.strip()) for _, line in zip(range(3), f) if line.strip()]

print(f"Loaded {len(sample)} sample records.")
for i, rec in enumerate(sample):
    print(f"\n--- Record {i} ---")
    for k, v in rec.items():
        v_str = str(v)
        if len(v_str) > 60:
            v_str = v_str[:60] + "..."
        print(f"  {k}: {v_str}")
