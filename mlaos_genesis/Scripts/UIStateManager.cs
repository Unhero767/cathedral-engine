using Godot;

public partial class UIStateManager : Node
{
    [Signal]
    public delegate void StateTransitionedEventHandler(string newState);

    public override void _Ready()
    {
        Name = "UIStateManager";
        GD.Print("[UI STATE MANAGER]: Initialized and anchored to CathedralRoot.");
    }

    public void TransitionTo(string stateName)
    {
        GD.Print($"[UI STATE MANAGER]: Transitioning system state to -> {stateName}");
        EmitSignal(SignalName.StateTransitioned, stateName);
    }
}
