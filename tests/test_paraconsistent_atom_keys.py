"""
Cathedral-Engine: Gate 2
Contradiction test harness evaluating truth states strictly via structural
atomKey tokens and Belnap-Dunn FOUR lattice points rather than literal log matching.
"""
import pytest
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Tuple

class BelnapValue(str, Enum):
    TRUE = "T"        # (1, 0)
    FALSE = "F"       # (0, 1)
    BOTH = "B"        # (1, 1) - Harmonic Scar
    NEITHER = "N"     # (0, 0)

@dataclass(frozen=True)
class SemanticAtomKey:
    domain: str
    locus: str
    property_name: str

    @property
    def token(self) -> str:
        return f"{self.domain}.{self.locus}.{self.property_name}"

def evaluate_belnap_state(t_support: bool, f_support: bool) -> BelnapValue:
    if t_support and f_support:
        return BelnapValue.BOTH
    elif t_support:
        return BelnapValue.TRUE
    elif f_support:
        return BelnapValue.FALSE
    return BelnapValue.NEITHER

class ContradictionHarness:
    def __init__(self):
        self.atom_registry: Dict[str, BelnapValue] = {}

    def ingest_observation(self, key: SemanticAtomKey, t_support: bool, f_support: bool) -> BelnapValue:
        current_state = evaluate_belnap_state(t_support, f_support)
        self.atom_registry[key.token] = current_state
        return current_state

def test_structural_atom_key_dialetheic_resolution():
    harness = ContradictionHarness()
    
    # Target Atom: Spire.Resonance.HarmonicCrystallization
    spire_resonance_key = SemanticAtomKey(
        domain="Spire", 
        locus="Resonance", 
        property_name="HarmonicCrystallization"
    )

    # Ingest simultaneous contradiction (Observer Alpha: True, Observer Beta: False)
    state = harness.ingest_observation(spire_resonance_key, t_support=True, f_support=True)

    # Strict structural assertions
    assert spire_resonance_key.token == "Spire.Resonance.HarmonicCrystallization"
    assert state == BelnapValue.BOTH, "Valuation must evaluate to lattice point BOTH (1, 1)"
    assert harness.atom_registry[spire_resonance_key.token] == BelnapValue.BOTH
    assert isinstance(state, BelnapValue)

def test_non_contradictory_atom_keys():
    harness = ContradictionHarness()
    
    key_true = SemanticAtomKey("Manifold", "Lumen", "Flux")
    key_false = SemanticAtomKey("Mortar", "Strain", "Fracture")
    key_neither = SemanticAtomKey("OuterChoir", "Signal", "Carrier")

    assert harness.ingest_observation(key_true, True, False) == BelnapValue.TRUE
    assert harness.ingest_observation(key_false, False, True) == BelnapValue.FALSE
    assert harness.ingest_observation(key_neither, False, False) == BelnapValue.NEITHER
