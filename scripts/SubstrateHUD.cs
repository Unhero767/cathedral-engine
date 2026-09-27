using Godot;
using CathedralEngine.Core.Substrate;

namespace CathedralEngine.Core
{
    [GlobalClass]
    public partial class SubstrateHUD : Label
    {
        [Export] public NodePath? BrushPath { get; set; }
        private SubstrateBrushController? _brush;

        public override void _Ready()
        {
            if (BrushPath != null)
                _brush = GetNodeOrNull<SubstrateBrushController>(BrushPath);
        }

        public override void _Process(double delta)
        {
            string element = _brush?.ActiveElement.ToString() ?? "None";
            int radius = _brush?.BrushRadius ?? 1;
            int fps = (int)Engine.GetFramesPerSecond();

            Text = $"MLAOS-PRIME // SUBSTRATE SANDBOX v1.0\n" +
                   $"TICK: 30.0 Hz Fixed | RENDER: {fps} FPS\n" +
                   $"ACTIVE BRUSH: [{element}] (Radius: {radius}px)\n" +
                   $"HOTKEYS: Basalt | Sand | Fluid | Lava | [5] Acid | [6] Scar | [C] Clear\n" +
                   $"CONTROLS: Left-Click Paint | Right-Click Erase | Scroll Wheel Brush Size";
        }
    }
}
