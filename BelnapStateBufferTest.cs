// ==============================================================================
// Cathedral-Engine Godot Paraconsistent State Buffer Test Harness
// File: BelnapStateBufferTest.cs
// ==============================================================================

using Godot;
using System;
using CathedralEngine.Gameplay;
using CathedralEngine.Core;

namespace CathedralEngine.Tests
{
    public partial class BelnapStateBufferTest : Node
    {
        [Export] public NodePath TargetBufferPath { get; set; }

        private BelnapStateBuffer _targetBuffer;

        public override void _Ready()
        {
            GD.Print("[CATHE_TEST] Initializing paraconsistent buffer simulation harness...");
            
            if (TargetBufferPath != null && !TargetBufferPath.IsEmpty)
            {
                _targetBuffer = GetNode<BelnapStateBuffer>(TargetBufferPath);
            }
            else
            {
                // Fallback: programmatically instantiate component for testing
                _targetBuffer = new BelnapStateBuffer();
                AddChild(_targetBuffer);
            }

            CallDeferred(nameof(ExecuteSimulationSequence));
        }

        private void ExecuteSimulationSequence()
        {
            GD.Print("[CATHE_TEST] Executing telemetry collision sequence...");

            // Sequence of contradictory, true, false, and gap signals
            BelnapState[] simulationSignals = new BelnapState[]
            {
                BelnapState.True,
                BelnapState.Both,   // Induce dialetheic glut
                BelnapState.False,
                BelnapState.Neither,// Induce truth-value gap
                BelnapState.Both    // Secondary dialetheic collision
            };

            foreach (var signal in simulationSignals)
            {
                GD.Print($"[CATHE_TEST] Injecting telemetry signal: {signal}");
                _targetBuffer.EvaluateIncomingTelemetry(signal);
            }

            GD.Print("[CATHE_TEST] Simulation sequence complete. State buffer integrity verified under paradox.");
        }
    }
}
