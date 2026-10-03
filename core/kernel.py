"""
Cathedral-Engine Minimal Reference Kernel (Phase II Dual-Persistence):
Pipeline: Event Envelope -> Causal Ordering -> Assertion Relation -> FOUR -> SQLite WAL + NDJSON -> Merkle Hash
"""
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
from pathlib import Path
import sqlite3
import threading
import time
from typing import Any, Dict, List, Optional, Tuple


class BelnapValue(str, Enum):
    TRUE = "T"        # (1, 0)
    FALSE = "F"       # (0, 1)
    BOTH = "B"        # (1, 1) - Harmonic Scar (Dialetheic collision)
    NEITHER = "N"     # (0, 0) - Absence / Unasserted


class EpistemicRegisterTag(str, Enum):
    EMPIRICAL = "E"
    MODEL = "M"
    INTERPRETATION = "I"
    HYPOTHESIS = "H"
    SCAR = "S"
    NULL = "N"


@dataclass(frozen=True)
class EventEnvelope:
    event_id: str
    atom_key: str
    lamport_clock: int
    source_timestamp: float
    actor: str
    polarity: bool       # True = positive evidence (t), False = negative evidence (f)
    value: Any
    parents: Tuple[str, ...] = field(default_factory=tuple)
    register: EpistemicRegisterTag = EpistemicRegisterTag.EMPIRICAL

    def serialize_payload(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "atom_key": self.atom_key,
            "lamport_clock": self.lamport_clock,
            "source_timestamp": self.source_timestamp,
            "actor": self.actor,
            "polarity": self.polarity,
            "value": self.value,
            "parents": list(self.parents),
            "register": self.register.value,
        }


class CausalSorter:
    """
    Decouples arrival order from causal precedence.
    Sorts events deterministically by (lamport_clock, source_timestamp, event_id).
    """
    @staticmethod
    def sort(events: List[EventEnvelope]) -> List[EventEnvelope]:
        return sorted(
            events,
            key=lambda e: (e.lamport_clock, e.source_timestamp, e.event_id)
        )


class FourAssertionLattice:
    """
    Accumulates evidence polarities per atomKey into Belnap-Dunn FOUR semantics:
    t_support: >= 1 positive observation
    f_support: >= 1 negative observation
    (1,1) -> BOTH (Harmonic Scar; No Explosion: B -/-> Crash)
    """
    def __init__(self):
        self._positive_sources: Dict[str, set] = {}
        self._negative_sources: Dict[str, set] = {}

    def ingest(self, atom_key: str, actor: str, polarity: bool) -> BelnapValue:
        if atom_key not in self._positive_sources:
            self._positive_sources[atom_key] = set()
            self._negative_sources[atom_key] = set()

        if polarity:
            self._positive_sources[atom_key].add(actor)
        else:
            self._negative_sources[atom_key].add(actor)

        t_support = len(self._positive_sources[atom_key]) > 0
        f_support = len(self._negative_sources[atom_key]) > 0

        if t_support and f_support:
            return BelnapValue.BOTH
        elif t_support:
            return BelnapValue.TRUE
        elif f_support:
            return BelnapValue.FALSE
        return BelnapValue.NEITHER


class MerkleAshArchive:
    """
    Dual-Persisted Ash Archive backed by SQLite WAL with Merkle DAG chaining
    and append-only NDJSON stream mirroring.
    Guarantees Lex I (Never-Overwrite Doctrine) and multithreaded lock safety.
    """
    GENESIS_HASH = "0" * 64

    def __init__(self, db_path: str = ":memory:", ndjson_path: Optional[Path] = None):
        self.db_path = str(db_path)
        self.ndjson_path = Path(ndjson_path) if ndjson_path else None
        if self.ndjson_path:
            self.ndjson_path.parent.mkdir(parents=True, exist_ok=True)

        self._lock = threading.Lock()
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.execute("PRAGMA foreign_keys=ON;")
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock, self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS ash_archive (
                    node_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    node_hash TEXT NOT NULL UNIQUE,
                    parent_hash TEXT NOT NULL,
                    atom_key TEXT NOT NULL,
                    lamport_clock INTEGER NOT NULL,
                    belnap_state TEXT NOT NULL,
                    register TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    commit_timestamp REAL NOT NULL
                );
            """)
            self.conn.execute("""
                CREATE TRIGGER IF NOT EXISTS prevent_ash_archive_update
                BEFORE UPDATE ON ash_archive
                BEGIN
                    SELECT RAISE(FAIL, 'Lex I Violation: Ash Archive is strictly append-only. Mutation forbidden.');
                END;
            """)
            self.conn.execute("""
                CREATE TRIGGER IF NOT EXISTS prevent_ash_archive_delete
                BEFORE DELETE ON ash_archive
                BEGIN
                    SELECT RAISE(FAIL, 'Lex I Violation: Ash Archive is strictly append-only. Deletion forbidden.');
                END;
            """)

    def get_tip_hash(self) -> str:
        with self._lock:
            cur = self.conn.cursor()
            cur.execute("SELECT node_hash FROM ash_archive ORDER BY node_id DESC LIMIT 1;")
            row = cur.fetchone()
            return row[0] if row else self.GENESIS_HASH

    def compute_merkle_node_hash(self, parent_hash: str, atom_key: str, lamport: int, belnap_state: str, payload_str: str) -> str:
        hasher = hashlib.sha256()
        hasher.update(parent_hash.encode("utf-8"))
        hasher.update(atom_key.encode("utf-8"))
        hasher.update(str(lamport).encode("utf-8"))
        hasher.update(belnap_state.encode("utf-8"))
        hasher.update(payload_str.encode("utf-8"))
        return hasher.hexdigest()

    def commit(self, event: EventEnvelope, belnap_state: BelnapValue) -> str:
        payload_dict = event.serialize_payload()
        payload_str = json.dumps(payload_dict, sort_keys=True)

        with self._lock:
            cur = self.conn.cursor()
            cur.execute("SELECT node_hash FROM ash_archive ORDER BY node_id DESC LIMIT 1;")
            tip_row = cur.fetchone()
            parent_hash = tip_row[0] if tip_row else self.GENESIS_HASH

            node_hash = self.compute_merkle_node_hash(
                parent_hash=parent_hash,
                atom_key=event.atom_key,
                lamport=event.lamport_clock,
                belnap_state=belnap_state.value,
                payload_str=payload_str
            )
            commit_ts = time.time()

            register = (
                EpistemicRegisterTag.SCAR.value
                if belnap_state == BelnapValue.BOTH
                else event.register.value
            )

            # Atomic SQLite Commit
            with self.conn:
                self.conn.execute("""
                    INSERT INTO ash_archive (
                        node_hash, parent_hash, atom_key, lamport_clock,
                        belnap_state, register, payload_json, commit_timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    node_hash,
                    parent_hash,
                    event.atom_key,
                    event.lamport_clock,
                    belnap_state.value,
                    register,
                    payload_str,
                    commit_ts
                ))

        # Append-Only NDJSON Dual-Mirroring
        if self.ndjson_path:
            ndjson_record = {
                "node_hash": node_hash,
                "parent_hash": parent_hash,
                "atom_key": event.atom_key,
                "lamport_clock": event.lamport_clock,
                "belnap_state": belnap_state.value,
                "register": register,
                "commit_timestamp": commit_ts,
                "payload": payload_dict
            }
            with open(self.ndjson_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(ndjson_record, sort_keys=True) + "\n")

        return node_hash

    def verify_dag_integrity(self) -> Tuple[bool, str]:
        with self._lock:
            cur = self.conn.cursor()
            cur.execute("""
                SELECT node_id, node_hash, parent_hash, atom_key, lamport_clock, belnap_state, payload_json
                FROM ash_archive ORDER BY node_id ASC;
            """)
            rows = cur.fetchall()

        expected_parent = self.GENESIS_HASH

        for row in rows:
            node_id, node_hash, parent_hash, atom_key, lamport, belnap, payload = row
            if parent_hash != expected_parent:
                return False, f"Broken chain at node_id {node_id}: expected parent {expected_parent}, found {parent_hash}"

            expected_hash = self.compute_merkle_node_hash(parent_hash, atom_key, lamport, belnap, payload)
            if expected_hash != node_hash:
                return False, f"Hash mismatch at node_id {node_id}: expected {expected_hash}, stored {node_hash}"

            expected_parent = node_hash

        return True, "Merkle DAG chain is valid and uncorrupted."
