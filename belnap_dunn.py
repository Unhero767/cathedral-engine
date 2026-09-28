from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Set, Tuple


class BelnapBit(Enum):
    N = 0b00  # Neither (Null / Unmapped)
    F = 0b01  # False
    T = 0b10  # True
    B = 0b11  # Both (Dialetheic Contradiction)


class BelnapValue(str, Enum):
    T = "T"
    F = "F"
    B = "B"
    N = "N"

    @classmethod
    def from_bit(cls, bit: int) -> BelnapValue:
        mapping = {
            BelnapBit.N.value: cls.N,
            BelnapBit.F.value: cls.F,
            BelnapBit.T.value: cls.T,
            BelnapBit.B.value: cls.B,
        }
        return mapping[bit]

    @property
    def bit(self) -> int:
        mapping = {
            self.N: BelnapBit.N.value,
            self.F: BelnapBit.F.value,
            self.T: BelnapBit.T.value,
            self.B: BelnapBit.B.value,
        }
        return mapping[self]


class BelnapDunnEvaluator:
    VALUES: Set[str] = {"T", "F", "B", "N"}

    CONJUNCTION_MATRIX: Dict[Tuple[str, str], str] = {
        ("T", "T"): "T", ("T", "F"): "F", ("T", "B"): "B", ("T", "N"): "N",
        ("F", "T"): "F", ("F", "F"): "F", ("F", "B"): "F", ("F", "N"): "F",
        ("B", "T"): "B", ("B", "F"): "F", ("B", "B"): "B", ("B", "N"): "N",
        ("N", "T"): "N", ("N", "F"): "F", ("N", "B"): "N", ("N", "N"): "N",
    }

    DISJUNCTION_MATRIX: Dict[Tuple[str, str], str] = {
        ("T", "T"): "T", ("T", "F"): "T", ("T", "B"): "T", ("T", "N"): "T",
        ("F", "T"): "T", ("F", "F"): "F", ("F", "B"): "B", ("F", "N"): "N",
        ("B", "T"): "T", ("B", "F"): "B", ("B", "B"): "B", ("B", "N"): "B",
        ("N", "T"): "T", ("N", "F"): "N", ("N", "B"): "B", ("N", "N"): "N",
    }

    NEGATION_MAP: Dict[str, str] = {
        "T": "F", "F": "T", "B": "B", "N": "N",
    }

    @classmethod
    def validate_value(cls, val: str) -> None:
        if val not in cls.VALUES:
            raise ValueError(f"INVALID_FOUR_VALUED_STATE: '{val}' is outside {{T, F, B, N}}.")

    @classmethod
    def evaluate_conjunction(cls, a: str, b: str) -> str:
        cls.validate_value(a)
        cls.validate_value(b)
        return cls.CONJUNCTION_MATRIX[(a, b)]

    @classmethod
    def evaluate_disjunction(cls, a: str, b: str) -> str:
        cls.validate_value(a)
        cls.validate_value(b)
        return cls.DISJUNCTION_MATRIX[(a, b)]

    @classmethod
    def evaluate_negation(cls, a: str) -> str:
        cls.validate_value(a)
        return cls.NEGATION_MAP[a]

    @classmethod
    def process_dialetheic_collision(cls, assertion: str, negation: str) -> Dict[str, Any]:
        cls.validate_value(assertion)
        cls.validate_value(negation)

        has_assertion = assertion in {"T", "B"}
        has_negation = negation in {"T", "B"}

        if has_assertion and has_negation:
            state = "B"
            strain_factor = 2.5
        elif has_assertion:
            state = "T"
            strain_factor = 0.5
        elif has_negation:
            state = "F"
            strain_factor = 0.5
        else:
            state = "N"
            strain_factor = 0.0

        return {
            "resolved_state": state,
            "tensor_strain": strain_factor,
            "is_dialetheic": state == "B",
        }
