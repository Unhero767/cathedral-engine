from __future__ import annotations
import copy
import hashlib
import json
import sqlite3
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

class ConstitutionViolation(Exception):
    """Raised when an operation violates Constitution vΩ.1."""
    pass

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def sha256_hexdigest(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

@dataclass
class Event:
    event_id: str
    timestamp: str
    entity_id: str
    previous_state_hash: Optional[str]
    new_state: Dict[str, Any]
    reason: str
    author: str
    authority: str
    provenance: List[str]

class LedgerEngine:
    """
    MLAOS Sovereign Event-Sourcing Ledger Engine
    Enforces Constitution vΩ.1, Lex I Never-Overwrite cryptographic hash chains,
    and paraconsistent contradiction quarantine.
    """
    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            base_dir = Path(__file__).resolve().parent.parent
            db_path = str(base_dir / "strata" / "mlaos_ledger.db")
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_db(self) -> None:
        with self._get_connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS entities (
                    entity_id         TEXT PRIMARY KEY,
                    latest_event_id   TEXT NOT NULL,
                    current_status    TEXT NOT NULL,
                    reality_level     TEXT NOT NULL,
                    updated_at        TEXT NOT NULL
                );

                CREATE TABLE IF NOT EXISTS events (
                    event_id            TEXT PRIMARY KEY,
                    timestamp           TEXT NOT NULL,
                    entity_id           TEXT NOT NULL,
                    previous_state_hash TEXT,
                    new_state_json      TEXT NOT NULL,
                    reason              TEXT NOT NULL,
                    author              TEXT NOT NULL,
                    authority           TEXT NOT NULL,
                    provenance_json     TEXT NOT NULL DEFAULT '[]',
                    FOREIGN KEY (entity_id) REFERENCES entities(entity_id)
                );

                CREATE TABLE IF NOT EXISTS contradictions (
                    contradiction_id TEXT PRIMARY KEY,
                    entity_id        TEXT NOT NULL,
                    claim            TEXT NOT NULL,
                    counterclaim     TEXT NOT NULL,
                    severity         TEXT NOT NULL,
                    scope            TEXT NOT NULL,
                    status           TEXT NOT NULL,
                    resolution_path  TEXT,
                    recorded_at      TEXT NOT NULL,
                    FOREIGN KEY (entity_id) REFERENCES entities(entity_id)
                );
                """
            )
            conn.commit()

    def create_entity(
        self,
        entity_id: str,
        name: str,
        definition: str,
        entity_type: str,
        author: str,
        authority: str = "HUMAN_SOVEREIGN",
        canonical_status: str = "LAB",
        reality_level: str = "R1",
        dependencies: Optional[List[str]] = None,
        implementation_path: Optional[str] = None,
        reason: str = "Initial Genesis registration",
    ) -> Event:
        """Registers a new entity into the ledger with genesis event."""
        with self._get_connection() as conn:
            cur = conn.execute("SELECT entity_id FROM entities WHERE entity_id = ?", (entity_id,))
            if cur.fetchone():
                raise ConstitutionViolation(f"C-01: Entity already exists: {entity_id}")

        timestamp = now_iso()
        event_id = f"EVT-{uuid.uuid4()}"
        state = {
            "id": entity_id,
            "name": name,
            "definition": definition,
            "type": entity_type,
            "canonical_status": canonical_status,
            "reality_level": reality_level,
            "dependencies": dependencies or [],
            "implementation_path": implementation_path,
            "claims": [],
        }

        event = Event(
            event_id=event_id,
            timestamp=timestamp,
            entity_id=entity_id,
            previous_state_hash=None,
            new_state=state,
            reason=reason,
            author=author,
            authority=authority,
            provenance=[],
        )

        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO entities (
                    entity_id, latest_event_id, current_status, reality_level, updated_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (entity_id, event_id, canonical_status, reality_level, timestamp),
            )
            conn.execute(
                """
                INSERT INTO events (
                    event_id, timestamp, entity_id, previous_state_hash,
                    new_state_json, reason, author, authority, provenance_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.timestamp,
                    event.entity_id,
                    event.previous_state_hash,
                    json.dumps(event.new_state, sort_keys=True),
                    event.reason,
                    event.author,
                    event.authority,
                    json.dumps(event.provenance),
                ),
            )
            conn.commit()

        return event

    def add_claim(self, entity_id: str, claim_text: str, author: str, reason: str, authority: str = "HUMAN_SOVEREIGN") -> Event:
        """Appends a claim to an entity and checks for paraconsistent contradiction quarantine."""
        if len(reason) < 12:
            raise ConstitutionViolation("C-01/C-05: Canonical revisions require substantial reason (>= 12 chars).")

        with self._get_connection() as conn:
            cur = conn.execute(
                "SELECT e.new_state_json, e.event_id FROM events e JOIN entities en ON e.event_id = en.latest_event_id WHERE en.entity_id = ?",
                (entity_id,),
            )
            row = cur.fetchone()
            if not row:
                raise ConstitutionViolation(f"Entity not found: {entity_id}")

            current_state = json.loads(row["new_state_json"])
            prev_hash = sha256_hexdigest(row["new_state_json"])

        new_state = copy.deepcopy(current_state)
        new_state.setdefault("claims", []).append({
            "text": claim_text,
            "author": author,
            "timestamp": now_iso()
        })

        event_id = f"EVT-{uuid.uuid4()}"
        timestamp = now_iso()
        event = Event(
            event_id=event_id,
            timestamp=timestamp,
            entity_id=entity_id,
            previous_state_hash=prev_hash,
            new_state=new_state,
            reason=reason,
            author=author,
            authority=authority,
            provenance=[row["event_id"]],
        )

        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO events (
                    event_id, timestamp, entity_id, previous_state_hash,
                    new_state_json, reason, author, authority, provenance_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.timestamp,
                    event.entity_id,
                    event.previous_state_hash,
                    json.dumps(event.new_state, sort_keys=True),
                    event.reason,
                    event.author,
                    event.authority,
                    json.dumps(event.provenance),
                ),
            )
            conn.execute(
                "UPDATE entities SET latest_event_id = ?, updated_at = ? WHERE entity_id = ?",
                (event_id, timestamp, entity_id),
            )

            # Check for contradiction with existing claims (e.g. negation prefix '!')
            for existing in current_state.get("claims", []):
                ex_text = existing["text"]
                if claim_text == f"!{ex_text}" or ex_text == f"!{claim_text}":
                    contra_id = f"CONTRA-{uuid.uuid4()}"
                    conn.execute(
                        """
                        INSERT INTO contradictions (
                            contradiction_id, entity_id, claim, counterclaim,
                            severity, scope, status, recorded_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (contra_id, entity_id, ex_text, claim_text, "MAJOR", "LOCAL_SCOPE", "QUARANTINED", timestamp),
                    )
            conn.commit()

        return event

    def get_contradictions(self, entity_id: str) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cur = conn.execute("SELECT * FROM contradictions WHERE entity_id = ?", (entity_id,))
            return [dict(r) for r in cur.fetchall()]

if __name__ == "__main__":
    ledger = LedgerEngine()
    print(f"[LEDGER] Database initialized at: {ledger.db_path}")
