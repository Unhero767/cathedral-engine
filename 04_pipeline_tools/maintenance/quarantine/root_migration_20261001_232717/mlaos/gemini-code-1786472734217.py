from __future__ import annotations

import copy
import hashlib
import json
import sqlite3
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class ConstitutionViolation(Exception):
    """Raised when an architectural or constitutional rule is violated."""


CANONICAL_STATUS = {"LAB", "PROVISIONAL", "CANON", "SUPERSEDED", "ASH"}
REALITY_LEVELS = {"R0", "R1", "R2", "R3", "R4", "R5"}
VALID_AUTHORITIES = {
    "HUMAN_SOVEREIGN",
    "ARCHITECT_PRIME",
    "AI_PROPOSAL",
    "CRUCIBLE_REVIEW",
    "AUTOMATED_LINTER",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def hash_state(state: Dict[str, Any]) -> str:
    canonical = json.dumps(state, sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Event:
    event_id: str
    timestamp: str
    entity_id: str
    previous_state_hash: Optional[str]
    new_state: Dict[str, Any]
    reason: str
    author: str
    authority: str
    provenance: List[str] = field(default_factory=list)


class MLAOSPersistentLedger:
    """Persistent Event-Sourcing Ledger enforcing Constitution vΩ.1."""

    def __init__(self, db_path: str | Path = "mlaos_core.db") -> None:
        self.db_path = Path(db_path)
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

    def _validate_entity_state(self, state: Dict[str, Any]) -> None:
        required_fields = {
            "id",
            "name",
            "definition",
            "type",
            "canonical_status",
            "reality_level",
        }
        missing = required_fields - set(state.keys())
        if missing:
            raise ConstitutionViolation(
                f"Entity state missing required fields: {sorted(missing)}"
            )
        if state["canonical_status"] not in CANONICAL_STATUS:
            raise ConstitutionViolation(
                f"Invalid canonical status: {state['canonical_status']}"
            )
        if state["reality_level"] not in REALITY_LEVELS:
            raise ConstitutionViolation(
                f"Invalid reality level: {state['reality_level']}"
            )

    def current_state(self, entity_id: str) -> Dict[str, Any]:
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT new_state_json FROM events e
                JOIN entities ent ON e.event_id = ent.latest_event_id
                WHERE ent.entity_id = ?
                """,
                (entity_id,),
            )
            row = cursor.fetchone()
            if not row:
                raise ConstitutionViolation(f"Unknown or uninitialized entity: {entity_id}")
            return json.loads(row["new_state_json"])

    def entity_exists(self, entity_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT 1 FROM entities WHERE entity_id = ?", (entity_id,)
            )
            return cursor.fetchone() is not None

    def create_entity(
        self,
        entity_id: str,
        name: str,
        definition: str,
        entity_type: str,
        author: str,
        canonical_status: str = "LAB",
        reality_level: str = "R0",
        dependencies: Optional[List[str]] = None,
        invariants: Optional[List[str]] = None,
        representations: Optional[List[Dict[str, str]]] = None,
        implementation_path: Optional[str] = None,
        termination_condition: Optional[str] = None,
        reason: str = "Initial entity creation.",
        authority: str = "AI_PROPOSAL",
    ) -> Event:
        if self.entity_exists(entity_id):
            raise ConstitutionViolation(f"C-01: Entity already exists: {entity_id}")
        if not reason.strip():
            raise ConstitutionViolation("C-01: Mutation requires explicit reason.")
        if not author.strip():
            raise ConstitutionViolation("C-02: Mutation requires explicit author.")
        if authority not in VALID_AUTHORITIES:
            raise ConstitutionViolation(f"C-02: Unknown authority: {authority}")

        state = {
            "id": entity_id,
            "name": name,
            "definition": definition,
            "type": entity_type,
            "canonical_status": canonical_status,
            "reality_level": reality_level,
            "dependencies": dependencies or [],
            "invariants": invariants or [],
            "representations": representations or [],
            "claims": [],
            "contradictions": [],
            "implementation_path": implementation_path,
            "termination_condition": termination_condition,
        }

        self._validate_entity_state(state)

        event_id = f"EVT-{uuid.uuid4()}"
        timestamp = now_iso()
        event = Event(
            event_id=event_id,
            timestamp=timestamp,
            entity_id=entity_id,
            previous_state_hash=None,
            new_state=copy.deepcopy(state),
            reason=reason,
            author=author,
            authority=authority,
            provenance=[],
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
                """
                INSERT INTO entities (
                    entity_id, latest_event_id, current_status, reality_level, updated_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (entity_id, event_id, canonical_status, reality_level, timestamp),
            )
            conn.commit()

        return event

    def propose_change(
        self,
        entity_id: str,
        patch: Dict[str, Any],
        author: str,
        reason: str,
        authority: str = "AI_PROPOSAL",
        provenance: Optional[List[str]] = None,
    ) -> Event:
        if not self.entity_exists(entity_id):
            raise ConstitutionViolation(f"Unknown entity: {entity_id}")
        if not reason.strip():
            raise ConstitutionViolation("C-01: Mutation requires explicit reason.")
        if not author.strip():
            raise ConstitutionViolation("C-02: Mutation requires explicit author.")
        if authority not in VALID_AUTHORITIES:
            raise ConstitutionViolation(f"C-02: Unknown authority: {authority}")

        current_state = self.current_state(entity_id)
        expected_hash = hash_state(current_state)

        new_state = copy.deepcopy(current_state)
        for key, value in patch.items():
            new_state[key] = value

        self._validate_entity_state(new_state)

        if current_state["canonical_status"] == "CANON":
            if len(reason.strip()) < 12:
                raise ConstitutionViolation(
                    "C-01/C-05: Canonical revisions require substantial reason (>= 12 chars)."
                )

        event_id = f"EVT-{uuid.uuid4()}"
        timestamp = now_iso()
        event = Event(
            event_id=event_id,
            timestamp=timestamp,
            entity_id=entity_id,
            previous_state_hash=expected_hash,
            new_state=copy.deepcopy(new_state),
            reason=reason,
            author=author,
            authority=authority,
            provenance=provenance or [],
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
                """
                UPDATE entities
                SET latest_event_id = ?, current_status = ?, reality_level = ?, updated_at = ?
                WHERE entity_id = ?
                """,
                (
                    event_id,
                    new_state["canonical_status"],
                    new_state["reality_level"],
                    timestamp,
                    entity_id,
                ),
            )
            conn.commit()

        return event

    def add_claim(
        self,
        entity_id: str,
        claim: str,
        author: str,
        reason: str = "Add claim.",
        authority: str = "AI_PROPOSAL",
    ) -> Event:
        current_state = self.current_state(entity_id)
        claims = current_state.get("claims", [])

        if claim in claims:
            return self.propose_change(
                entity_id=entity_id,
                patch={"claims": claims},
                author=author,
                reason=f"No-op claim addition: {claim}",
                authority=authority,
            )

        opposite = f"!{claim}" if not claim.startswith("!") else claim[1:]

        if opposite in claims:
            contra_id = f"CONTRA-{uuid.uuid4()}"
            with self._get_connection() as conn:
                conn.execute(
                    """
                    INSERT INTO contradictions (
                        contradiction_id, entity_id, claim, counterclaim,
                        severity, scope, status, resolution_path, recorded_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        contra_id,
                        entity_id,
                        claim,
                        opposite,
                        "LOCAL",
                        "ENTITY",
                        "PRESERVED",
                        "CRUCIBLE_REVIEW",
                        now_iso(),
                    ),
                )
                conn.commit()

        new_claims = claims + [claim]
        return self.propose_change(
            entity_id=entity_id,
            patch={"claims": new_claims},
            author=author,
            reason=reason,
            authority=authority,
        )

    def get_contradictions(self, entity_id: Optional[str] = None) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            if entity_id:
                cursor = conn.execute(
                    "SELECT * FROM contradictions WHERE entity_id = ?", (entity_id,)
                )
            else:
                cursor = conn.execute("SELECT * FROM contradictions")
            return [dict(row) for row in cursor.fetchall()]

    def list_entities(self) -> List[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT entity_id, current_status, reality_level, updated_at FROM entities"
            )
            return [dict(row) for row in cursor.fetchall()]