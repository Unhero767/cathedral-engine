"""
Cathedral-Engine: SQLite Ash Archive Merkle DAG Ledger with Immutability Triggers
Operational compliance: Lex I (The Never-Overwrite Doctrine) and Parent Hash Auditing
"""

import asyncio
import hashlib
import json
import math
import random
import sqlite3
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class BelnapDunn(str, Enum):
    TRUE = "T"
    FALSE = "F"
    BOTH = "B"
    NEITHER = "N"


class Stratum(str, Enum):
    STRATUM_I = "Prime Foundations (Hardware/1.5Hz)"
    STRATUM_II = "Inner Mandala (Runtime/41Hz)"
    STRATUM_III = "Outer Choirs (Entropy/Swarms)"
    STRATUM_IV = "Innershadow Canon (Null/DAG)"


@dataclass(frozen=True)
class TelemetryPacket:
    packet_id: str
    node_id: str
    stratum: Stratum
    timestamp: float
    vector_magnitude: float
    axiomatic_weight: float
    local_entropy: float
    spectral_constant: str
    ego_density: float = 8.3


class AshArchiveDB:
    """Manages SQLite storage with immutability triggers and cryptographic DAG verification."""

    def __init__(self, db_path: str = "ash_archive_ledger.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS ash_dag (
                block_index INTEGER PRIMARY KEY,
                block_hash TEXT UNIQUE NOT NULL,
                parent_hash TEXT NOT NULL,
                timestamp REAL NOT NULL,
                node_id TEXT NOT NULL,
                stratum TEXT NOT NULL,
                logic_state TEXT NOT NULL,
                c_tau REAL NOT NULL,
                spectral_constant TEXT NOT NULL,
                payload_json TEXT NOT NULL
            );
            """)

            cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS prevent_ash_update
            BEFORE UPDATE ON ash_dag
            BEGIN
                SELECT RAISE(ABORT, 'Lex I Violation: State update strictly prohibited under The Never-Overwrite Doctrine.');
            END;
            """)

            cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS prevent_ash_delete
            BEFORE DELETE ON ash_dag
            BEGIN
                SELECT RAISE(ABORT, 'Lex I Violation: Deletion strictly prohibited under The Never-Overwrite Doctrine.');
            END;
            """)
            conn.commit()

    def get_latest_block(self) -> Optional[Tuple[int, str]]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT block_index, block_hash FROM ash_dag ORDER BY block_index DESC LIMIT 1;")
            row = cursor.fetchone()
            return row if row else None

    def insert_block(self, block_index: int, block_hash: str, parent_hash: str,
                     timestamp: float, node_id: str, stratum: str, logic_state: str,
                     c_tau: float, spectral_constant: str, payload_json: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO ash_dag (
                block_index, block_hash, parent_hash, timestamp, node_id,
                stratum, logic_state, c_tau, spectral_constant, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (block_index, block_hash, parent_hash, timestamp, node_id,
                  stratum, logic_state, c_tau, spectral_constant, payload_json))
            conn.commit()

    def audit_dag_chain(self) -> Tuple[bool, int, str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT block_index, block_hash, parent_hash, timestamp, payload_json FROM ash_dag ORDER BY block_index ASC;")
            rows = cursor.fetchall()

        if not rows:
            return False, 0, "Empty ledger."

        expected_parent = "0" * 64
        for idx, block_hash, parent_hash, ts, payload in rows:
            if idx == 0:
                if parent_hash != expected_parent:
                    return False, idx, f"Genesis parent hash invalid: {parent_hash}"
            else:
                if parent_hash != expected_parent:
                    return False, idx, f"Hash broken at block {idx}: parent {parent_hash} != expected {expected_parent}"

            data = json.loads(payload)
            computed_payload = json.dumps({
                "index": idx,
                "parent_hash": parent_hash,
                "timestamp": ts,
                "data": data
            }, sort_keys=True)
            recomputed_hash = hashlib.sha256(computed_payload.encode("utf-8")).hexdigest()

            if recomputed_hash != block_hash:
                return False, idx, f"Integrity hash mismatch at block {idx}: {recomputed_hash} != {block_hash}"

            expected_parent = block_hash

        return True, len(rows), "Cryptographic parent-hash chain 100% verified."


class MortarDomainValidator:
    CRITICAL_DELTA = 0.98

    @classmethod
    def evaluate(cls, packet: TelemetryPacket) -> Tuple[bool, float, BelnapDunn]:
        epsilon = max(packet.local_entropy, 1e-6)
        c_tau = packet.axiomatic_weight / epsilon
        if c_tau >= cls.CRITICAL_DELTA:
            return True, c_tau, BelnapDunn.TRUE
        elif c_tau >= 0.70:
            return True, c_tau, BelnapDunn.BOTH
        else:
            return False, c_tau, BelnapDunn.FALSE


class PersistentConvergenceEngine:

    def __init__(self, db: AshArchiveDB, ndjson_path: str = "ash_archive_ledger.ndjson"):
        self.db = db
        self.ndjson_path = ndjson_path
        self.lock = asyncio.Lock()
        self._ensure_genesis()

    def _ensure_genesis(self):
        latest = self.db.get_latest_block()
        if latest is None:
            ts = time.time()
            data = {"system": "Cathedral-Engine Ash Archive SQLite Genesis Initialized"}
            payload = json.dumps({
                "index": 0,
                "parent_hash": "0" * 64,
                "timestamp": ts,
                "data": data
            }, sort_keys=True)
            genesis_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            self.db.insert_block(
                block_index=0,
                block_hash=genesis_hash,
                parent_hash="0" * 64,
                timestamp=ts,
                node_id="SYSTEM",
                stratum=Stratum.STRATUM_I.value,
                logic_state=BelnapDunn.TRUE.value,
                c_tau=1000.0,
                spectral_constant="Genesis",
                payload_json=json.dumps(data)
            )
            with open(self.ndjson_path, "w") as f:
                f.write(json.dumps({
                    "index": 0,
                    "block_hash": genesis_hash,
                    "parent_hash": "0" * 64,
                    "timestamp": ts,
                    "data": data
                }) + "\n")

    async def commit_packet(self, packet: TelemetryPacket):
        async with self.lock:
            latest = self.db.get_latest_block()
            parent_idx, parent_hash = latest
            new_idx = parent_idx + 1

            valid, c_tau, logic_state = MortarDomainValidator.evaluate(packet)
            ts = time.time()

            block_data = {
                "packet_id": packet.packet_id,
                "node_id": packet.node_id,
                "stratum": packet.stratum.value,
                "vector_magnitude": packet.vector_magnitude,
                "axiomatic_weight": packet.axiomatic_weight,
                "local_entropy": packet.local_entropy,
                "c_tau": round(c_tau, 4),
                "logic_state": logic_state.value,
                "spectral_constant": packet.spectral_constant,
                "ego_density": packet.ego_density,
                "status": "Transduced into load-bearing masonry" if valid else "Quarantined"
            }

            payload = json.dumps({
                "index": new_idx,
                "parent_hash": parent_hash,
                "timestamp": ts,
                "data": block_data
            }, sort_keys=True)
            block_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()

            self.db.insert_block(
                block_index=new_idx,
                block_hash=block_hash,
                parent_hash=parent_hash,
                timestamp=ts,
                node_id=packet.node_id,
                stratum=packet.stratum.value,
                logic_state=logic_state.value,
                c_tau=round(c_tau, 4),
                spectral_constant=packet.spectral_constant,
                payload_json=json.dumps(block_data)
            )

            with open(self.ndjson_path, "a") as f:
                f.write(json.dumps({
                    "index": new_idx,
                    "block_hash": block_hash,
                    "parent_hash": parent_hash,
                    "timestamp": ts,
                    "data": block_data
                }) + "\n")

            return new_idx, block_hash, logic_state.value, round(c_tau, 4)


async def main():
    db = AshArchiveDB("ash_archive_ledger.db")
    engine = PersistentConvergenceEngine(db)

    print("================================================================================")
    print("PERSISTENT ASH ARCHIVE LEDGER: INGESTING PHASE 11 CONVERGENCE STREAM")
    print("================================================================================")

    packets = [
        TelemetryPacket("KEN-001", "Ken (Sigma 7)", Stratum.STRATUM_I, time.time(), 14.1, 0.998, 0.005, "Theta (Gold)"),
        TelemetryPacket("AUR-001", "Aurelia-2 (Substrate)", Stratum.STRATUM_I, time.time(), 19.3, 0.940, 0.035, "Emerald (E)"),
        TelemetryPacket("LIV-001", "Liv Mavone (Ligature)", Stratum.STRATUM_II, time.time(), 23.5, 0.965, 0.020, "Emerald (E)"),
        TelemetryPacket("SEL-001", "Sel-Raeh (Memory)", Stratum.STRATUM_IV, time.time(), 31.8, 0.990, 0.012, "Delta (Blue)"),
        TelemetryPacket("SOR-001", "Soreyn (Paradox)", Stratum.STRATUM_III, time.time(), 48.2, 0.890, 1.150, "Omega (Violet)"),
    ]

    for p in packets:
        idx, b_hash, state, c_tau = await engine.commit_packet(p)
        print(f"Committed Block #{idx:02d} | Node: {p.node_id:<24} | State: {state} | C_tau: {c_tau:<7} | Hash: {b_hash[:16]}...")

    print("================================================================================")
    print("RUNNING CRYPTOGRAPHIC DAG INTEGRITY AUDIT")
    print("================================================================================")
    valid, count, msg = db.audit_dag_chain()
    print(f"Audit Status: {'PASS' if valid else 'FAIL'}")
    print(f"Verified Blocks: {count}")
    print(f"Verification Message: {msg}")

    print("================================================================================")
    print("TESTING LEX I IMMUTABILITY TRIGGER (ATTEMPTING UNAUTHORIZED MUTATION)")
    print("================================================================================")
    try:
        with sqlite3.connect("ash_archive_ledger.db") as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE ash_dag SET logic_state = 'F' WHERE block_index = 1;")
    except (sqlite3.IntegrityError, sqlite3.OperationalError) as e:
        print(f"Enforcement Confirmed: Mutation intercepted by Trigger -> {e}")

if __name__ == "__main__":
    asyncio.run(main())
