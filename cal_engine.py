from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

from .belnap_dunn import BelnapDunnEvaluator


@dataclass
class InvariantValidationResult:
    is_valid: bool
    violations: List[str] = field(default_factory=list)
    enforced_stratum: str = "CANON_INVARIANT_GATE"
    sanitized_delta: Dict[str, Any] = field(default_factory=dict)


class CALEngine:
    ALLOWED_FOUR_VALS: Set[str] = BelnapDunnEvaluator.VALUES

    def __init__(self, strict_lex_i: bool = True) -> None:
        self.strict_lex_i = strict_lex_i

    def validate_transition(
        self,
        current_state: Dict[str, Any],
        proposed_delta: Dict[str, Any],
        harmonic_scars: Optional[List[Dict[str, Any]]] = None,
        cascade_event: Optional[Dict[str, Any]] = None,
    ) -> InvariantValidationResult:
        violations: List[str] = []

        if self.strict_lex_i:
            for key, val in proposed_delta.items():
                if val is None and key in current_state and current_state[key] is not None:
                    violations.append(f"LEX_I_VIOLATION: Destructive overwrite attempted on '{key}'.")

        logic_props = proposed_delta.get("logic_propositions", {})
        if isinstance(logic_props, dict):
            for p_k, p_v in logic_props.items():
                if isinstance(p_v, str) and p_v not in self.ALLOWED_FOUR_VALS:
                    violations.append(f"BELNAP_DUNN_VIOLATION: Proposition '{p_k}' invalid value '{p_v}'.")

        if "strain" in proposed_delta:
            strain = proposed_delta["strain"]
            if not isinstance(strain, (int, float)) or strain < 0.0 or strain > 5.0:
                violations.append(f"STRAIN_ACCUMULATOR_OUT_OF_BOUNDS: {strain} not in [0.0, 5.0].")

        if harmonic_scars:
            for idx, scar in enumerate(harmonic_scars):
                if not scar.get("scar_hash"):
                    violations.append(f"SCAR_INVARIANT_VIOLATION: Scar index {idx} lacks scar_hash.")
                if scar.get("structural_capacity", 0.0) <= 0.0:
                    violations.append(f"SCAR_INVARIANT_VIOLATION: Scar index {idx} capacity <= 0.")

        if cascade_event:
            if cascade_event.get("new_epoch", 0) <= cascade_event.get("previous_epoch", 0):
                violations.append("CASCADE_EPOCH_REGRESSION: Non-monotonic epoch advance.")
            if not cascade_event.get("phase_shift_digest"):
                violations.append("CASCADE_INVARIANT_VIOLATION: Missing digest.")

        is_valid = len(violations) == 0
        return InvariantValidationResult(
            is_valid=is_valid,
            violations=violations,
            sanitized_delta=dict(proposed_delta) if is_valid else {},
        )
