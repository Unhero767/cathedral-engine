#!/usr/bin/env python3
"""
MLAOS Core Decoupled State Machine
==================================
Specification: The Architectural Pillars of MLAOS (M = (S, E, H, C, G))
Governing Laws: Lex I (Never-Overwrite), Lex IV (Belnap-Dunn FOUR = {T, F, B, N})
Sprint 01: Days 1–3 State Machine Decoupling
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Tuple

from storage_adapter import StorageAdapter, InMemoryAshArchive

PHI: float = 1.6180339887

class BelnapValue(str, Enum):
    T = "T"  # True
    F = "F"  # False
    B = "B"  # Both (Dialetheic Contradiction)
    N = "N"  # Neither (Uncertain / Fog)

@dataclass(frozen=True)
class HarmonicScar:
    scar_id: str
    shear_angle_deg: float
    absorbed_strain: float
    structural_capacity: float
    timestamp: float

@dataclass
class MachineStateTuple:
    """Formal unified machine tuple: M = (S, E, H, C, G)"""
    S: Dict[str, Any] = field(default_factory=dict)       # Operational State
    E: Dict[str, BelnapValue] = field(default_factory=dict) # Epistemic State
    H_digest: str = "0" * 64                               # Historical Tip Digest
    C: Dict[str, float] = field(default_factory=dict)     # Coupling State
    G_active: bool = True                                 # Continuity Guard Status
    strain_accumulator: float = 0.0                       # Volatile Dialetheic Strain
    scars: List[HarmonicScar] = field(default_factory=list)

class FatalDissolutionError(Exception):
    """Raised by the Continuity Guard when systemic invariants fail."""
    pass

class MLAOSCognitiveEngine:
    """Pure finite state machine with zero direct file-system bindings."""

    def __init__(self, storage: Optional[StorageAdapter] = None) -> None:
        self.storage: StorageAdapter = storage if storage is not None else InMemoryAshArchive()
        self.state: MachineStateTuple = MachineStateTuple(H_digest=self.storage.get_latest_hash())

    def process_dialetheic_input(self, claim_key: str, assert_true: bool, assert_false: bool) -> BelnapValue:
        """Resolve paraconsistent propositions into Belnap-Dunn FOUR."""
        if assert_true and assert_false:
            resolved = BelnapValue.B
            strain = 2.5
        elif assert_true:
            resolved = BelnapValue.T
            strain = 0.2
        elif assert_false:
            resolved = BelnapValue.F
            strain = 0.2
        else:
            resolved = BelnapValue.N
            strain = 0.5

        self.state.E[claim_key] = resolved
        self.state.strain_accumulator += strain

        # If strain crosses threshold, crystallize into an immutable Harmonic Scar
        if self.state.strain_accumulator >= 3.0:
            self._crystallize_scar(absorbed=self.state.strain_accumulator)
        return resolved

    def _crystallize_scar(self, absorbed: float) -> HarmonicScar:
        scar_id = f"scar_{len(self.state.scars) + 1:04d}_{int(time.time() * 1000)}"
        capacity = absorbed * PHI
        scar = HarmonicScar(
            scar_id=scar_id,
            shear_angle_deg=54.7356,  # Magic-Angle shear relief
            absorbed_strain=absorbed,
            structural_capacity=capacity,
            timestamp=time.time(),
        )
        self.state.scars.append(scar)
        self.state.strain_accumulator = 0.0
        return scar

    def transition(self, state_delta: Dict[str, Any]) -> MachineStateTuple:
        """Execute deterministic transition: M_{t+1} = delta(M_t, Delta S)"""
        # Continuity Guard evaluation
        if not self.state.G_active:
            raise FatalDissolutionError("Continuity Guard G is inactive; execution halted.")

        # Update operational state S
        new_S = dict(self.state.S)
        new_S.update(state_delta)
        self.state.S = new_S

        # Cumulative digest
        state_dump = json.dumps(self.state.S, sort_keys=True)
        cumulative_digest = hashlib.sha256(state_dump.encode("utf-8")).hexdigest()

        # Commit append-only transition to H via StorageAdapter
        block_payload = {
            "parent_hash": self.state.H_digest,
            "timestamp": time.time(),
            "state_delta": state_delta,
            "cumulative_digest": cumulative_digest,
        }
        new_tip_hash = self.storage.append_block(block_payload)
        self.state.H_digest = new_tip_hash

        # Update Coupling State C
        self.state.C["last_transition_ts"] = time.time()
        self.state.C["total_scars"] = float(len(self.state.scars))
        return self.state
