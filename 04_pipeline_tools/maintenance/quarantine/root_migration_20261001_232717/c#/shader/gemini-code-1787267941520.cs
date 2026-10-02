using System;
using Godot;

namespace CathedralEngine.EAS03.Epistemic
{
    [GlobalClass]
    public partial class EpistemicComponent : Node3D
    {
        [Signal]
        public delegate void StateChangedEventHandler(byte rawState, string stateName);

        [Signal]
        public delegate void HarmonicScarEngagedEventHandler(string scarHash, double consistency);

        [Export]
        public EpistemicBilatticeState CurrentState { get; set; } = EpistemicBilatticeState.NeitherTentative;

        [Export]
        public NodePath TargetMeshPath { get; set; }

        public double ConsistencyCoefficient { get; private set; } = 1.0;
        public double DivergenceVector { get; private set; } = 0.0;
        public BelnapDunnType LogicalClassification { get; private set; } = BelnapDunnType.Neither;
        public bool IsConfirmed { get; private set; } = false;

        private MeshInstance3D _targetMesh;
        private ShaderMaterial _shaderMaterial;

        public override void _Ready()
        {
            FindAndBindMesh();
            TransitionToState(CurrentState, true);
        }

        public void TransitionToState(EpistemicBilatticeState newState, bool forceUpdate = false)
        {
            if (CurrentState == newState && !forceUpdate)
                return;

            CurrentState = newState;
            byte raw = (byte)newState;

            // Bit 0: Confirmation (0 = Tentative, 1 = Confirmed)
            // Bit 1: Positivity / Truth
            // Bit 2: Negativity / Falsehood
            IsConfirmed = (raw & 0b001) != 0;
            bool hasTrue = (raw & 0b010) != 0;
            bool hasFalse = (raw & 0b100) != 0;

            if (hasTrue && hasFalse)
            {
                LogicalClassification = BelnapDunnType.Both_Dialetheic;
                ConsistencyCoefficient = IsConfirmed ? 0.98 : 0.45;
                DivergenceVector = IsConfirmed ? 0.088 : 0.850;
            }
            else if (hasTrue)
            {
                LogicalClassification = BelnapDunnType.True;
                ConsistencyCoefficient = IsConfirmed ? 1.00 : 0.80;
                DivergenceVector = IsConfirmed ? 0.000 : 0.200;
            }
            else if (hasFalse)
            {
                LogicalClassification = BelnapDunnType.False;
                ConsistencyCoefficient = IsConfirmed ? 1.00 : 0.75;
                DivergenceVector = IsConfirmed ? 0.050 : 0.400;
            }
            else
            {
                LogicalClassification = BelnapDunnType.Neither;
                ConsistencyCoefficient = IsConfirmed ? 1.00 : 0.90;
                DivergenceVector = 0.000;
            }

            UpdateVisuals();
            EmitSignal(SignalName.StateChanged, raw, newState.ToString());

            if (newState == EpistemicBilatticeState.BothConfirmed)
            {
                string scarHash = $"0xSCAR_{Guid.NewGuid().ToString("N")[..8].ToUpper()}";
                EmitSignal(SignalName.HarmonicScarEngaged, scarHash, ConsistencyCoefficient);
            }
        }

        private void FindAndBindMesh()
        {
            if (TargetMeshPath != null && !TargetMeshPath.IsEmpty)
            {
                _targetMesh = GetNodeOrNull<MeshInstance3D>(TargetMeshPath);
            }

            if (_targetMesh == null)
            {
                foreach (Node child in GetChildren())
                {
                    if (child is MeshInstance3D mesh)
                    {
                        _targetMesh = mesh;
                        break;
                    }
                }
            }

            if (_targetMesh != null)
            {
                Material activeMat = _targetMesh.GetActiveMaterial(0);
                if (activeMat is ShaderMaterial sm)
                {
                    _shaderMaterial = sm;
                }
            }
        }

        private void UpdateVisuals()
        {
            if (_shaderMaterial == null && _targetMesh != null)
            {
                Material activeMat = _targetMesh.GetActiveMaterial(0);
                if (activeMat is ShaderMaterial sm)
                    _shaderMaterial = sm;
            }

            if (_shaderMaterial == null)
                return;

            Color spectralColor = GetSpectralColorForState(CurrentState);
            float scarIntensity = (CurrentState == EpistemicBilatticeState.BothConfirmed) ? 1.0f : 0.0f;
            float entropyIntensity = (CurrentState == EpistemicBilatticeState.BothTentative) ? 0.85f : 0.0f;

            _shaderMaterial.SetShaderParameter("u_state_color", spectralColor);
            _shaderMaterial.SetShaderParameter("u_scar_intensity", scarIntensity);
            _shaderMaterial.SetShaderParameter("u_entropy_intensity", entropyIntensity);
            _shaderMaterial.SetShaderParameter("u_is_confirmed", IsConfirmed ? 1.0f : 0.0f);
        }

        public static Color GetSpectralColorForState(EpistemicBilatticeState state)
        {
            return state switch
            {
                EpistemicBilatticeState.NeitherTentative => new Color(0.18f, 0.20f, 0.24f, 1.0f),
                EpistemicBilatticeState.NeitherConfirmed => new Color(0.06f, 0.06f, 0.09f, 1.0f),
                EpistemicBilatticeState.TrueTentative    => new Color(0.15f, 0.65f, 0.75f, 1.0f),
                EpistemicBilatticeState.TrueConfirmed    => new Color(0.00f, 0.90f, 0.85f, 1.0f),
                EpistemicBilatticeState.FalseTentative   => new Color(0.70f, 0.30f, 0.15f, 1.0f),
                EpistemicBilatticeState.FalseConfirmed   => new Color(0.95f, 0.10f, 0.15f, 1.0f),
                EpistemicBilatticeState.BothTentative    => new Color(0.75f, 0.18f, 0.85f, 1.0f),
                EpistemicBilatticeState.BothConfirmed    => new Color(0.98f, 0.78f, 0.22f, 1.0f),
                _ => Colors.White
            };
        }
    }
}