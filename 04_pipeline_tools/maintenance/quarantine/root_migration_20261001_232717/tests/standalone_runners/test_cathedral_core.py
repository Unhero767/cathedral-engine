import pytest
from cathedral_core.ontology.truth import TruthValue, ParaconsistentState
from cathedral_core.logic.evaluator import ParaconsistentEvaluator

def test_paraconsistent_merge_contradiction():
    state_1 = ParaconsistentState(entity_id="ENT-001", truth=TruthValue.TRUE, sources=["Node-A"])
    state_2 = ParaconsistentState(entity_id="ENT-001", truth=TruthValue.FALSE, sources=["Node-B"])

    merged = ParaconsistentEvaluator.merge(state_1, state_2)

    assert merged.truth == TruthValue.BOTH
    assert merged.harmonic_scar is not None
    assert "Node-A" in merged.sources
    assert "Node-B" in merged.sources

def test_paraconsistent_merge_idempotent():
    state_1 = ParaconsistentState(entity_id="ENT-002", truth=TruthValue.NEITHER, sources=["Node-C"])
    state_2 = ParaconsistentState(entity_id="ENT-002", truth=TruthValue.NEITHER, sources=["Node-D"])

    merged = ParaconsistentEvaluator.merge(state_1, state_2)

    assert merged.truth == TruthValue.NEITHER
    assert merged.harmonic_scar is None
