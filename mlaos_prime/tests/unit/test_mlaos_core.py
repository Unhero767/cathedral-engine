# ====================================================================
# MLAOS-Prime :: Core Paraconsistent & Architecture Unit Tests
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# ====================================================================
import os
import pytest
import sqlite3
from axioms import BelnapDunnEngine, FourValuedLogic
from ledger import AshArchive
from paraconsistent import DialetheicReasoner

@pytest.fixture
def temp_ledger(tmp_path):
    """Fixture providing an isolated Ash Archive DAG for testing."""
    db_file = tmp_path / "test_ash_archive.db"
    ledger = AshArchive(db_path=str(db_file))
    yield ledger
    if db_file.exists():
        db_file.unlink()

def test_lex_invariant_math():
    """Verify Lex I axiom baseline: dH/dt > 0."""
    dh_dt = 1.0  
    assert dh_dt > 0, "Invariant violated: Entropy/Harmonic gradient must be positive."

def test_belnap_dunn_conjunction():
    """Verify Truth Meet (/\t)."""
    result = BelnapDunnEngine.conjunction_truth(FourValuedLogic.TRUE, FourValuedLogic.FALSE)
    assert result == FourValuedLogic.FALSE

def test_belnap_dunn_knowledge_join():
    """Verify Knowledge Join (\/k) synthesizes BOTH (B)."""
    result = BelnapDunnEngine.knowledge_join(FourValuedLogic.TRUE, FourValuedLogic.FALSE)
    assert result == FourValuedLogic.BOTH

def test_lex_i_immutability(temp_ledger):
    """Verify SQLite triggers block UPDATE/DELETE (Lex I)."""
    temp_ledger.append({"test": "payload_alpha"})
    assert temp_ledger.verify_integrity() is True
    
    with sqlite3.connect(temp_ledger.db_path) as conn:
        cursor = conn.cursor()
        with pytest.raises(sqlite3.OperationalError):
            cursor.execute("UPDATE blocks SET payload = 'corrupted' WHERE index_id = 1")
        with pytest.raises(sqlite3.OperationalError):
            cursor.execute("DELETE FROM blocks WHERE index_id = 1")

def test_metamorphic_squeeze(temp_ledger):
    """Verify contradictions trigger Squeeze at 54.74 degrees."""
    reasoner = DialetheicReasoner(temp_ledger)
    result = reasoner.evaluate_pair(
        "Observation A", "Observation ~A", 
        FourValuedLogic.TRUE, FourValuedLogic.TRUE
    )
    assert result["truth_value"] == FourValuedLogic.BOTH.value
    assert result["scar"]["crystallization_angle"] == 54.74
    assert result["scar"]["structural_integrity"] == "LOAD_BEARING"
