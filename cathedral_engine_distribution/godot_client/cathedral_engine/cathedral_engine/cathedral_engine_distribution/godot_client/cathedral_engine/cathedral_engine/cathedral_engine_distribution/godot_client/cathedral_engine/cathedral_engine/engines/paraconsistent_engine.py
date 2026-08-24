import os
import json
import time
import random
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional

class BelnapDunnTruthState:
    TRUE = "T"
    FALSE = "F"
    BOTH = "Both"   # Dialetheic Contradiction / Harmonic Scar
    NONE = "None"   # Paraconsistent Vacuum

class EAS03ParaconsistentEngine:
    """
    EAS-03 Paraconsistent Collision & Harmonic Scar Engine
    Implements 60 Hz frame collision detection, Belnap-Dunn 4-valued logic,
    and SHA-256 Merkle DAG state persistence.
    """
    def __init__(self, ledger_path: Optional[str] = None):
        if ledger_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ledger_path = os.path.join(base_dir, "strata", "prime_ledger.ndjson")
        self.ledger_path = ledger_path
        self.pressure = 0.0
        self.fog_level = 0.0
        self.crystallized_scars = 0
        self.last_merkle_hash = "0x35_OBSIDIAN_SCAR_EAS03_F3600_8A9B"
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)

    def compute_belnap_dunn_state(self, c_pos: float, c_neg: float) -> str:
        """Evaluates Belnap-Dunn 4-valued lattice truth state."""
        if c_pos > 0.5 and c_neg > 0.5:
            return BelnapDunnTruthState.BOTH
        elif c_pos > 0.5:
            return BelnapDunnTruthState.TRUE
        elif c_neg > 0.5:
            return BelnapDunnTruthState.FALSE
        else:
            return BelnapDunnTruthState.NONE

    def compute_merkle_hash(self, prev_hash: str, payload_str: str) -> str:
        """Computes SHA-256 Merkle root hash."""
        hasher = hashlib.sha256()
        hasher.update(prev_hash.encode("utf-8"))
        hasher.update(payload_str.encode("utf-8"))
        return "0x" + hasher.hexdigest()[:32].upper()

    def process_frame_tick(self, frame_id: int, c_pos: Optional[float] = None, c_neg: Optional[float] = None) -> Dict[str, Any]:
        """Processes a single 60 Hz frame cycle."""
        start_ns = time.perf_counter_ns()

        if c_pos is None:
            c_pos = random.uniform(0.1, 0.95)
        if c_neg is None:
            c_neg = random.uniform(0.1, 0.95)

        truth_state = self.compute_belnap_dunn_state(c_pos, c_neg)
        scar_recorded = False

        if truth_state == BelnapDunnTruthState.BOTH:
            self.crystallized_scars += 1
            scar_recorded = True
            delta_p = (c_pos + c_neg) * 0.05
            self.pressure = min(1.0, self.pressure + delta_p)
            self.fog_level = min(1.0, self.fog_level + 0.02)
        else:
            self.pressure = max(0.0, self.pressure - 0.01)
            self.fog_level = max(0.0, self.fog_level - 0.005)

        payload_dict = {
            "frame": frame_id,
            "truth_state": truth_state,
            "c_pos": round(c_pos, 4),
            "c_neg": round(c_neg, 4),
            "pressure": round(self.pressure, 4),
            "fog": round(self.fog_level, 4),
            "scars": self.crystallized_scars
        }
        
        self.last_merkle_hash = self.compute_merkle_hash(self.last_merkle_hash, json.dumps(payload_dict, sort_keys=True))

        elapsed_us = (time.perf_counter_ns() - start_ns) / 1000.0

        if scar_recorded:
            self.inscribe_stratum(frame_id, truth_state, payload_dict)

        return {
            "frame": frame_id,
            "state": truth_state,
            "c_pos": round(c_pos, 4),
            "c_neg": round(c_neg, 4),
            "pressure": round(self.pressure, 4),
            "fog": round(self.fog_level, 4),
            "scars": self.crystallized_scars,
            "merkle_tip": self.last_merkle_hash,
            "latency_us": round(elapsed_us, 2)
        }

    def inscribe_stratum(self, frame_id: int, state: str, metrics: Dict[str, Any]):
        """Inscribes a permanent stratum entry into the Ash Archive ledger."""
        stratum = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "chapter": "IV. Shadow Canon",
            "thesis": "EAS-03 Paraconsistent Collision Frame",
            "spectrum": "Bronze-Obsidian/Null",
            "phi": 0.0,
            "dialetheic_active": True,
            "payload": f"HARMONIC SCAR #{self.crystallized_scars} [Frame {frame_id}]: Lattice State {state} | Merkle {self.last_merkle_hash}",
            "metrics": metrics
        }
        try:
            with open(self.ledger_path, "a") as f:
                f.write(json.dumps(stratum) + chr(10))
        except Exception as e:
            print(f"[ERROR] Failed to inscribe stratum: {e}")

    def run_harness(self, total_frames: int = 60) -> Dict[str, Any]:
        """Runs a batch benchmark of the 60 Hz collision harness."""
        print(f"[EAS-03] Initializing {total_frames}-Frame Collision Stress Harness...")
        results = []
        for i in range(1, total_frames + 1):
            res = self.process_frame_tick(i)
            results.append(res)
        
        avg_latency = sum(r["latency_us"] for r in results) / len(results)
        print(f"[EAS-03] Harness Completed. Scars: {self.crystallized_scars}, Merkle Tip: {self.last_merkle_hash}, Avg Latency: {avg_latency:.2f} µs")
        return {
            "total_frames": total_frames,
            "crystallized_scars": self.crystallized_scars,
            "final_pressure": round(self.pressure, 4),
            "final_fog": round(self.fog_level, 4),
            "merkle_tip": self.last_merkle_hash,
            "avg_latency_us": round(avg_latency, 2)
        }

if __name__ == "__main__":
    engine = EAS03ParaconsistentEngine()
    engine.run_harness(120)
