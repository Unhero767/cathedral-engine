#!/usr/bin/env python3
# ==============================================================================
# Cathedral-Engine Ash Archive Monograph Inscription: Book XXII
# File: inscribe_book_xxii.py
# ==============================================================================

import json
import os
import hashlib
from datetime import datetime

ARCHIVE_PATH = "strata/ash_archive_codex_xxii.json"

def inscribe_codex():
    print("[ARCHIVE] Initiating cryptographic inscription for Book XXII: The Refractive Spires...")
    
    treatise_payload = {
        "codex_book": 22,
        "title": "The Refractive Spires: The Architecture of Optical Stratigraphy",
        "spectral_dominant": "GOLD_JOY",
        "core_thesis": "Coherent photon fluxes refracted through non-Euclidean lattices crystallize into load-bearing dielectric structural struts.",
        "axioms": [
            "Luminosity functions as a rigid tensor field under precise geometric constraint.",
            "Crossed optical beams bind zero-point vacuum energy into transparent structural barriers.",
            "Refraction matrices are permanently archived as stratigraphic layers within the Ash Archive."
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

    print(f"[ARCHIVE] Book XXII successfully inscribed into the Ash Archive. Block Hash: {block_hash[:16]}...")

if __name__ == "__main__":
    inscribe_codex()
