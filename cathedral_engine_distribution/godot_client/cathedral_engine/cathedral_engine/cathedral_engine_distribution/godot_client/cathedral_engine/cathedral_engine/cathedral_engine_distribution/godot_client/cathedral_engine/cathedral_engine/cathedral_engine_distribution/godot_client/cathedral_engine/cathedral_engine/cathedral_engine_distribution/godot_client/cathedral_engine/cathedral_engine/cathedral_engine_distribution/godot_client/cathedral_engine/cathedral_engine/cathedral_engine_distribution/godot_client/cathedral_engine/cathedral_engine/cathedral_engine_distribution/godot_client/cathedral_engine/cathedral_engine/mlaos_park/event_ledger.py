import sqlite3
import hashlib
import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

class SparkEventLedger:
    def __init__(self, db_path: str, ndjson_path: str):
        self.db_path = db_path
        self.ndjson_path = ndjson_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.ndjson_path), exist_ok=True)
        self._init_db()

    def _get_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_conn() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS spark_event_ledger (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    aggregate_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    prev_merkle_root TEXT NOT NULL,
                    merkle_root TEXT NOT NULL,
                    inscribed_at TEXT NOT NULL
                );

                CREATE TRIGGER IF NOT EXISTS spark_ledger_prevent_update
                BEFORE UPDATE ON spark_event_ledger
                BEGIN
                    SELECT RAISE(FAIL, 'Lex I Violation: Ledger events are strictly immutable.');
                END;

                CREATE TRIGGER IF NOT EXISTS spark_ledger_prevent_delete
                BEFORE DELETE ON spark_event_ledger
                BEGIN
                    SELECT RAISE(FAIL, 'Lex I Violation: Historical state cannot be deleted.');
                END;
            """)
            conn.commit()

    def get_last_merkle_root(self) -> str:
        with self._get_conn() as conn:
            cur = conn.execute("SELECT merkle_root FROM spark_event_ledger ORDER BY event_id DESC LIMIT 1")
            row = cur.fetchone()
            return row["merkle_root"] if row else "0x0000000000000000_GENESIS_SPARK"

    def append_event(self, event_type: str, aggregate_id: str, payload: Dict[str, Any]) -> str:
        prev_root = self.get_last_merkle_root()
        ts = datetime.now(timezone.utc).isoformat()
        payload_str = json.dumps(payload, sort_keys=True)
        raw_hash = hashlib.sha256(f"{prev_root}_{event_type}_{aggregate_id}_{payload_str}_{ts}".encode()).hexdigest().upper()
        merkle_root = f"0x{raw_hash}"

        with self._get_conn() as conn:
            conn.execute("""
                INSERT INTO spark_event_ledger (event_type, aggregate_id, payload_json, prev_merkle_root, merkle_root, inscribed_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (event_type, aggregate_id, payload_str, prev_root, merkle_root, ts))
            conn.commit()

        event_doc = {
            "event_type": event_type,
            "aggregate_id": aggregate_id,
            "payload": payload,
            "prev_merkle_root": prev_root,
            "merkle_root": merkle_root,
            "inscribed_at": ts
        }
        with open(self.ndjson_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event_doc) + chr(10))

        return merkle_root
