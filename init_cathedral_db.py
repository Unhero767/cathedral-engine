#!/usr/bin/env python3
# ==============================================================================
# Cathedral-Engine SQLite Relational Schema Initialization
# File: init_cathedral_db.py
# ==============================================================================

import sqlite3
import os

DB_PATH = "strata/cathedral_engine.db"

def initialize_database():
    print("[CATHE_DB] Initializing Cathedral-Engine SQLite persistence layer...")
    
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Table 1: stable_characters
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stable_characters (
        character_id TEXT PRIMARY KEY,
        callsign TEXT NOT NULL,
        dominant_spectrum TEXT NOT NULL CHECK(dominant_spectrum IN ('THETA','PSI','DELTA','PHI','OMEGA','EPSILON','NULL')),
        ego_density REAL NOT NULL DEFAULT 8.3,
        current_status TEXT NOT NULL CHECK(current_status IN ('SANCTUM_REST', 'ACTIVE_DELVE', 'PINNED_IN_CHAMBER', 'CRITICAL_STASIS', 'CARBONIZED')),
        current_chamber_id TEXT,
        pos_x REAL,
        pos_y REAL,
        pos_z REAL,
        somatic_stress REAL NOT NULL DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Table 2: active_parties
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS active_parties (
        party_id TEXT PRIMARY KEY,
        slot_1_id TEXT NOT NULL REFERENCES stable_characters(character_id),
        slot_2_id TEXT REFERENCES stable_characters(character_id),
        slot_3_id TEXT REFERENCES stable_characters(character_id),
        slot_4_id TEXT REFERENCES stable_characters(character_id),
        dungeon_id TEXT NOT NULL,
        current_chamber_id TEXT NOT NULL,
        composite_cohesion REAL NOT NULL DEFAULT 1.0,
        is_active BOOLEAN NOT NULL DEFAULT 1
    );
    """)

    # Table 3: chamber_persistent_drops
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chamber_persistent_drops (
        drop_id TEXT PRIMARY KEY,
        chamber_id TEXT NOT NULL,
        owner_character_id TEXT REFERENCES stable_characters(character_id),
        item_payload_json TEXT NOT NULL,
        retrieval_status TEXT NOT NULL DEFAULT 'UNRECOVERED' CHECK(retrieval_status IN ('UNRECOVERED', 'RETRIEVED', 'CONSUMED_BY_WASTE'))
    );
    """)

    conn.commit()
    conn.close()
    print(f"[CATHE_DB] Relational schema successfully compiled and locked at {DB_PATH}.")

if __name__ == "__main__":
    initialize_database()
