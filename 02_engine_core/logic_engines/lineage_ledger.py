import json
import hashlib
import os

class LineageLedger:
    def __init__(self, ledger_path: str = "06_strata_data/genesis_lineage_ledger.json"):
        self.ledger_path = ledger_path
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        
    def record_transition(self, state_hash: str, parent_hash: str, metadata: dict) -> str:
        block_data = {
            "parent_hash": parent_hash,
            "state_hash": state_hash,
            "metadata": metadata
        }
        block_string = json.dumps(block_data, sort_keys=True)
        current_hash = hashlib.sha256(block_string.encode('utf-8')).hexdigest()
        
        ledger = self._load_ledger()
        ledger.append({
            "block_hash": current_hash,
            **block_data
        })
        
        with open(self.ledger_path, "w") as f:
            json.dump(ledger, f, indent=2)
            
        return current_hash

    def _load_ledger(self) -> list:
        if not os.path.exists(self.ledger_path):
            return []
        with open(self.ledger_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

if __name__ == "__main__":
    ledger = LineageLedger()
    h1 = ledger.record_transition("sha256_state_001", "0" * 64, {"chamber": "Chamber I", "phase": "Potential"})
    print(f"Genesis Block Committed: {h1}")
