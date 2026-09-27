#!/usr/bin/env python3
# ==============================================================================
# Cathedral-Engine Active Parties Seeding Utility
# File: seed_active_parties.py
# ==============================================================================

import sqlite3
import os

DB_PATH = "strata/cathedral_engine.db"

def seed_parties():
    print("[CATHE_PARTY] Connecting to Cathedral persistence layer...")
    
    if not os.path.exists(DB_PATH):
        print(f"[CATHE_ERR] Database not found at {DB_PATH}. Run init_cathedral_db.py and seed_stable_characters.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Initial expedition squad assignment referencing valid character IDs
    # Slot 1: Kaelen Vane (CHAR-02)
    # Slot 2: Sariel Thorne (CHAR-03)
    # Slot 3 & 4: NULL (Unassigned slot flex)
    initial_parties = [
        ("PARTY-ALPHA", "CHAR-02", "CHAR-03", None, None, "DUNGEON-DEEP-01", "CHAMBER-03", 0.94, 1)
    ]

    print(f"[CATHE_PARTY] Inscribing {len(initial_parties)} active party formation(s)...")
    
    for party in initial_parties:
        try:
            cursor.execute("""
            INSERT OR REPLACE INTO active_parties 
            (party_id, slot_1_id, slot_2_id, slot_3_id, slot_4_id, dungeon_id, current_chamber_id, composite_cohesion, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, party)
            print(f"[CATHE_PARTY] Inscribed Party [{party[0]}] | Dungeon: {party[5]} | Chamber: {party[6]} | Cohesion: {party[7]:.2f}")
        except sqlite3.IntegrityError as e:
            print(f"[CATHE_ERR] Failed to seed party {party[0]}: {e}")

    conn.commit()
    conn.close()
    print("[CATHE_PARTY] Party seeding sequence complete. Relational topology locked.")

if __name__ == "__main__":
    seed_parties()
