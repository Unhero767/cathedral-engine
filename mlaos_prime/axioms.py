"""
axioms.py - Belnap-Dunn Four-Valued Bilattice Engine
"""
from enum import Enum
from typing import Set, Dict, Tuple

class FourValuedLogic(Enum):
    NEITHER = "N"  # Epistemic Gap {}
    FALSE = "F"    # Pure Falsity {0}
    TRUE = "T"     # Pure Truth {1}
    BOTH = "B"     # Contradiction / Paradox {0, 1}

class BelnapDunnEngine:
    """Implements logical operations over FOUR bilattice."""
    
    _UNDERLYING: Dict[FourValuedLogic, Set[int]] = {
        FourValuedLogic.NEITHER: set(),
        FourValuedLogic.FALSE: {0},
        FourValuedLogic.TRUE: {1},
        FourValuedLogic.BOTH: {0, 1}
    }
    
    _REVERSE: Dict[Tuple[int, ...], FourValuedLogic] = {
        (): FourValuedLogic.NEITHER,
        (0,): FourValuedLogic.FALSE,
        (1,): FourValuedLogic.TRUE,
        (0, 1): FourValuedLogic.BOTH
    }

    @classmethod
    def negation(cls, val: FourValuedLogic) -> FourValuedLogic:
        """Truth negation (~t): Swaps 0 and 1, preserving B and N."""
        s = cls._UNDERLYING[val]
        negated = set()
        if 0 in s: negated.add(1)
        if 1 in s: negated.add(0)
        return cls._REVERSE[tuple(sorted(negated))]

    @classmethod
    def conjunction_truth(cls, a: FourValuedLogic, b: FourValuedLogic) -> FourValuedLogic:
        """Truth meet (/\t): Minimum in truth order."""
        table = {
            (FourValuedLogic.TRUE, FourValuedLogic.TRUE): FourValuedLogic.TRUE,
            (FourValuedLogic.TRUE, FourValuedLogic.BOTH): FourValuedLogic.BOTH,
            (FourValuedLogic.TRUE, FourValuedLogic.NEITHER): FourValuedLogic.NEITHER,
            (FourValuedLogic.TRUE, FourValuedLogic.FALSE): FourValuedLogic.FALSE,
            
            (FourValuedLogic.BOTH, FourValuedLogic.BOTH): FourValuedLogic.BOTH,
            (FourValuedLogic.BOTH, FourValuedLogic.NEITHER): FourValuedLogic.FALSE,
            (FourValuedLogic.BOTH, FourValuedLogic.FALSE): FourValuedLogic.FALSE,
            
            (FourValuedLogic.NEITHER, FourValuedLogic.NEITHER): FourValuedLogic.NEITHER,
            (FourValuedLogic.NEITHER, FourValuedLogic.FALSE): FourValuedLogic.FALSE,
            
            (FourValuedLogic.FALSE, FourValuedLogic.FALSE): FourValuedLogic.FALSE,
        }
        key = (a, b) if (a, b) in table else (b, a)
        return table[key]

    @classmethod
    def disjunction_truth(cls, a: FourValuedLogic, b: FourValuedLogic) -> FourValuedLogic:
        """Truth join (\\/t): Maximum in truth order."""
        return cls.negation(cls.conjunction_truth(cls.negation(a), cls.negation(b)))

    @classmethod
    def knowledge_join(cls, a: FourValuedLogic, b: FourValuedLogic) -> FourValuedLogic:
        """Knowledge join (\\/k): Set union of semantic content."""
        s_a = cls._UNDERLYING[a]
        s_b = cls._UNDERLYING[b]
        union = s_a.union(s_b)
        return cls._REVERSE[tuple(sorted(union))]

    @classmethod
    def is_designated(cls, val: FourValuedLogic) -> bool:
        """Designated values D = {T, B} preserve assertion status without explosion."""
        return val in {FourValuedLogic.TRUE, FourValuedLogic.BOTH}
