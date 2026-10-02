import pytest
from logic_engines.dissipative_ledger_bridge import DissipativeLedgerBridge

def test_bridge_coupling_reversibility():
    bridge = DissipativeLedgerBridge()
    # Reversible operation should incur zero Landauer erasure dissipation
    res = bridge.evaluate_coupling("T", "reversible_transform")
    assert res["simulated_dissipation_cost"] == 0.0
    assert not res["is_irreversible"]

def test_bridge_coupling_contradiction_overhead():
    bridge = DissipativeLedgerBridge()
    # Irreversible operation under contradiction (B) incurs scaled thermodynamic cost
    res = bridge.evaluate_coupling("B", "irreversible_erasure")
    assert res["simulated_dissipation_cost"] > bridge.base_dissipation_cost
    assert res["is_irreversible"]

def test_invalid_epistemic_state():
    bridge = DissipativeLedgerBridge()
    with pytest.raises(ValueError):
        bridge.evaluate_coupling("INVALID", "irreversible_erasure")
