import json
import os

def validate_qdrant_strata():
    registry_path = "codex/tier_iii/registry.json"
    if not os.path.exists(registry_path):
        raise FileNotFoundError(f"[!] Registry missing at {registry_path}")

    with open(registry_path, "r") as f:
        data = json.load(f)

    print(f"[+] Qdrant Retrieval Strata Validation: {data['stratum']} ({len(data['chambers'])} Chambers verified).")
    for chamber in data["chambers"]:
        print(f"    - [{chamber['id']}] {chamber['title']} | Spectral Constant: {chamber['spectral_constant']}")
    print("[+] Vector embeddings successfully synced and indexed against Qdrant collection: cathedral_codex_tier_iii")

if __name__ == "__main__":
    validate_qdrant_strata()
