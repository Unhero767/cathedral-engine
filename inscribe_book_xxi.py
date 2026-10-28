#!/usr/init/env python3
# ==============================================================================
# Cathedral-Engine Ash Archive Monograph Inscription: Book XXI
# File: inscribe_book_xxi.py
# ==============================================================================

import json
import os
import hashlib
from datetime import datetime

ARCHIVE_PATH = "strata/ash_archive_codex_xxi.json"

def inscribe_codex():
    print("[ARCHIVE] Initiating cryptographic inscription for Book XXI: The Resonance Vaults...")
    
    treatise_payload = {
        "codex_book": 21,
        "title": "The Resonance Vaults: The Architecture of Acoustic Stratigraphy",
        "spectral_dominant": "TEAL_CURIOSITY",
        "core_thesis": "Acoustic resonance within closed non-Euclidean chambers functions as load-bearing architectural substrate.",
        "axioms": [
            "Wave nodes crystallize zero-point energy into spatial mass.",
            "Harmonic eigenmodes prevent topological de-coherence across vault boundaries.",
            "Historical soundscapes are permanent geological strata within the Ash Archive."
        ],
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    
    prev_hash = "0000000000000000000000000000000000000000000000000000000000000000"
    if os.path.exists(ARCHIVE_PATH):
        with open(ARCHIVE_PATH, "r") as f:
            existing = json.load(f)
            if existing:
                prev_hash = existing[-1].get("block_hash", prev_hash)

    serialized = json.dumps(treatise_payload, sort_keys=True) + prev_hash
    block_hash = hashlib.sha256(serialized.encode('utf-8')).hexdigest()

    archive_record = {
        "prev_hash": prev_hash,
        "block_hash": block_hash,
        "monograph": treatise_payload
    }

    os.makedirs(os.path.dirname(ARCHIVE_PATH), exist_ok=True)
    with open(ARCHIVE_PATH, "w") as f:
        json.dump([archive_record], f, indent=4)

    print(f"[ARCHIVE] Book XXI successfully inscribed into the Ash Archive. Block Hash: {block_hash[:16]}...")

if __name__ == "__main__":
    inscribe_codex()
