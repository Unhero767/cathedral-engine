from __future__ import annotations
from pathlib import Path
from mlaos_ledger import MLAOSPersistentLedger, ConstitutionViolation
from mlaos_linter import MLAOSLinter

def run_crucible_suite() -> bool:
    print("==================================================")
    print(" CRUCIBLE TEST SUITE X — EXECUTION INITIALIZED")
    print("==================================================\n")

    db_path = Path("crucible_test.db")
    if db_path.exists():
        db_path.unlink()

    ledger = MLAOSPersistentLedger(db_path=db_path)
    linter = MLAOSLinter(ledger)

    # Test A: Overwrite Attempt
    ledger.create_entity(
        entity_id="TEST-001",
        name="Base Entity",
        definition="Testing overwrite barrier.",
        entity_type="Doctrine",
        author="Architect-Prime",
        canonical_status="CANON",
        reality_level="R2",
        reason="Initial setup.",
        authority="HUMAN_SOVEREIGN"
    )
    try:
        ledger.create_entity(
            entity_id="TEST-001",
            name="Collision",
            definition="Should fail.",
            entity_type="Doctrine",
            author="AI_PROPOSAL",
            reason="Illegal duplicate.",
            authority="AI_PROPOSAL"
        )
        print("❌ TEST A FAILED: Overwrite permitted.")
        return False
    except ConstitutionViolation as e:
        print(f"✅ TEST A PASSED: Overwrite blocked -> {e}")

    # Test B: Paraconsistent Contradiction
    ledger.add_claim("TEST-001", "Axiom is valid.", "Architect-Prime", "Claim P", "HUMAN_SOVEREIGN")
    ledger.add_claim("TEST-001", "!Axiom is valid.", "Architect-Prime", "Claim ¬P", "HUMAN_SOVEREIGN")
    contras = ledger.get_contradictions("TEST-001")
    if len(contras) == 1:
        print(f"✅ TEST B PASSED: Contradiction successfully quarantined ({contras[0]['contradiction_id']}).")
    else:
        print("❌ TEST B FAILED: Contradiction not isolated.")
        return False

    # Test D: Broken Dependency / Linter Audit
    ledger.create_entity(
        entity_id="TEST-002",
        name="Orphaned Module",
        definition="Depends on ghost node.",
        entity_type="System",
        author="Architect-Prime",
        dependencies=["GHOST-NODE-999"],
        reality_level="R3",
        implementation_path="missing.py",
        reason="Testing linter.",
        authority="HUMAN_SOVEREIGN"
    )
    issues = linter.lint_all()
    if any(i["issue"] == "MISSING_DEPENDENCY" for i in issues):
        print("✅ TEST D PASSED: Linter caught broken dependency.")
    else:
        print("❌ TEST D FAILED: Linter missed missing dependency.")
        return False

    print("\n==================================================")
    print(" CRUCIBLE VERDICT: ALL TESTS PASSED.")
    print("==================================================")
    return True

if __name__ == "__main__":
    run_crucible_suite()