#!/usr/bin/env python3
"""
Ash Archive Merkle DAG & Ledger Verifier (verify_ash_dag.py - v1.2.0)
===================================================================
Dallmier Tech Venture (Olney, Illinois)
Lex I Compliance: Merkle Lineage & Somatic Cadence Verification
"""

from __future__ import annotations
import argparse, hashlib, json, shutil, sqlite3, sys, time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

GENESIS_HASH: str = "0" * 64
EXPECTED_PULSE_HZ: float = 1.50
EXPECTED_INTERVAL: float = 1.0 / EXPECTED_PULSE_HZ

class AshLedgerVerifier:
    def __init__(self, pulse_tolerance: float = 0.25) -> None:
        self.pulse_tolerance = pulse_tolerance
        self.records: List[Dict[str, Any]] = []

    def load_ndjson(self, file_path: Path) -> int:
        self.records.clear()
        with open(file_path, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, start=1):
                clean = line.strip()
                if not clean: continue
                data = json.loads(clean)
                data["_source_idx"] = idx
                self.records.append(data)
        return len(self.records)

    def load_sqlite(self, db_path: Path, table_name: Optional[str] = None) -> int:
        self.records.clear()
        target_path = db_path.resolve()

        # Connect with standard fallback for active WAL journal recovery
        try:
            conn = sqlite3.connect(f"file:{target_path}?mode=ro", uri=True)
            conn.execute("SELECT 1;")
        except (sqlite3.OperationalError, sqlite3.DatabaseError):
            temp_copy = Path(f"/tmp/ash_verify_{time.time_ns()}.db")
            shutil.copy2(target_path, temp_copy)
            conn = sqlite3.connect(str(temp_copy))

        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        if not table_name:
            cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = [r[0] for r in cur.fetchall()]
            for cand in ["ash_ledger", "Ash_Archive_Nodes", "ash_archive_nodes", "ledger", "nodes"]:
                if cand in tables:
                    table_name = cand
                    break
            if not table_name and tables:
                table_name = tables[0]

        if not table_name:
            conn.close()
            return 0

        cur.execute(f"PRAGMA table_info({table_name});")
        cols = [r["name"] for r in cur.fetchall()]
        order_col = "rowid ASC"
        for cand in ["id", "block_height", "height", "timestamp"]:
            if cand in cols:
                order_col = f"{cand} ASC"
                break

        cur.execute(f"SELECT * FROM {table_name} ORDER BY {order_col};")
        for idx, row in enumerate(cur.fetchall()):
            d = dict(row)
            d["_source_idx"] = idx
            self.records.append(d)

        conn.close()
        return len(self.records)

    def verify(self, strict_pulse: bool = False) -> Dict[str, Any]:
        if not self.records:
            return {"status": "FAILED", "total_records": 0, "error": "Ledger is empty"}

        violations: List[str] = []
        pulse_intervals: List[float] = []
        prev_hash: Optional[str] = None
        prev_ts: Optional[float] = None

        for idx, rec in enumerate(self.records):
            rec_id = rec.get("node_id") or rec.get("id") or rec.get("_source_idx")
            parent_hash = (rec.get("parent_hash") or rec.get("parent") or "").strip()
            stored_hash = (
                rec.get("current_hash")
                or rec.get("merkle_leaf_hash")
                or rec.get("merkle_hash")
                or rec.get("leaf_hash")
                or rec.get("hash")
                or ""
            ).strip()

            # Check Merkle Parent Lineage
            if idx == 0:
                if parent_hash and parent_hash != GENESIS_HASH:
                    violations.append(f"Genesis Block (ID: {rec_id}): Invalid parent {parent_hash} (Expected {GENESIS_HASH})")
            else:
                if prev_hash and parent_hash != prev_hash:
                    violations.append(f"Block {idx} (ID: {rec_id}): Lineage fracture! Parent {parent_hash} does not match predecessor tip {prev_hash}")

            # Monotonicity and Cadence Analysis
            raw_ts = rec.get("timestamp") or rec.get("created_at") or rec.get("create_ts")
            curr_ts = self._extract_epoch(raw_ts)

            if curr_ts is not None:
                if prev_ts is not None:
                    delta_t = curr_ts - prev_ts
                    if delta_t < -1e-6:
                        violations.append(f"Block {idx} (ID: {rec_id}): Temporal non-monotonicity! {curr_ts} < {prev_ts}")
                    else:
                        pulse_intervals.append(delta_t)
                        if strict_pulse and delta_t > 0:
                            min_t = EXPECTED_INTERVAL * (1.0 - self.pulse_tolerance)
                            max_t = EXPECTED_INTERVAL * (1.0 + self.pulse_tolerance)
                            if not (min_t <= delta_t <= max_t):
                                violations.append(f"Block {idx} (ID: {rec_id}): Pulse cadence anomaly! {delta_t:.4f}s outside [{min_t:.4f}s, {max_t:.4f}s]")
                prev_ts = curr_ts

            if stored_hash:
                prev_hash = stored_hash

        avg_pulse = sum(pulse_intervals) / len(pulse_intervals) if pulse_intervals else 0.0
        eff_hz = (1.0 / avg_pulse) if avg_pulse > 0 else 0.0
        passed = len(violations) == 0

        return {
            "status": "VERIFIED" if passed else "CORRUPTED",
            "total_blocks": len(self.records),
            "merkle_tip": prev_hash or GENESIS_HASH,
            "average_pulse_sec": round(avg_pulse, 6),
            "effective_hz": round(eff_hz, 4),
            "lex_i_compliance": passed,
            "violations_count": len(violations),
            "violations": violations[:20]
        }

    def _extract_epoch(self, val: Any) -> Optional[float]:
        if val is None: return None
        if isinstance(val, (int, float)): return float(val)
        if isinstance(val, str):
            try: return datetime.fromisoformat(val.replace("Z", "+00:00")).timestamp()
            except ValueError:
                try: return float(val)
                except ValueError: return None
        return None

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sqlite", type=Path)
    p.add_argument("--ndjson", type=Path)
    p.add_argument("--table", type=str)
    p.add_argument("--strict-pulse", action="store_true")
    p.add_argument("--json-report", action="store_true")
    args = p.parse_args()

    v = AshLedgerVerifier()
    if args.sqlite: v.load_sqlite(args.sqlite, args.table)
    elif args.ndjson: v.load_ndjson(args.ndjson)
    else: sys.exit(1)

    res = v.verify(strict_pulse=args.strict_pulse)
    if args.json_report: print(json.dumps(res, indent=2))
    else: print(f"[{res['status']}] Blocks: {res['total_blocks']} | Tip: {res['merkle_tip'][:16]}... | Violations: {res['violations_count']}")
    sys.exit(0 if res["status"] == "VERIFIED" else 1)

if __name__ == "__main__":
    main()
