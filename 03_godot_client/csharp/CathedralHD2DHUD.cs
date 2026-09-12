using Godot;

namespace MLAOS.Runtime
{
    /// <summary>
    /// Governs the 32-bit HD-2D Head-Up Display (HUD) for the Cathedral-Engine.
    /// Features a dark noir, biomechanical aesthetic with high-contrast obsidian panels,
    /// teal spectral gauges, and real-time cryptographic integrity readouts.
    /// </summary>
    public partial class CathedralHD2DHUD : Control
    {
        private Label _statusLabel;
        private Label _integrityLabel;
        private ProgressBar _structuralBar;

        public override void _Ready()
        {
            // Configure full-rect scaling for UI layer
            AnchorRight = 1.0f;
            AnchorBottom = 1.0f;

            // Build Obsidian/Teal UI Container
            var panelContainer = new PanelContainer();
            panelContainer.SetAnchorsAndOffsetsPreset(LayoutPreset.TopLeft);
            panelContainer.OffsetLeft = 20;
            panelContainer.OffsetTop = 20;
            panelContainer.OffsetRight = 340;
            panelContainer.OffsetBottom = 140;

            var vbox = new VBoxContainer();
            vbox.AddThemeConstantOverride("separation", 8);

            // Title Header
            _statusLabel = new Label();
            _statusLabel.Text = "CATHEDRAL-ENGINE // H_STATE: LOCKED";
            _statusLabel.AddThemeColorOverride("font_color", new Color(0.0f, 1.0f, 0.8f)); // Teal Accent

            // Integrity Readout
            _integrityLabel = new Label();
            _integrityLabel.Text = "STRUCTURAL INTEGRITY: 100.0%";
            _integrityLabel.AddThemeColorOverride("font_color", new Color(0.9f, 0.95f, 1.0f));

            // Structural Bar
            _structuralBar = new ProgressBar
            {
                MaxValue = 100.0f,
                Value = 100.0f,
                ShowPercentage = false
            };
            _structuralBar.CustomMinimumSize = new Vector2(0, 12);

            vbox.AddChild(_statusLabel);
            vbox.AddChild(_integrityLabel);
            vbox.AddChild(_structuralBar);
            panelContainer.AddChild(vbox);
            AddChild(panelContainer);

            GD.Print("[UI]: 32-bit HD-2D biomechanical HUD successfully initialized.");
        }

        public void UpdateStructuralIntegrity(float current, float max)
        {
            _structuralBar.MaxValue = max;
            _structuralBar.Value = current;
            _integrityLabel.Text = $"STRUCTURAL INTEGRITY: {current:F1}%";
        }
    }
}
// ==============================================================================
// END OF FILE: CathedralHD2DHUD.cs
// ==============================================================================
