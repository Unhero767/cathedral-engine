import sqlite3
import hashlib
import json
import datetime
import urllib.request

DB_PATH = "ash_archive.db"
TELEMETRY_URL = "http://localhost:8000/telemetry"

class MLAOSArbiterReconciliation:
    def __init__(self):
        self.init_arbiter_db()

    def init_arbiter_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute('''
            CREATE TABLE IF NOT EXISTS arbiter_reconciliations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                node_target TEXT,
                lex_compliance TEXT,
                parent_hash TEXT,
                synthesis_hash TEXT,
                payload TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def reconcile_fracture(self, node_id: str, conflict_type: str):
        print(f"[ARBITER] Reconciling Quarantined Fracture Node [{node_id}] | Conflict: {conflict_type}")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT merkle_hash FROM lab_experiments ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        parent_hash = row[0] if row else "0"*64
        
        synthesis_record = {
            "arbiterEngine": "MLAOS-Magisterial-Arbiter-v1",
            "targetNode": node_id,
            "conflictResolution": conflict_type,
            "lexCompliance": "LEX-I-ABSOLUTE",
            "parentHash": parent_hash,
            "timestamp": str(datetime.datetime.utcnow())
        }
        
        payload_str = json.dumps(synthesis_record, sort_keys=True)
        synthesis_hash = hashlib.sha256(payload_str.encode("utf-8")).hexdigest()
        
        cursor.execute(
            "INSERT INTO arbiter_reconciliations (node_target, lex_compliance, parent_hash, synthesis_hash, payload) VALUES (?, ?, ?, ?, ?)",
            (node_id, "LEX-I", parent_hash, synthesis_hash, payload_str)
        )
        conn.commit()
        conn.close()
        
        print(f"-> Crystallized Synthesis Block [SHA-256: {synthesis_hash[:16]}...]")
        try:
            urllib.request.urlopen(
                urllib.request.Request(
                    TELEMETRY_URL,
                    data=json.dumps({"tier": "ARBITER", "payload": synthesis_record}).encode("utf-8"),
                    headers={"Content-Type": "application/json"}
                )
            )
        except Exception:
            pass

if __name__ == "__main__":
    arbiter = MLAOSArbiterReconciliation()
    arbiter.reconcile_fracture("NODE-FRACTURE-884", "Dialetheic Overflow")
