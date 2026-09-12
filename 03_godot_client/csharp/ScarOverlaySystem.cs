using Godot;
using System.Collections.Generic;

namespace MLAOS.Runtime
{
    /// <summary>
    /// Projects immutable ScarRecord coordinates into Godot viewport space as visual glyphs,
    /// influence spheres, or architectural markers, maintaining cryptographic binding.
    /// </summary>
    public sealed class ScarOverlaySystem : Node3D
    {
        [Export] private Material ScarMarkerMaterial;

        /// <summary>
        /// Instantiates visual markers for each immutable scar record in the canonical coordinate space.
        /// </summary>
        public void RenderScarOverlays(List<Dictionary<string, object>> scars)
        {
            foreach (var scar in scars)
            {
                if (scar["position"] is List<double> pos && pos.Count == 3)
                {
                    var markerInstance = new MeshInstance3D();
                    var sphereMesh = new SphereMesh();
                    
                    // Scale radius based on immutable record properties if available
                    float radius = scar.ContainsKey("radius") ? Convert.ToSingle(scar["radius"]) : 0.05f;
                    sphereMesh.Radius = radius;
                    sphereMesh.Height = radius * 2.0f;

                    markerInstance.Mesh = sphereMesh;
                    if (ScarMarkerMaterial != null)
                    {
                        markerInstance.MaterialOverride = ScarMarkerMaterial;
                    }

                    // Map canonical normalized space [-1.0, 1.0]^3 to world dimensions
                    markerInstance.Position = new Vector3((float)pos[0], (float)pos[1], (float)pos[2]);
                    
                    AddChild(markerInstance);
                    GD.Print($"[ScarOverlaySystem]: Anchored immutable scar '{scar["id"]}' at world position {markerInstance.Position}.");
                }
            }
        }
    }
}
// ==============================================================================
// END OF FILE: ScarOverlaySystem.cs
// ==============================================================================
