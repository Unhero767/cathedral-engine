using Godot;

namespace MLAOS.Runtime
{
    /// <summary>
    /// Governs sovereign player locomotion and kinematic movement within the 2.5D HD-2D
    /// Cathedral-Engine environment, adhering to the physical-architectural axis.
    /// </summary>
    public partial class CathedralEngineLocomotionSystem : CharacterBody3D
    {
        [Export] public float MoveSpeed = 5.0f;
        [Export] public float Gravity = 9.8f;

        private Vector3 _velocity;

        public override void _PhysicsProcess(double delta)
        {
            Vector3 velocity = _velocity;

            // Add gravity if not on floor
            if (!IsOnFloor())
            {
                velocity.y -= Gravity * (float)delta;
            }

            // Gather directional input
            Vector2 inputDir = Input.GetVector("ui_left", "ui_right", "ui_up", "ui_down");
            Vector3 direction = new Vector3(inputDir.x, 0, inputDir.y).Normalized();

            if (direction != Vector3.Zero)
            {
                velocity.x = direction.x * MoveSpeed;
                velocity.z = direction.z * MoveSpeed;
            }
            else
            {
                velocity.x = Mathf.MoveToward(_velocity.x, 0, MoveSpeed);
                velocity.z = Mathf.MoveToward(_velocity.z, 0, MoveSpeed);
            }

            _velocity = velocity;
            Velocity = velocity;
            MoveAndSlide();
        }
    }
}
// ==============================================================================
// END OF FILE: CathedralEngineLocomotionSystem.cs
// ==============================================================================
