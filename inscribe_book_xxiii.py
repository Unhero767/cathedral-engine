#!/usr/bin/env python3
# ==============================================================================
# Cathedral-Engine Ash Archive Monograph Inscription: Book XXIII
# File: inscribe_book_xxiii.py
# ==============================================================================

import json
import os
import hashlib
from datetime import datetime

ARCHIVE_PATH = "strata/ash_archive_codex_xxiii.json"

def inscribe_codex():
    print("[ARCHIVE] Initiating cryptographic inscription for Book XXIII: The Gravitic Altars...")
    
    treatise_payload = {
        "codex_book": 23,
        "title": "The Gravitic Altars: The Architecture of Gravitational Stratigraphy",
        "spectral_dominant": "BLUE_SORROW",
        "core_thesis": "Localized gravitational fields shaped through non-Euclidean mass-tensor arrays provide essential structural tension and inertial stability across outer choir vaults.",
        "axioms": [
            "Gravitic flux operates as a load-bearing tension vector within non-Euclidean architecture.",
            "Tensors of mass distribution stabilize chambers against gravitational shear.",
            "Gravitational curvature metrics are permanently archived as stratigraphic layers within the Ash Archive."
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

    print(f"[ARCHIVE] Book XXIII successfully inscribed into the Ash Archive. Block Hash: {block_hash[:16]}...")

if __name__ == "__main__":
    inscribe_codex()
