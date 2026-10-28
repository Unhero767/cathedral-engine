#!/usr/bin/env python3
# ==============================================================================
# Cathedral-Engine Stable Characters Seeding Utility
# File: seed_stable_characters.py
# ==============================================================================

import sqlite3
import os

DB_PATH = "strata/cathedral_engine.db"

def seed_characters():
    print("[CATHE_SEED] Connecting to Cathedral persistence layer...")
    
    if not os.path.exists(DB_PATH):
        print(f"[CATHE_ERR] Database not found at {DB_PATH}. Run init_cathedral_db.py first.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Initial operator profiles mapped to valid spectral constants and status states
    initial_characters = [
        ("CHAR-01", "Mr. Laos", "OMEGA", 9.5, "SANCTUM_REST", "CHAMBER-00", 0.0, 0.0, 0.0, 0.0),
        ("CHAR-02", "Kaelen Vane", "PHI", 8.3, "ACTIVE_DELVE", "CHAMBER-03", 12.5, 4.1, -1.5, 1.2),
        ("CHAR-03", "Sariel Thorne", "THETA", 7.9, "ACTIVE_DELVE", "CHAMBER-03", 14.0, 3.8, -1.5, 2.4),
        ("CHAR-04", "Vespera Nyx", "PSI", 8.8, "PINNED_IN_CHAMBER", "CHAMBER-07", -5.2, 18.9, 0.0, 7.6)
    ]

    print(f"[CATHE_SEED] Inscribing {len(initial_characters)} operator profiles into stable_characters...")
    
    for char in initial_characters:
        try:
            cursor.execute("""
            INSERT OR REPLACE INTO stable_characters 
            (character_id, callsign, dominant_spectrum, ego_density, current_status, current_chamber_id, pos_x, pos_y, pos_z, somatic_stress, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP);
            """, char)
            print(f"[CATHE_SEED] Inscribed Operator [{char[0]}] '{char[1]}' | Spectrum: {char[2]} | Status: {char[4]}")
        except sqlite3.IntegrityError as e:
            print(f"[CATHE_ERR] Failed to seed operator {char[0]}: {e}")

    conn.commit()
    conn.close()
    print("[CATHE_SEED] Seeding sequence complete. Database state locked.")

if __name__ == "__main__":
    seed_characters()
