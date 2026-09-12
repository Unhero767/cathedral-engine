using System;

namespace CathedralEngine.EAS03.Epistemic
{
    [Flags]
    public enum EpistemicBilatticeState : byte
    {
        NeitherTentative = 0b000, // 0 - Bottom / Unknown (No evidence, tentative)
        NeitherConfirmed = 0b001, // 1 - Void / Null (Evaluated, confirmed absence)
        TrueTentative    = 0b010, // 2 - Hypothesis (Positive evidence, unconfirmed)
        TrueConfirmed    = 0b011, // 3 - Proven Law (Positive evidence, verified)
        FalseTentative   = 0b100, // 4 - Suspected Fault (Negative evidence, unconfirmed)
        FalseConfirmed   = 0b101, // 5 - Refutation (Negative evidence, verified)
        BothTentative    = 0b110, // 6 - Paradox Collision (Contradiction detected, unstable)
        BothConfirmed    = 0b111  // 7 - Dialetheic Harmonic Scar (Permineralized contradiction)
    }

    public enum BelnapDunnType
    {
        Neither,
        True,
        False,
        Both_Dialetheic
    }
}