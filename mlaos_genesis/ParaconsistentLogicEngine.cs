using Godot;
using System;

public partial class ParaconsistentLogicEngine : Node
{
    [Flags]
    public enum OntologicalState 
    {
        None = 0,       // Null / Unmanifested
        Alive = 1,      // True / Executing in Dungeon
        Terminated = 2, // False / Inert Spatial Data
        Dialetheic = 3  // Both / The Harmonic Scar
    }

    public static OntologicalState EvaluateAsset(bool hasVitality, bool requiresRescueAllocation)
    {
        int stateValue = (int)OntologicalState.None;

        if (hasVitality) stateValue |= (int)OntologicalState.Alive;
        else stateValue |= (int)OntologicalState.Terminated;

        if (!hasVitality && requiresRescueAllocation) 
        {
            return OntologicalState.Dialetheic;
        }

        return (OntologicalState)stateValue;
    }
}
