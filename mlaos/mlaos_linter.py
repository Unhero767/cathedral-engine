from __future__ import annotations
from typing import Any, Dict, List
from mlaos_ledger import MLAOSPersistentLedger, CANONICAL_STATUS, REALITY_LEVELS

class MLAOSLinter:
    """Ontology Linter Ω enforcing complexity and structural invariants."""

    def __init__(self, ledger: MLAOSPersistentLedger) -> None:
        self.ledger = ledger

    def lint_all(self) -> List[Dict[str, str]]:
        issues: List[Dict[str, str]] = []
        entities = self.ledger.list_entities()
        known_entity_ids = {ent["entity_id"] for ent in entities}

        for ent_summary in entities:
            entity_id = ent_summary["entity_id"]
            state = self.ledger.current_state(entity_id)

            for dep in state.get("dependencies", []):
                if dep not in known_entity_ids:
                    issues.append({
                        "entity_id": entity_id,
                        "issue": "MISSING_DEPENDENCY",
                        "detail": f"Reference points to non-existent entity: {dep}"
                    })

            if state.get("canonical_status") not in CANONICAL_STATUS:
                issues.append({
                    "entity_id": entity_id,
                    "issue": "INVALID_CANONICAL_STATUS",
                    "detail": f"Unknown status: {state.get('canonical_status')}"
                })

            if state.get("reality_level") not in REALITY_LEVELS:
                issues.append({
                    "entity_id": entity_id,
                    "issue": "INVALID_REALITY_LEVEL",
                    "detail": f"Unknown reality level: {state.get('reality_level')}"
                })

            if state.get("reality_level") in {"R3", "R4", "R5"}:
                if not state.get("implementation_path"):
                    issues.append({
                        "entity_id": entity_id,
                        "issue": "MISSING_IMPLEMENTATION_PATH",
                        "detail": f"Entity is marked at {state.get('reality_level')} but lacks an implementation path (C-08)."
                    })

        return issues