using Godot;
using System;

namespace MLAOS.Runtime
{
    /// <summary>
    /// Governs Cathedral-Engine Entrainment Mechanics (Phenomenological Seduction).
    /// Treats seduction not as mundane persuasion, but as Gravitational Attractor Well Capture—
    /// bending the emotional-metric tensor to pull sovereign frequencies across the event horizon
    /// into a shared architectural chamber.
    /// </summary>
    public partial class ResonanceEntrainmentSystem : Node3D
    {
        [Export] public float AttractorStrength = 2.5f;
        [Export] public float EventHorizonRadius = 4.0f;
        [Export] public string ActiveSpectralConstant = "Teal_Curiosity";

        [Signal]
        public delegate void EntrainmentCapturedEventHandler(string targetEntityId, float fieldIntensity);

        /// <summary>
        /// Applies gravitational-emotional entrainment on a target entity within the spatial field,
        /// drawing its coordinates into the sovereign attractor well.
        /// </summary>
        public void EvaluateEntrainment(Node3D targetEntity, float delta)
        {
            if (targetEntity == null) return;

            float distance = GlobalPosition.DistanceTo(targetEntity.GlobalPosition);
            if (distance <= EventHorizonRadius)
            {
                // Calculate entrainment pull vector proportional to inverse-square emotional gravity
                float pullFactor = (1.0f - (distance / EventHorizonRadius)) * AttractorStrength * delta;
                Vector3 pullDirection = (GlobalPosition - targetEntity.GlobalPosition).Normalized();
                
                targetEntity.GlobalPosition += pullDirection * pullFactor;

                // If crossed into the core threshold, trigger harmonic capture
                if (distance <= 0.5f)
                {
                    EmitSignal(SignalName.EntrainmentCapturedEventHandler, targetEntity.Name.ToString(), pullFactor);
                    GD.Print($"[Entrainment]: Sovereign attractor well successfully captured '{targetEntity.Name}'. Spectral constant '{ActiveSpectralConstant}' locked.");
                }
            }
        }
    }
}
// ==============================================================================
// END OF FILE: ResonanceEntrainmentSystem.cs
// ==============================================================================
