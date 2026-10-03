#!/usr/bin/env python3
"""
Cathedral-Engine: Gate 1
Audit SQLite database files configured for the Ash Archive; confirm that triggers
prevent_ash_archive_update and prevent_ash_archive_delete are active in all WAL-mode profiles.
"""
import sqlite3
import sys
from pathlib import Path

TARGET_DBS = [
    Path("/users/kennethdallmier/cathedral_engine/ash_archive_stratum.db"),
    Path("/users/kennethdallmier/cathedral_engine/ash_archive.db"),
]

EXPECTED_TRIGGERS = {
    "prevent_ash_archive_update": "UPDATE",
    "prevent_ash_archive_delete": "DELETE",
}

def verify_database_interlocks(db_path: Path) -> bool:
    if not db_path.exists():
        print(f"[SKIP] Database not found: {db_path}")
        return True

    print(f"\n--- Auditing: {db_path} ---")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Verify WAL Mode
    cursor.execute("PRAGMA journal_mode;")
    mode_row = cursor.fetchone()
    mode = mode_row[0].upper() if mode_row else "UNKNOWN"
    print(f"Journal Mode: {mode}")
    if mode != "WAL":
        print(f"[FAIL] {db_path} is running under {mode}, expected WAL.")
        conn.close()
        return False

    # 2. Inspect Triggers
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type = 'trigger';")
    active_triggers = {row[0]: row[1] for row in cursor.fetchall()}

    for trig_name, action in EXPECTED_TRIGGERS.items():
        if trig_name not in active_triggers:
            print(f"[FAIL] Missing critical trigger: {trig_name}")
            conn.close()
            return False
        
        sql = active_triggers[trig_name].upper()
        if f"BEFORE {action} ON" not in sql or "RAISE" not in sql:
            print(f"[FAIL] Trigger {trig_name} is malformed or lacks Lex I RAISE abort.")
            conn.close()
            return False
        print(f"[PASS] Interlock verified: {trig_name} ({action})")

    # 3. Dynamic Mutation Defense Test
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ash_archive';")
    if not cursor.fetchone():
        print("[FAIL] Table 'ash_archive' does not exist.")
        conn.close()
        return False

    cursor.execute("SELECT node_id FROM ash_archive LIMIT 1;")
    sample_row = cursor.fetchone()
    if sample_row:
        sample_id = sample_row[0]
        # Attempt Mutation
        try:
            conn.execute(f"UPDATE ash_archive SET atom_key = 'MUTATION_TEST' WHERE node_id = {sample_id};")
            print("[CRITICAL FAIL] Database allowed UPDATE on ash_archive.")
            conn.close()
            return False
        except sqlite3.DatabaseError as e:
            print(f"[PASS] Mutation rejected: {e}")

        # Attempt Deletion
        try:
            conn.execute(f"DELETE FROM ash_archive WHERE node_id = {sample_id};")
            print("[CRITICAL FAIL] Database allowed DELETE on ash_archive.")
            conn.close()
            return False
        except sqlite3.DatabaseError as e:
            print(f"[PASS] Deletion rejected: {e}")
    else:
        print("[WARN] Table ash_archive is empty; dynamic trigger verification verified via static SQL check.")

    conn.close()
    return True

if __name__ == "__main__":
    existing_targets = [db for db in TARGET_DBS if db.exists()]
    if not existing_targets:
        print("[ERROR] No target Ash Archive databases found at specified paths.")
        sys.exit(1)
        
    results = [verify_database_interlocks(db) for db in existing_targets]
    if not all(results):
        print("\nAudit Status: FAILED.")
        sys.exit(1)
    print("\nAudit Status: ALL ASH ARCHIVE INTERLOCKS COMPLIANT (Lex I).")
