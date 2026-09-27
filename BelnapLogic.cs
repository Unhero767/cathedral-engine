// ==============================================================================
// Cathedral-Engine Belnap-Dunn Four-Valued Logic Struct (C#)
// File: BelnapLogic.cs
// ==============================================================================

using System;

namespace CathedralEngine.Core
{
    public enum BelnapState
    {
        True,
        False,
        Both,
        Neither
    }

    public readonly struct BelnapValue : IEquatable<BelnapValue>
    {
        public BelnapState State { get; }

        public BelnapValue(BelnapState state)
        {
            State = state;
        }

        public static BelnapValue Negate(BelnapValue val) => val.State switch
        {
            BelnapState.True => new BelnapValue(BelnapState.False),
            BelnapState.False => new BelnapValue(BelnapState.True),
            BelnapState.Both => new BelnapValue(BelnapState.Both),
            BelnapState.Neither => new BelnapValue(BelnapState.Neither),
            _ => val
        };

        public static BelnapValue Conjunction(BelnapValue a, BelnapValue b)
        {
            return (a.State, b.State) switch
            {
                (BelnapState.True, BelnapState.True) => new BelnapValue(BelnapState.True),
                (BelnapState.Both, B_STATE) when B_STATE != BelnapState.False => new BelnapValue(BelnapState.Both),
                (A_STATE, BelnapState.Both) when A_STATE != BelnapState.False => new BelnapValue(BelnapState.Both),
                (BelnapState.False, _) => new BelnapValue(BelnapState.False),
                (_, BelnapState.False) => new BelnapValue(BelnapState.False),
                _ => new BelnapValue(BelnapState.Neither)
            };
        }

        public bool Equals(BelnapValue other) => State == other.State;
        public override bool Equals(object obj) => obj is BelnapValue other && Equals(other);
        public override int GetHashCode() => (int)State;
        public override string ToString() => State.ToString();
    }
}
