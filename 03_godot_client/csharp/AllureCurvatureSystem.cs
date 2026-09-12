using Godot;

namespace MLAOS.Runtime
{
    /// <summary>
    /// Governs Cathedral-Engine Allure Mechanics (The Aesthetic Curvature Tensor).
    /// Treats allure not as superficial charm, but as Spacetime Geodesic Warping—
    /// bending local light, shadow density, and emotional gravity to create an irresistible
    /// optical-phenomenological gradient that pulls observer trajectories inward.
    /// </summary>
    public partial class AllureCurvatureSystem : Node3D
    {
        [Export] public float CurvatureTensorWeight = 1.618f; // Golden ratio baseline
        [Export] public float AllureFieldRadius = 6.0f;
        [Export] public string SpectralConstant = "Gold_Joy"; // Revelatory synthesis pull

        [Signal]
        public delegate void GeodesicCaptureEventHandler(string entityId, float tensorMagnitude);

        /// <summary>
        /// Warps local space-time trajectories based on the aesthetic allure gradient,
        /// bending incoming entity paths along the cathedral's optical manifold.
        /// </summary>
        public void ApplyAllureWarp(Node3D observerEntity, float delta)
        {
            if (observerEntity == null) return;

            float distance = GlobalPosition.DistanceTo(observerEntity.GlobalPosition);
            if (distance <= AllureFieldRadius)
            {
                // Calculate non-linear gravitational-optic curvature dropoff
                float warpFactor = Mathf.Pow(1.0f - (distance / AllureFieldRadius), 2.0f) * CurvatureTensorWeight * delta;
                Vector3 geodesicVector = (GlobalPosition - observerEntity.GlobalPosition).Normalized();

                // Bend observer movement along the aesthetic tensor
                observerEntity.GlobalPosition += geodesicVector * warpFactor;

                if (distance <= 1.0f)
                {
                    EmitSignal(SignalName.GeodesicCaptureEventHandler, observerEntity.Name.ToString(), CurvatureTensorWeight);
                    GD.Print($"[Allure]: Aesthetic Curvature Tensor locked on '{observerEntity.Name}'. Geodesic convergence achieved.");
                }
            }
        }
    }
}
// ==============================================================================
// END OF FILE: AllureCurvatureSystem.cs
// ==============================================================================
