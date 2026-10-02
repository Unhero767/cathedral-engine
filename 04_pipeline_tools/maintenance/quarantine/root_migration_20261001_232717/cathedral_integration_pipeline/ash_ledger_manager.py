"""
MLAOS Ash Archive & JBP Merkle Ledger Manager
"""
import json, hashlib, time, os
from typing import Dict, Any

class AshLedgerManager:
    def __init__(self, ledger_path: str = ""):
        self.ledger_path = ledger_path or os.path.join(os.path.dirname(__file__), "ash_ledger.json")
        self.ledger = self._load_or_init()

    def _load_or_init(self) -> Dict[str, Any]:
        if os.path.exists(self.ledger_path):
            try:
                with open(self.ledger_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "magisterium_version": "MLAOS-PRIME-v1.0.0",
            "doctrine": "Never-Overwrite (Book III: The Ash Archive)",
            "total_entries": 1,
            "entries": [{
                "index": 0,
                "timestamp": "2026-08-20T00:00:00Z",
                "event_type": "GENESIS_COVENANT",
                "archetype_id": "SYSTEM_CORE",
                "layer_target": "Layer_00_Skeletal",
                "telemetry": "The First Hearth ignition; baseline substrate established.",
                "prev_j_hash": "0000000000000000000000000000000000000000000000000000000000000000",
                "j_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
            }]
        }

    def append_historical_scar(self, archetype_id: str, scar_description: str, severity: float, spectral_constant: str) -> Dict[str, Any]:
        prev_entry = self.ledger["entries"][-1]
        idx = len(self.ledger["entries"])
        entry_data = {
            "index": idx,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event_type": "HISTORICAL_SCAR_INJECTION",
            "archetype_id": archetype_id,
            "layer_target": "Layer_11_Custom_Overlay",
            "severity": round(severity, 2),
            "spectral_constant": spectral_constant,
            "telemetry": scar_description,
            "prev_j_hash": prev_entry["j_hash"]
        }
        serialized = json.dumps(entry_data, sort_keys=True)
        entry_data["j_hash"] = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        self.ledger["entries"].append(entry_data)
        self.ledger["total_entries"] = len(self.ledger["entries"])
        self._save()
        return entry_data

    def _save(self):
        os.makedirs(os.path.dirname(os.path.abspath(self.ledger_path)), exist_ok=True)
        with open(self.ledger_path, "w", encoding="utf-8") as f:
            json.dump(self.ledger, f, indent=2)
