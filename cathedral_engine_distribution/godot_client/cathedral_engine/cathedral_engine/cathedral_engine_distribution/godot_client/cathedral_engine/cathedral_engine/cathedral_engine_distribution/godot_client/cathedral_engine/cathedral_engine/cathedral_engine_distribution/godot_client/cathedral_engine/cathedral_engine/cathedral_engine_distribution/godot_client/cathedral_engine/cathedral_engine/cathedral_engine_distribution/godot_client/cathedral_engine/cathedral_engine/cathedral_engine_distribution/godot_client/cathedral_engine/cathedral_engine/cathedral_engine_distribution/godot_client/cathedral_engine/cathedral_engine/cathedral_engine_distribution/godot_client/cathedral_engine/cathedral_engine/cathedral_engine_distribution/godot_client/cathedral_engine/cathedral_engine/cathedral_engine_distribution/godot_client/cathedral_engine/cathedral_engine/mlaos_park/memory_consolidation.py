from typing import Dict, Any
from datetime import datetime, timezone

class MemoryConsolidationEngine:
    def __init__(self, ledger):
        self.ledger = ledger
        self.phi_coherence_index = 0.8100

    def consolidate_cycle(self) -> Dict[str, Any]:
        self.phi_coherence_index += 0.005
        ts = datetime.now(timezone.utc).isoformat()
        merkle_root = self.ledger.append_event(
            event_type="MEMORY_CONSOLIDATED",
            aggregate_id="SPARK_CORE",
            payload={"phi_coherence": self.phi_coherence_index, "timestamp": ts}
        )
        return {
            "status": "CONSOLIDATED",
            "phi_coherence": round(self.phi_coherence_index, 4),
            "merkle_root": merkle_root,
            "timestamp": ts
        }
