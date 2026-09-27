using Godot;
using CathedralEngine.Core.Substrate;

namespace CathedralEngine.Core
{
    [GlobalClass]
    public partial class SubstrateBrushController : Node
    {
        [Export] public NodePath? EnginePath { get; set; }
        [Export] public NodePath? DisplayPath { get; set; }

        public SubstrateElement ActiveElement { get; private set; } = SubstrateElement.Sand;
        public int BrushRadius { get; private set; } = 3;

        private MlaosSubstrateEngine? _engine;
        private TextureRect? _display;

        public override void _Ready()
        {
            if (EnginePath != null)
                _engine = GetNodeOrNull<MlaosSubstrateEngine>(EnginePath);
            if (DisplayPath != null)
                _display = GetNodeOrNull<TextureRect>(DisplayPath);
        }

        public override void _Process(double delta)
        {
            if (_engine == null || _display == null) return;

            Vector2 mousePos = _display.GetLocalMousePosition();
            Vector2 displaySize = _display.Size;

            if (mousePos.X >= 0 && mousePos.X < displaySize.X && mousePos.Y >= 0 && mousePos.Y < displaySize.Y)
            {
                int gridX = (int)(mousePos.X / displaySize.X * _engine.GridWidth);
                int gridY = (int)(mousePos.Y / displaySize.Y * _engine.GridHeight);

                if (Input.IsMouseButtonPressed(MouseButton.Left))
                {
                    _engine.InscribeBrush(gridX, gridY, BrushRadius, ActiveElement);
                }
                else if (Input.IsMouseButtonPressed(MouseButton.Right))
                {
                    _engine.InscribeBrush(gridX, gridY, BrushRadius, SubstrateElement.Void);
                }
            }
        }

        public override void _UnhandledInput(InputEvent @event)
        {
            if (@event is InputEventMouseButton mouseBtn && mouseBtn.Pressed)
            {
                if (mouseBtn.ButtonIndex == MouseButton.WheelUp)
                    BrushRadius = Mathf.Clamp(BrushRadius + 1, 1, 16);
                else if (mouseBtn.ButtonIndex == MouseButton.WheelDown)
                    BrushRadius = Mathf.Clamp(BrushRadius - 1, 1, 16);
            }
            else if (@event is InputEventKey keyEvent && keyEvent.Pressed)
            {
                switch (keyEvent.Keycode)
                {
                    case Key.Key1: ActiveElement = SubstrateElement.Basalt; break;
                    case Key.Key2: ActiveElement = SubstrateElement.Sand; break;
                    case Key.Key3: ActiveElement = SubstrateElement.Fluid; break;
                    case Key.Key4: ActiveElement = SubstrateElement.Lava; break;
                    case Key.Key5: ActiveElement = SubstrateElement.Acid; break;
                    case Key.Key6: ActiveElement = SubstrateElement.HarmonicScar; break;
                    case Key.C: _engine?.ClearGrid(); break;
                }
            }
        }
    }
}
