using Godot;

public partial class HarmonicScarController : Node3D
{
    [Export] public MeshInstance3D TargetMesh;
    private ShaderMaterial _scarMaterial;
    private float _currentIntensity = 0.0f;
    private float _targetIntensity = 0.0f;

    public override void _Ready()
    {
        if (TargetMesh != null)
        {
            _scarMaterial = TargetMesh.GetSurfaceOverrideMaterial(0) as ShaderMaterial;
        }
    }

    public void OnHarmonicScarManifested(string entityId, float incurredCost, string ontologicalState)
    {
        if (ontologicalState == "B")
        {
            _targetIntensity = Mathf.Clamp(incurredCost / 5000.0f, 1.0f, 10.0f);
            GD.Print($"[VISUAL MANIFESTATION]: Harmonic Scar activated on entity {entityId} with intensity {_targetIntensity}");
        }
        else
        {
            _targetIntensity = 0.0f;
        }
    }

    public override void _Process(double delta)
    {
        if (_scarMaterial != null)
        {
            _currentIntensity = Mathf.Lerp(_currentIntensity, _targetIntensity, (float)delta * 5.0f);
            _scarMaterial.SetShaderParameter("scar_intensity", _currentIntensity);
        }
    }
}
