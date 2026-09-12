import os
import shutil
import json
from datetime import datetime, timezone

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STRATA_DIR = os.path.join(BASE_DIR, "strata")
LEDGER_PATH = os.path.join(STRATA_DIR, "prime_ledger.ndjson")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
MANIFEST_PATH = os.path.join(BASE_DIR, "codex_manifest.json")
EXPANDED_DIR = os.path.join(BASE_DIR, "expanded_chambers")

DEFAULT_CONFIG = {
    "active_chapter": "I. Prime Foundation",
    "core_thesis": "The stone does not merely feel the weight of the cathedral; the stone IS the weight of the architect's devotion made manifest.",
    "spectral_dominant": "Gold/Joy",
    "phi_intensity": 1.414,
    "dialetheic_buffer": True
}

DEFAULT_MANIFEST = [
    {
        "chapter": "I. Prime Foundation",
        "spectrum": "Gold/Joy",
        "phi": 1.414,
        "payload": "The stone does not merely feel the weight of the cathedral; the stone IS the weight of the architect's devotion made manifest."
    },
    {
        "chapter": "II. Inner Mandala",
        "spectrum": "Teal/Curiosity",
        "phi": 1.618,
        "payload": "Exploring the recursive geometries of the local state machine and paraconsistent logic gates."
    },
    {
        "chapter": "III. Outer Choirs",
        "spectrum": "Blue/Sorrow",
        "phi": 1.224,
        "payload": "Excavating the loss embedded within deprecated codebases and forgotten architectural strata."
    },
    {
        "chapter": "IV. Shadow Canon",
        "spectrum": "Bronze-Obsidian/Null",
        "phi": 0.000,
        "payload": "Processing dialetheic collisions without resolution, crystallizing contradictions into load-bearing Harmonic Scars."
    }
]

def reset_all():
    print("\n==========================================")
    print("   CATHEDRAL-ENGINE: FULL SYSTEM RESET    ")
    print("==========================================")

    # 1. Purge and recreate strata directory
    if os.path.exists(STRATA_DIR):
        shutil.rmtree(STRATA_DIR)
    os.makedirs(STRATA_DIR, exist_ok=True)
    print("  [+] Cleaned strata directory.")

    # 2. Purge expanded chambers
    if os.path.exists(EXPANDED_DIR):
        shutil.rmtree(EXPANDED_DIR)
    os.makedirs(EXPANDED_DIR, exist_ok=True)
    print("  [+] Reset expanded_chambers directory.")

    # 3. Reset config.json
    with open(CONFIG_PATH, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    print("  [+] Reset config.json to Genesis state.")

    # 4. Ensure codex_manifest.json exists
    if not os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "w") as f:
            json.dump(DEFAULT_MANIFEST, f, indent=2)
        print("  [+] Generated default codex_manifest.json.")

    # 5. Inscribe foundational strata
    with open(MANIFEST_PATH, "r") as f:
        manifest = json.load(f)

    seeded_count = 0
    with open(LEDGER_PATH, "w") as f:
        for entry in manifest:
            stratum = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "chapter": entry["chapter"],
                "thesis": DEFAULT_CONFIG["core_thesis"],
                "spectrum": entry["spectrum"],
                "phi": entry["phi"],
                "dialetheic_active": DEFAULT_CONFIG["dialetheic_buffer"],
                "payload": entry["payload"]
            }
            f.write(json.dumps(stratum) + "\n")
            seeded_count += 1

    print(f"  [+] Inscribed {seeded_count} canonical strata into prime_ledger.ndjson.")
    print("==========================================")
    print(" SYSTEM RESTORED TO RADIANT REST GENESIS. ")
    print("==========================================\n")

if __name__ == "__main__":
    reset_all()
