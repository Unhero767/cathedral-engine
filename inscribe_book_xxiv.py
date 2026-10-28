#!/usr/bin/env python3
# ==============================================================================
# Cathedral-Engine Ash Archive Monograph Inscription: Book XXIV
# File: inscribe_book_xxiv.py
# ==============================================================================

import json
import os
import hashlib
from datetime import datetime

ARCHIVE_PATH = "strata/ash_archive_codex_xxiv.json"

def inscribe_codex():
    print("[ARCHIVE] Initiating cryptographic inscription for Book XXIV: The Chronologic Sanctuaries...")
    
    treatise_payload = {
        "codex_book": 24,
        "title": "The Chronologic Sanctuaries: The Architecture of Temporal Stratigraphy",
        "spectral_dominant": "BRONZE_OBSIDIAN_NULL",
        "core_thesis": "Compressible temporal gradients bind past execution states and future projection vectors into load-bearing chronological strata across outer choir vaults.",
        "axioms": [
            "Temporal flow functions as a compressible stratigraphic medium within non-Euclidean enclosures.",
            "Block universe grammar treats past and future operational states as simultaneous structural loads.",
            "Chronological sync metrics are permanently archived as immutable layers within the Ash Archive."
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

    print(f"[ARCHIVE] Book XXIV successfully inscribed into the Ash Archive. Block Hash: {block_hash[:16]}...")

if __name__ == "__main__":
    inscribe_codex()
