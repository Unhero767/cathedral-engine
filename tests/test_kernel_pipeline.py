"""
Cathedral-Engine: Pipeline Test Suite
Tests:
1. Out-of-order event ingestion & causal sorting.
2. Dialetheic contradiction -> Belnap-Dunn BOTH (Harmonic Scar).
3. SQLite WAL trigger defense (Lex I).
4. Full Merkle DAG chain verification.
"""
import pytest
import sqlite3
import time
from core.kernel import (
    EventEnvelope,
    CausalSorter,
    FourAssertionLattice,
    MerkleAshArchive,
    BelnapValue,
    EpistemicRegisterTag,
)

def test_pipeline_out_of_order_and_contradiction():
    # 1. Prepare events arriving strictly OUT OF ORDER
    # Event 3 (Lamport 3) arrives FIRST
    e3 = EventEnvelope(
        event_id="EVT-003",
        atom_key="Spire.Resonance",
        lamport_clock=3,
        source_timestamp=100.3,
        actor="Observer-Beta",
        polarity=False,  # Negative evidence (f) -> False
        value={"strain": 0.95},
        parents=("EVT-002",)
    )

    # Event 1 (Lamport 1) arrives SECOND
    e1 = EventEnvelope(
        event_id="EVT-001",
        atom_key="Spire.Resonance",
        lamport_clock=1,
        source_timestamp=100.1,
        actor="Observer-Alpha",
        polarity=True,   # Positive evidence (t) -> True
        value={"strain": 0.40},
        parents=()
    )

    # Event 2 (Lamport 2) arrives THIRD
    e2 = EventEnvelope(
        event_id="EVT-002",
        atom_key="Mortar.Bond",
        lamport_clock=2,
        source_timestamp=100.2,
        actor="Observer-Gamma",
        polarity=True,
        value={"integrity": 0.99},
        parents=("EVT-001",)
    )

    raw_arrival_queue = [e3, e1, e2]

    # 2. Causal Sorting
    ordered_events = CausalSorter.sort(raw_arrival_queue)
    assert [e.event_id for e in ordered_events] == ["EVT-001", "EVT-002", "EVT-003"]

    # 3. Assertion Lattice & Merkle Ledger Execution
    lattice = FourAssertionLattice()
    archive = MerkleAshArchive()

    committed_hashes = []
    evaluated_states = []

    for evt in ordered_events:
        state = lattice.ingest(
            atom_key=evt.atom_key,
            actor=evt.actor,
            polarity=evt.polarity
        )
        evaluated_states.append(state)
        node_hash = archive.commit(evt, state)
        committed_hashes.append(node_hash)

    # 4. Verify Belnap Progression
    # EVT-001 (Spire.Resonance): Positive only -> T
    assert evaluated_states[0] == BelnapValue.TRUE

    # EVT-002 (Mortar.Bond): Positive only -> T
    assert evaluated_states[1] == BelnapValue.TRUE

    # EVT-003 (Spire.Resonance): Negative arrives from Beta while Alpha had Positive -> B (Harmonic Scar)
    assert evaluated_states[2] == BelnapValue.BOTH

    # 5. Verify Lex S Register Promotion
    cur = archive.conn.cursor()
    cur.execute("SELECT register FROM ash_archive WHERE atom_key = 'Spire.Resonance' ORDER BY node_id DESC LIMIT 1;")
    assert cur.fetchone()[0] == EpistemicRegisterTag.SCAR.value

    # 6. Verify Merkle Chain Integrity
    is_valid, msg = archive.verify_dag_integrity()
    assert is_valid, msg

    # 7. Verify Lex I Trigger Interlocks (UPDATE / DELETE)
    with pytest.raises(sqlite3.DatabaseError, match="Lex I Violation"):
        archive.conn.execute("UPDATE ash_archive SET belnap_state = 'T' WHERE atom_key = 'Spire.Resonance';")

    with pytest.raises(sqlite3.DatabaseError, match="Lex I Violation"):
        archive.conn.execute("DELETE FROM ash_archive WHERE node_id = 1;")
