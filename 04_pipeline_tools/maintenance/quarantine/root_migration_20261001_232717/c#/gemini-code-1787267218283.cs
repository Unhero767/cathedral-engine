using System;

public enum EpistemicBilatticeState : byte
{
    NeitherTentative = 0b000,
    NeitherConfirmed = 0b001,
    TrueTentative    = 0b010,
    TrueConfirmed    = 0b011,
    FalseTentative   = 0b100,
    FalseConfirmed   = 0b101,
    BothTentative    = 0b110,
    BothConfirmed    = 0b111
}

public readonly struct BilatticeBuffer
{
    private readonly byte packedState;

    public BilatticeBuffer(EpistemicBilatticeState state)
    {
        packedState = (byte)state;
    }

    public EpistemicBilatticeState State => (EpistemicBilatticeState)(packedState & 0x07);

    /// <summary>
    /// Extracts the underlying Belnap-Dunn 4-valued base.
    /// Bit 2 represents Falsity, Bit 0 represents Truth.
    /// </summary>
    public byte GetBelnapBase()
    {
        return (byte)(packedState & 0b11);
    }

    /// <summary>
    /// Determines whether the state has achieved empirical confirmation.
    /// </summary>
    public bool IsConfirmed => (packedState & 0b001) != 0 && (packedState & 0b110) != 0;

    /// <summary>
    /// Evaluates if the state constitutes a hard dialetheic collision requiring scar stabilization.
    /// </summary>
    public bool RequiresHarmonicScar()
    {
        return State == EpistemicBilatticeState.BothConfirmed;
    }
}