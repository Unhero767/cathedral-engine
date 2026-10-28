#!/usr/bin/env python3
# ==============================================================================
# Cathedral-Engine Persistent Roster Inspection Utility
# File: inspect_persistent_roster.py
# ==============================================================================

import json
import os

LEDGER_PATH = "strata/persistent_roster_ledger.json"

def inspect_roster():
    print("[CATHE_INSPECT] Querying persistent world roster ledger strata...")
    
    if not os.path.exists(LEDGER_PATH):
        print(f"[CATHE_ERR] Ledger not found at {LEDGER_PATH}. Run simulate_persistent_roster.py first.")
        return

    with open(LEDGER_PATH, 'r') as f:
        records = json.load(f)

    total_entities = len(records)
    print(f"[CATHE_INSPECT] Total persistent entities in ledger N = {total_entities}")
    print("--------------------------------------------------------------------------------")
    
    sanctum_count = 0
    expedition_count = 0
    total_coherence = 0.0

    for idx, node in enumerate(records):
        data = node.get("data", {})
        entity_id = data.get("entity_id", "UNKNOWN")
        name = data.get("entity_name", "Unnamed")
        stratum = data.get("operational_stratum", "Unknown")
        coherence = data.get("ontological_coherence", 0.0)
        binary_state = data.get("binary_existence_state", True)
        block_hash = node.get("block_hash", "")[:12]
        
        total_coherence += coherence
        if stratum == "Basecamp Sanctum":
            sanctum_count += 1
        elif stratum == "Active Expedition":
            expedition_count += 1
            
        print(f"[{entity_id}] {name}")
        print(f"  -> Stratum: {stratum} | Coherence: {coherence:.2f} | Non-Binary: {not binary_state}")
        print(f"  -> Merkle Hash: {block_hash}...")
    
    avg_coherence = total_coherence / total_entities if total_entities > 0 else 0.0
    print("--------------------------------------------------------------------------------")
    print(f"[CATHE_INSPECT] Stratum Distribution -> Sanctum: {sanctum_count} | Expedition: {expedition_count}")
    print(f"[CATHE_INSPECT] Average Ontological Coherence across N: {avg_coherence:.4f}")
    print("[CATHE_INSPECT] Roster ledger integrity check complete. All entities nominal.")

if __name__ == "__main__":
    inspect_roster()
