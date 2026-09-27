// ==============================================================================
// Cathedral-Engine Godot 4 C# Character Controller & DB Sync
// File: CathedralCharacterController.cs
// ==============================================================================

using Godot;
using System;
using CathedralEngine.Core;

namespace CathedralEngine.Gameplay
{
    public partial class CathedralCharacterController : CharacterBody3D
    {
        [Export] public string CharacterId { get; set; } = "CHAR-02";
        [Export] public float MoveSpeed { get; set; } = 5.0f;
        [Export] public float SyncIntervalSeconds { get; set; } = 2.0f;

        private float _syncTimer = 0.0f;
        private float _somaticStress = 1.2f;
        private Vector3 _lastSyncedPosition;

        public override void _Ready()
        {
            _lastSyncedPosition = GlobalPosition;
            GD.Print($"[CATHE_CTRL] Character controller active for [{CharacterId}].");
        }

        public override void _PhysicsProcess(double delta)
        {
            Vector3 velocity = Velocity;

            // Apply gravity if airborne
            if (!IsOnFloor())
            {
                velocity += GetGravity() * (float)delta;
            }

            // Capture movement inputs
            Vector2 inputDir = Input.GetVector("ui_left", "ui_right", "ui_up", "ui_down");
            Vector3 direction = new Vector3(inputDir.X, 0, inputDir.Y).Normalized();
            
            if (direction != Vector3.Zero)
            {
                velocity.X = direction.X * MoveSpeed;
                velocity.Z = direction.Z * MoveSpeed;
                
                // Accumulate slight somatic stress during active traversal
                _somaticStress += 0.001f * (float)delta;
            }
            else
            {
                velocity.X = Mathf.MoveToward(Velocity.X, 0, MoveSpeed);
                velocity.Z = Mathf.MoveToward(Velocity.Z, 0, MoveSpeed);
            }

            Velocity = velocity;
            MoveAndSlide();

            // Periodic database synchronization
            _syncTimer += (float)delta;
            if (_syncTimer >= SyncIntervalSeconds)
            {
                _syncTimer = 0.0f;
                SyncPositionToDatabase();
            }
        }

        private void SyncPositionToDatabase()
        {
            if (CathedralDatabaseBridge.Instance != null)
            {
                CathedralDatabaseBridge.Instance.UpdateCharacterPosition(CharacterId, GlobalPosition, _somaticStress);
                _lastSyncedPosition = GlobalPosition;
            }
            else
            {
                GD.PrintErr("[CATHE_CTRL_ERR] CathedralDatabaseBridge instance not found in scene tree.");
            }
        }
    }
}
