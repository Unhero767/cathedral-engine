import unittest

class BelnapDunnState:
    PROVEN = "T"      # True only
    DISPROVEN = "F"   # False only
    BOTH = "B"        # Both True and False (Contradiction / Harmonic Scar)
    NEITHER = "N"     # Neither True nor False (Unresolved / Fog)

def evaluate_epistemic_state(claim_support: bool, claim_refutation: bool) -> str:
    if claim_support and not claim_refutation:
        return BelnapDunnState.PROVEN
    elif claim_refutation and not claim_support:
        return BelnapDunnState.DISPROVEN
    elif claim_support and claim_refutation:
        return BelnapDunnState.BOTH
    else:
        return BelnapDunnState.NEITHER

class TestBelnapDunnAdapter(unittest.TestCase):
    def test_truth_states(self):
        self.assertEqual(evaluate_epistemic_state(True, False), BelnapDunnState.PROVEN)
        self.assertEqual(evaluate_epistemic_state(False, True), BelnapDunnState.DISPROVEN)
        self.assertEqual(evaluate_epistemic_state(True, True), BelnapDunnState.BOTH)
        self.assertEqual(evaluate_epistemic_state(False, False), BelnapDunnState.NEITHER)
        print("SUCCESS: Belnap-Dunn four-valued state mapping validated (T, F, B, N).")

if __name__ == "__main__":
    unittest.main()
