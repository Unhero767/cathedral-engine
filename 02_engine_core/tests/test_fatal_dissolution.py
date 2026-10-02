import pytest
from logic_engines.fatal_dissolution_guard import FatalDissolutionGuard

def test_stable_state_evaluation():
    guard = FatalDissolutionGuard()
    metrics = {
        "recoverable_information": 0.9,
        "identity_mass": 0.5,
        "pressure": 0.2,
        "fog": 0,
        "lineage_intact": True
    }
    result = guard.evaluate_dissolution_risk(metrics)
    assert result["status"] == "STABLE"
    assert not result["is_dissolved"]

def test_fatal_dissolution_loss_of_lineage():
    guard = FatalDissolutionGuard()
    metrics = {
        "recoverable_information": 0.9,
        "identity_mass": 0.5,
        "pressure": 0.2,
        "fog": 0,
        "lineage_intact": False
    }
    result = guard.evaluate_dissolution_risk(metrics)
    assert result["status"] == "FATAL_DISSOLUTION"
    assert result["is_dissolved"]
