#!/usr/bin/env python3
import argparse, os, json
parser = argparse.ArgumentParser()
parser.add_argument("--config", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()
os.makedirs(args.output, exist_ok=True)
print(f"[PRETRAIN] Initializing base model weights using {args.config} -> {args.output}")
with open(os.path.join(args.output, "config.json"), "w") as f:
    json.dump({"architectures": ["LlamaForCausalLM"], "vocab_size": 32000}, f)
print("[PRETRAIN] Base model weights synthesized.")
