#!/usr/bin/env python3
import argparse, os, json
parser = argparse.ArgumentParser()
parser.add_argument("--model_dir", required=True)
args = parser.parse_args()
config_path = os.path.join(args.model_dir, "config.json")
if os.path.exists(config_path):
    with open(config_path, "r") as f:
        data = json.load(f)
    data["vocab_size"] = 32000
    with open(config_path, "w") as f:
        json.dump(data, f, indent=2)
print(f"[VOCAB] Reconciled configuration vocabulary for {args.model_dir}")
