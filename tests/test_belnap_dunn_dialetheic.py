import pytest

class FourValue:
    def __init__(self, pos, neg):
        self.pos = pos
        self.neg = neg
    def __neg__(self):
        return FourValue(self.neg, self.pos)
    def __and__(self, other):
        return FourValue(self.pos and other.pos, self.neg or other.neg)
    def __or__(self, other):
        return FourValue(self.pos or other.pos, self.neg and other.neg)
    def __eq__(self, other):
        return self.pos == other.pos and self.neg == other.neg
    def __repr__(self):
        if self.pos and not self.neg: return "T"
        if not self.pos and self.neg: return "F"
        if self.pos and self.neg: return "B"
        return "N"

T = FourValue(1, 0)
F = FourValue(0, 1)
B = FourValue(1, 1)
N = FourValue(0, 0)

def test_negation():
    assert -T == F
    assert -F == T
    assert -B == B
    assert -N == N

def test_conjunction():
    assert (T & B) == B
    assert (F & B) == F

def test_disjunction():
    assert (T | F) == T
    assert (B | N) == T
