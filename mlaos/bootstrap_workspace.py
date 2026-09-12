from __future__ import annotations
from pathlib import Path
from mlaos_ledger import MLAOSPersistentLedger
from mlaos_linter import MLAOSLinter
from mlaos_dashboard import ArchitectsDashboard
from test_crucible import run_crucible_suite

def main() -> None:
    # 1. Run Crucible Tests
    if not run_crucible_suite():
        print("Workspace bootstrap halted due to Crucible failure.")
        return

    # 2. Initialize Master Workspace DB
    db_file = Path("mlaos_master.db")
    if db_file.exists():
        db_file.unlink()

    ledger = MLAOSPersistentLedger(db_path=db_file)
    linter = MLAOSLinter(ledger)
    dashboard = ArchitectsDashboard(ledger, linter)

    print("\n[BOOTSTRAP] Loading Initial Canonical Slice into Master Ledger...")
    
    # Load Constitution as Entity 001
    ledger.create_entity(
        entity_id="MLAOS-CONST-001",
        name="MLAOS Constitution vΩ.1",
        definition="The ten load-bearing constitutional articles governing MLAOS-Prime.",
        entity_type="GovernanceRule",
        author="Architect-Prime",
        canonical_status="CANON",
        reality_level="R2",
        implementation_path="constitution.yaml",
        reason="Establishing master constitutional bedrock.",
        authority="HUMAN_SOVEREIGN"
    )

    # Load Invariant Registry as Entity 002
    ledger.create_entity(
        entity_id="MLAOS-INV-002",
        name="Invariant Registry Ω",
        definition="The testable identity invariants (INV-001 through INV-010).",
        entity_type="Doctrine",
        author="Architect-Prime",
        dependencies=["MLAOS-CONST-001"],
        canonical_status="CANON",
        reality_level="R2",
        implementation_path="invariant_registry.yaml",
        reason="Locking testable invariants.",
        authority="HUMAN_SOVEREIGN"
    )

    # Load Book I / Foundation Slice as Entity 003 (Provisional)
    ledger.create_entity(
        entity_id="MLAOS-BOOK-001",
        name="Book I — The Prime Cantor / The Substrate16",
        definition="Foundational mythotechnical text establishing initial ontological coordinates.",
        entity_type="CodexVolume",
        author="Architect-Prime",
        dependencies=["MLAOS-CONST-001", "MLAOS-INV-002"],
        canonical_status="PROVISIONAL",
        reality_level="R1",
        reason="Initial narrative and structural intake.",
        authority="HUMAN_SOVEREIGN"
    )

    print("\n[BOOTSTRAP SUCCESS] Master Workspace Compiled.")
    dashboard.render()

if __name__ == "__main__":
    main()