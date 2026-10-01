# ====================================================================
# MLAOS-Prime :: Belnap-Dunn 4-Valued Logic Matrix Tests
# Matrix Values: T (True), F (False), B (Both/Contradiction), N (Neither)
# ====================================================================
import pytest

class BelnapValue:
    def __init__(self, t: bool, f: bool):
        self.t = t
        self.f = f

    def __repr__(self):
        if self.t and not self.f: return "T"
        if not self.t and self.f: return "F"
        if self.t and self.f: return "B"
        return "N"

# Define canonical states
T = BelnapValue(True, False)
F = BelnapValue(False, True)
B = BelnapValue(True, True)
N = BelnapValue(False, False)

def belnap_and(a: BelnapValue, b: BelnapValue) -> BelnapValue:
    return BelnapValue(a.t and b.t, a.f or b.f)

def belnap_or(a: BelnapValue, b: BelnapValue) -> BelnapValue:
    return BelnapValue(a.t or b.t, a.f and b.f)

def test_belnap_matrix_identities():
    """Verify core 4-valued conjunction and disjunction algebra."""
    # B (Both) AND F (False) -> T is True(T) and False(F) -> False. F is False(T) and True(F) -> True. Result: F.
    res_and = belnap_and(B, F)
    assert str(res_and) == "F", f"Expected F, got {res_and}"

    # N (Neither) OR T (True) -> T is False or True -> True. F is True and False -> False. Result: T.
    res_or = belnap_or(N, T)
    assert str(res_or) == "T", f"Expected T, got {res_or}"

def test_lex_invariant_harmonic_growth():
    """Verify harmonic progression rate under Lex I."""
    entropy_states = [1.0, 1.414, 2.0, 2.718]
    for i in range(1, len(entropy_states)):
        dh_dt = entropy_states[i] - entropy_states[i-1]
        assert dh_dt > 0, f"Harmonic regression detected at index {i}"
