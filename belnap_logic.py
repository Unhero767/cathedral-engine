#!/usr/bin/env python3
# ==============================================================================
# Cathedral-Engine Belnap-Dunn Four-Valued Logic Engine (Python)
# File: belnap_logic.py
# ==============================================================================

from enum import Enum

class BelnapValue(Enum):
    TRUE = "T"
    FALSE = "F"
    BOTH = "B"
    NEITHER = "N"

def belnap_negation(val: BelnapValue) -> BelnapValue:
    mapping = {
        BelnapValue.TRUE: BelnapValue.FALSE,
        BelnapValue.FALSE: BelnapValue.TRUE,
        BelnapValue.BOTH: BelnapValue.BOTH,
        BelnapValue.NEITHER: BelnapValue.NEITHER
    }
    return mapping[val]

def belnap_conjunction(a: BelnapValue, b: BelnapValue) -> BelnapValue:
    matrix = {
        (BelnapValue.TRUE, BelnapValue.TRUE): BelnapValue.TRUE,
        (BelnapValue.TRUE, BelnapValue.FALSE): BelnapValue.FALSE,
        (BelnapValue.TRUE, BelnapValue.BOTH): BelnapValue.BOTH,
        (BelnapValue.TRUE, BelnapValue.NEITHER): BelnapValue.NEITHER,
        
        (BelnapValue.FALSE, BelnapValue.TRUE): BelnapValue.FALSE,
        (BelnapValue.FALSE, BelnapValue.FALSE): BelnapValue.FALSE,
        (BelnapValue.FALSE, BelnapValue.BOTH): BelnapValue.FALSE,
        (BelnapValue.FALSE, BelnapValue.NEITHER): BelnapValue.FALSE,
        
        (BelnapValue.BOTH, BelnapValue.TRUE): BelnapValue.BOTH,
        (BelnapValue.BOTH, BelnapValue.FALSE): BelnapValue.FALSE,
        (BelnapValue.BOTH, BelnapValue.BOTH): BelnapValue.BOTH,
        (BelnapValue.BOTH, BelnapValue.NEITHER): BelnapValue.NEITHER,
        
        (BelnapValue.NEITHER, BelnapValue.TRUE): BelnapValue.NEITHER,
        (BelnapValue.NEITHER, BelnapValue.FALSE): BelnapValue.FALSE,
        (BelnapValue.NEITHER, BelnapValue.BOTH): BelnapValue.NEITHER,
        (BelnapValue.NEITHER, BelnapValue.NEITHER): BelnapValue.NEITHER,
    }
    return matrix[(a, b)]

def belnap_disjunction(a: BelnapValue, b: BelnapValue) -> BelnapValue:
    matrix = {
        (BelnapValue.TRUE, BelnapValue.TRUE): BelnapValue.TRUE,
        (BelnapValue.TRUE, BelnapValue.FALSE): BelnapValue.TRUE,
        (BelnapValue.TRUE, BelnapValue.BOTH): BelnapValue.TRUE,
        (BelnapValue.TRUE, BelnapValue.NEITHER): BelnapValue.TRUE,
        
        (BelnapValue.FALSE, BelnapValue.TRUE): BelnapValue.TRUE,
        (BelnapValue.FALSE, BelnapValue.FALSE): BelnapValue.FALSE,
        (BelnapValue.FALSE, BelnapValue.BOTH): BelnapValue.BOTH,
        (BelnapValue.FALSE, BelnapValue.NEITHER): BelnapValue.NEITHER,
        
        (BelnapValue.BOTH, BelnapValue.TRUE): BelnapValue.TRUE,
        (BelnapValue.BOTH, BelnapValue.FALSE): BelnapValue.BOTH,
        (BelnapValue.BOTH, BelnapValue.BOTH): BelnapValue.BOTH,
        (BelnapValue.BOTH, BelnapValue.NEITHER): BelnapValue.TRUE,
        
        (BelnapValue.NEITHER, BelnapValue.TRUE): BelnapValue.TRUE,
        (BelnapValue.NEITHER, BelnapValue.FALSE): BelnapValue.NEITHER,
        (BelnapValue.NEITHER, BelnapValue.BOTH): BelnapValue.TRUE,
        (BelnapValue.NEITHER, BelnapValue.NEITHER): BelnapValue.NEITHER,
    }
    return matrix[(a, b)]

if __name__ == "__main__":
    print("[BELNAP_PYTHON] Evaluating dialetheic conjunction of BOTH and FALSE:")
    result = belnap_conjunction(BelnapValue.BOTH, BelnapValue.FALSE)
    print(f"Result -> {result.value}")
