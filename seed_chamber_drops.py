#!/usr/bin/env python3
# ==============================================================================
# Cathedral-Engine Chamber Persistent Drops Seeding Utility
# File: seed_chamber_drops.py
# ==============================================================================

import sqlite3
import os
import json

DB_PATH = "strata/cathedral_engine.db"

def seed_drops():
    print("[CATHE_DROPS] Connecting to Cathedral persistence layer...")
    
    if not os.path.exists(DB_PATH):
        print(f"[CATHE_ERR] Database not found at {DB_PATH}. Run prior initialization and seeding scripts first.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Initial persistent drops left behind during expedition operations
    initial_drops = [
        (
            "DROP-001", 
            "CHAMBER-03", 
            "CHAR-02", 
            json.dumps({"item_name": "Resonance Prism", "tier": "ASTRAL", "potency": 45.2}), 
            "UNRECOVERED"
        ),
        (
            "DROP-002", 
            "CHAMBER-07", 
            "CHAR-04", 
            json.dumps({"item_name": "Shattered Lithic Core", "tier": "OBSIDIAN", "potency": 89.9}), 
            "UNRECOVERED"
        )
    ]

    print(f"[CATHE_DROPS] Inscribing {len(initial_drops)} persistent drop record(s)...")
    
    for drop in initial_drops:
        try:
            cursor.execute("""
            INSERT OR REPLACE INTO chamber_persistent_drops 
            (drop_id, chamber_id, owner_character_id, item_payload_json, retrieval_status)
            VALUES (?, ?, ?, ?, ?);
            """, drop)
            payload_summary = json.loads(drop[3])
            print(f"[CATHE_DROPS] Inscribed Drop [{drop[0]}] in {drop[1]} -> Item: '{payload_summary['item_name']}' [Status: {drop[4]}]")
        except sqlite3.IntegrityError as e:
            print(f"[CATHE_ERR] Failed to seed drop {drop[0]}: {e}")

    conn.commit()
    conn.close()
    print("[CATHE_DROPS] Drop seeding sequence complete. Artifact strata locked.")

if __name__ == "__main__":
    seed_drops()
