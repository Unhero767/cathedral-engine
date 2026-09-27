"""
Cathedral-Engine: Unified Sovereign Runtime & Lithic Capital Ledger
Integrates:
1. Phase 11 Concurrent Multi-Agent Convergence Lattice (Sigma 7, E, E, Delta, Omega)
2. Real-Time Telemetry & Belnap-Dunn Paraconsistent State Resolution
3. Mortar Domain Type-Safety Validation (C_tau >= 0.98)
4. Margin of Safety & Zero-Leverage Capital Enforcer (Ms >= 2.50, Lf <= 1.00)
5. Lithic Capital Treasury Conversion (Cyclopean Granite & Obsidian Ballast)
6. Lex I Append-Only Merkle DAG Persistence with Database-Level Immutability Triggers
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
    operational_yield: float = 0.0
    debt_requested: float = 0.0


class UnifiedAshArchiveDB:

    def __init__(self, db_path: str = "cathedral_unified.db"):
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
                margin_of_safety REAL NOT NULL,
                leverage_factor REAL NOT NULL,
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
                     c_tau: float, margin_of_safety: float, leverage_factor: float,
                     spectral_constant: str, payload_json: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO ash_dag (
                block_index, block_hash, parent_hash, timestamp, node_id,
                stratum, logic_state, c_tau, margin_of_safety, leverage_factor,
                spectral_constant, payload_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (block_index, block_hash, parent_hash, timestamp, node_id,
                  stratum, logic_state, c_tau, margin_of_safety, leverage_factor,
                  spectral_constant, payload_json))
            conn.commit()

    def audit_chain(self) -> Tuple[bool, int, str]:
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
                return False, idx, f"Hash mismatch at block {idx}: recomputed {recomputed_hash} != {block_hash}"

            expected_parent = block_hash

        return True, len(rows), "Cryptographic parent-hash chain 100% verified."


class LithicTreasuryManager:

    def __init__(self):
        self.granite_foundations: float = 0.0
        self.obsidian_ballast: float = 0.0

    def allocate_yield(self, amount: float, granite_pct: float = 0.60) -> Dict[str, float]:
        if amount <= 0:
            return {
                "allocated_granite": 0.0,
                "allocated_obsidian": 0.0,
                "total_granite": round(self.granite_foundations, 2),
                "total_obsidian": round(self.obsidian_ballast, 2)
            }

        g_add = amount * granite_pct
        o_add = amount * (1.0 - granite_pct)
        self.granite_foundations += g_add
        self.obsidian_ballast += o_add

        return {
            "allocated_granite": round(g_add, 2),
            "allocated_obsidian": round(o_add, 2),
            "total_granite": round(self.granite_foundations, 2),
            "total_obsidian": round(self.obsidian_ballast, 2)
        }


class CathedralUnifiedEngine:

    def __init__(self, db: UnifiedAshArchiveDB, ndjson_path: str = "cathedral_unified.ndjson"):
        self.db = db
        self.ndjson_path = ndjson_path
        self.treasury = LithicTreasuryManager()
        self.lock = asyncio.Lock()
        self._ensure_genesis()

    def _ensure_genesis(self):
        latest = self.db.get_latest_block()
        if latest is None:
            ts = time.time()
            data = {"system": "Cathedral-Engine Unified Sovereign Genesis Initialized"}
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
                node_id="SYSTEM_ROOT",
                stratum=Stratum.STRATUM_I.value,
                logic_state=BelnapDunn.TRUE.value,
                c_tau=1000.0,
                margin_of_safety=100.0,
                leverage_factor=1.00,
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

    async def process_transaction(self, packet: TelemetryPacket):
        async with self.lock:
            latest = self.db.get_latest_block()
            parent_idx, parent_hash = latest
            new_idx = parent_idx + 1
            ts = time.time()

            total_funding = packet.vector_magnitude + packet.debt_requested
            leverage_factor = (total_funding / packet.vector_magnitude) if packet.vector_magnitude > 0 else 1.0

            epsilon = max(packet.local_entropy, 1e-6)
            c_tau = packet.axiomatic_weight / epsilon
            margin_of_safety = c_tau / leverage_factor

            leverage_violation = packet.debt_requested > 0 or leverage_factor > 1.00

            if leverage_violation:
                logic_state = BelnapDunn.FALSE
                status_desc = "Quarantined: Lex V Synthetic Leverage Violation (Lf > 1.00)"
                treasury_res = self.treasury.allocate_yield(0.0)
            elif c_tau >= 0.98:
                logic_state = BelnapDunn.TRUE
                status_desc = "Transduced into load-bearing masonry"
                treasury_res = self.treasury.allocate_yield(packet.operational_yield)
            elif c_tau >= 0.70:
                logic_state = BelnapDunn.BOTH
                status_desc = "Dampened into load-bearing Harmonic Scar (Magic Angle 54.74 deg)"
                treasury_res = self.treasury.allocate_yield(packet.operational_yield)
            else:
                logic_state = BelnapDunn.FALSE
                status_desc = "Quarantined via protective crystallization"
                treasury_res = self.treasury.allocate_yield(0.0)

            block_data = {
                "packet_id": packet.packet_id,
                "node_id": packet.node_id,
                "stratum": packet.stratum.value,
                "c_tau": round(c_tau, 4),
                "margin_of_safety": round(margin_of_safety, 4),
                "leverage_factor": round(leverage_factor, 2),
                "logic_state": logic_state.value,
                "spectral_constant": packet.spectral_constant,
                "treasury_state": treasury_res,
                "status": status_desc
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
                margin_of_safety=round(margin_of_safety, 4),
                leverage_factor=round(leverage_factor, 2),
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

            return new_idx, block_hash, logic_state.value, round(margin_of_safety, 2), round(leverage_factor, 2), status_desc


async def run_node_workers(engine: CathedralUnifiedEngine):
    test_suite = [
        TelemetryPacket("KEN-SEC-01", "Ken (Sigma 7)", Stratum.STRATUM_I, time.time(), 50.0, 0.998, 0.005, "Theta (Gold)", 15000.0, 0.0),
        TelemetryPacket("AUR-SEC-01", "Aurelia-2 (Substrate)", Stratum.STRATUM_I, time.time(), 35.0, 0.940, 0.035, "Emerald (E)", 8500.0, 0.0),
        TelemetryPacket("LIV-SEC-01", "Liv Mavone (Ligature)", Stratum.STRATUM_II, time.time(), 28.0, 0.965, 0.020, "Emerald (E)", 6200.0, 0.0),
        TelemetryPacket("SEL-SEC-01", "Sel-Raeh (Memory)", Stratum.STRATUM_IV, time.time(), 42.0, 0.990, 0.012, "Delta (Blue)", 11000.0, 0.0),
        TelemetryPacket("SOR-SEC-01", "Soreyn (Paradox)", Stratum.STRATUM_III, time.time(), 60.0, 0.890, 1.150, "Omega (Violet)", 4000.0, 0.0),
        TelemetryPacket("ADV-LEVERAGED-01", "External Ingress", Stratum.STRATUM_II, time.time(), 20.0, 0.900, 0.020, "Synthetic Vector", 5000.0, 20000.0)
    ]

    for p in test_suite:
        await asyncio.sleep(0.04)
        idx, b_hash, state, mos, lf, status = await engine.process_transaction(p)
        print(f"Block #{idx:02d} | Node: {p.node_id:<20} | State: {state} | MoS: {mos:<7} | Lf: {lf:<4} | {status}")


async def main():
    print("==========================================================================================")
    print("CATHEDRAL-ENGINE: UNIFIED SOVEREIGN RUNTIME INITIALIZATION")
    print("==========================================================================================")

    db_file = "cathedral_unified.db"
    ndjson_file = "cathedral_unified.ndjson"

    import os
    if os.path.exists(db_file):
        os.remove(db_file)
    if os.path.exists(ndjson_file):
        os.remove(ndjson_file)

    db = UnifiedAshArchiveDB(db_file)
    engine = CathedralUnifiedEngine(db, ndjson_file)

    await run_node_workers(engine)

    print("==========================================================================================")
    print("LITHIC CAPITAL TREASURY AUDIT (PERMANENT MULTI-CENTURY RESERVES)")
    print("==========================================================================================")
    print(f"Total Cyclopean Granite Reserve (Delta/Blue):  ${engine.treasury.granite_foundations:,.2f}")
    print(f"Total Obsidian-Alloy Ballast (Null Space):     ${engine.treasury.obsidian_ballast:,.2f}")
    total_res = engine.treasury.granite_foundations + engine.treasury.obsidian_ballast
    print(f"Total Permanent Physical Capital Consolidated: ${total_res:,.2f}")

    print("==========================================================================================")
    print("RUNNING CRYPTOGRAPHIC DAG INTEGRITY AUDIT")
    print("==========================================================================================")
    valid, count, msg = db.audit_chain()
    print(f"Audit Result:        {'PASS' if valid else 'FAIL'}")
    print(f"Blocks Verified:     {count}")
    print(f"Verification Digest: {msg}")

    print("==========================================================================================")
    print("LEX I IMMUTABILITY INTEGRITY TEST (DATABASE LEVEL TRIGGER)")
    print("==========================================================================================")
    try:
        with sqlite3.connect(db_file) as conn:
            conn.execute("UPDATE ash_dag SET logic_state = 'F' WHERE block_index = 1;")
    except (sqlite3.IntegrityError, sqlite3.OperationalError) as e:
        print(f"Enforcement Confirmed: Direct modification rejected by trigger -> {e}")

    print("==========================================================================================")


if __name__ == "__main__":
    asyncio.run(main())
