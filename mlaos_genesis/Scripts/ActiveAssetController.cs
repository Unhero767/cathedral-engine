using Godot;

public partial class ActiveAssetController : CharacterBody3D
{
    [Export] public string EntityId = "Vesper_Null";
    [Export] public float BaseSpeed = 5.0f;
    [Export] public float MassMultiplier = 0.2f; // Low mass yields higher traversal agility
    
    private float _currentMass = 200.0f;
    private Vector3 _velocity;

    public override void _Ready()
    {
        GD.Print($"[GODOT RPG]: Initialized active asset entity -> {EntityId} with mass {_currentMass}");
    }

    public void ApplyTelemetryMass(float massBytes)
    {
        _currentMass = massBytes;
        GD.Print($"[MASS UPDATE]: Entity {EntityId} mass adjusted to {_currentMass} bytes.");
    }

    public override void _PhysicsProcess(double delta)
    {
        Vector3 direction = Vector3.Zero;

        // Input polling for 3D RPG navigation
        if (Input.IsActionPressed("ui_right")) direction.X += 1.0f;
        if (Input.IsActionPressed("ui_left")) direction.X -= 1.0f;
        if (Input.IsActionPressed("ui_down")) direction.Z += 1.0f;
        if (Input.IsActionPressed("ui_up")) direction.Z -= 1.0f;

        direction = direction.Normalized();

        // Velocity scaled inversely by chronological mass density (Landauer's Principle simulation)
        float effectiveSpeed = BaseSpeed / (1.0f + (_currentMass * 0.0001f * MassMultiplier));
        
        _velocity.X = direction.X * effectiveSpeed;
        _velocity.Z = direction.Z * effectiveSpeed;

        Velocity = _velocity;
        MoveAndSlide();
    }
}
