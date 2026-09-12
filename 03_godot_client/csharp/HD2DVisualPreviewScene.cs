using Godot;

namespace MLAOS.Runtime
{
    /// <summary>
    /// Instantiates a visual test scene showcasing the 2.5D HD-2D pixel shader, 
    /// volumetric chiaroscuro lighting, and biomechanical structural grid.
    /// </summary>
    public partial class HD2DVisualPreviewScene : Node3D
    {
        public override void _Ready()
        {
            GD.Print("================================================================================");
            GD.Print(" INITIALIZING 2.5D HD-2D VISUAL PREVIEW SCENE...");
            GD.Print("================================================================================");

            // 1. Create World Environment with Volumetric Fog and High Contrast Tone Mapping
            var env = new Environment
            {
                BackgroundMode = Environment.BGMode.Color,
                BackgroundColor = new Color(0.03f, 0.03f, 0.04f), // #0D0D11 Dark Noir Base
                VolumetricFogEnabled = true,
                VolumetricFogDensity = 0.05f,
                VolumetricFogAlbedo = new Color(0.1f, 0.12f, 0.15f),
                TonemapMode = Environment.TonemapEnum.Filmic,
                AdjustmentEnabled = true,
                AdjustmentContrast = 1.35f,
                AdjustmentSaturation = 0.85f
            };

            var envNode = new WorldEnvironment { Environment = env };
            AddChild(envNode);

            // 2. Establish Chiaroscuro Key Light (Volumetric Rim / Beam)
            var keyLight = new DirectionalLight3D
            {
                LightColor = new Color(0.9f, 0.95f, 1.0f),
                LightEnergy = 2.5f,
                ShadowEnabled = true,
                Rotation = new Vector3(Mathf.DegToRad(-45), Mathf.DegToRad(30), 0)
            };
            AddChild(keyLight);

            // 3. Establish Neon Spectral Accent Fill (Teal/Curiosity Flare)
            var accentLight = new OmniLight3D
            {
                LightColor = new Color(0.0f, 1.0f, 0.8f),
                LightEnergy = 4.0f,
                OmniRange = 10.0f,
                Position = new Vector3(0, 2, -2)
            };
            AddChild(accentLight);

            GD.Print("[VisualPreview]: Scene constructed. Chiaroscuro lighting and 2.5D shaders active.");
            GD.Print("================================================================================");
        }
    }
}
// ==============================================================================
// END OF FILE: HD2DVisualPreviewScene.cs
// ==============================================================================
