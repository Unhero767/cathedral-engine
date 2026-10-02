using Godot;
using System;

[GlobalClass]
public partial class EpistemicComponent : Node3D
{
    [Export] public byte PackedBilatticeState { get; set; } = 0b000; // Default: NeitherTentative

    public EpistemicBilatticeState State 
    { 
        get => (EpistemicBilatticeState)(PackedBilatticeState & 0x07);
        set => PackedBilatticeState = (byte)value;
    }

    /// <summary>
    /// Computes a normalized weight [0.0 - 1.0] for transition physics and shader blending.
    /// Hard dialetheic collisions (BothConfirmed) maximize weight intensity.
    /// </summary>
    public float GetTransitionWeight()
    {
        return State switch
        {
            EpistemicBilatticeState.NeitherTentative => 0.0f,
            EpistemicBilatticeState.NeitherConfirmed => 0.1f,
            EpistemicBilatticeState.TentativeTrue    => 0.3f,
            EpistemicBilatticeState.ConfirmedTrue    => 0.5f,
            EpistemicBilatticeState.TentativeFalse   => 0.4f,
            EpistemicBilatticeState.ConfirmedFalse   => 0.6f,
            EpistemicBilatticeState.TentativeBoth    => 0.8f,
            EpistemicBilatticeState.ConfirmedBoth    => 1.0f, // Harmonic Scar anchor
            _ => 0.0f
        };
    }

    public override void _Process(double delta)
    {
        // Push current bilattice state and weight to material shader uniforms
        if (GetNode<MeshInstance3D>("MeshInstance3D")?.MaterialOverride is ShaderMaterial mat)
        {
            mat.SetShaderParameter("epistemic_state_id", (float)State);
            mat.SetShaderParameter("transition_weight", GetTransitionWeight());
        }
    }
}