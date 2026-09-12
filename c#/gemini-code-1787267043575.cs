using System;

public enum EpistemicState : byte
{
    Neither = 0b00, // Neither true nor false (N)
    True    = 0b01, // True only (T)
    False   = 0b10, // False only (F)
    Both    = 0b11  // Both true and false - Dialetheic (B)
}

public readonly struct ParaconsistentBuffer
{
    private readonly byte packedStates;

    public ParaconsistentBuffer(EpistemicState stateA, EpistemicState stateB)
    {
        packedStates = (byte)(((byte)stateA << 4) | (byte)stateB);
    }

    public EpistemicState StateA => (EpistemicState)(packedStates >> 4);
    public EpistemicState StateB => (EpistemicState)(packedStates & 0x0F);

    /// <summary>
    /// Computes the Belnap-Dunn First-Degree Entailment (FDE) Conjunction (Meet).
    /// </summary>
    public static EpistemicState Meet(EpistemicState a, EpistemicState b)
    {
        // Truth bit is bit 0, False bit is bit 1
        int t = ((int)a & 1) & ((int)b & 1);
        int f = ((int)a >> 1) | ((int)b >> 1);
        return (EpistemicState)((f << 1) | t);
    }

    /// <summary>
    /// Computes the Belnap-Dunn First-Degree Entailment (FDE) Disjunction (Join).
    /// </summary>
    public static EpistemicState Join(EpistemicState a, EpistemicState b)
    {
        int t = ((int)a & 1) | ((int)b & 1);
        int f = ((int)a >> 1) & ((int)b >> 1);
        return (EpistemicState)((f << 1) | t);
    }

    /// <summary>
    /// Evaluates structural load or harmonic scar formation based on contradiction density.
    /// </summary>
    public bool ContainsHarmonicScar()
    {
        return StateA == EpistemicState.Both || StateB == EpistemicState.Both;
    }
}