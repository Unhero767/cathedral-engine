using Godot;
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

namespace MLAOS.Runtime
{
    /// <summary>
    /// Bridges the Cathedral-Engine runtime to local ComfyUI / Flux image synthesis endpoints,
    /// translating text-to-image prompts into 32-bit HD-2D biomechanical textures and volumetric assets.
    /// </summary>
    public partial class CathedralImageSynthesisBridge : Node
    {
        [Export] public string ComfyApiEndpoint = "http://127.0.0.1:8188/prompt";
        private readonly HttpClient _httpClient = new HttpClient();

        [Signal]
        public delegate void TextureSynthesisCompletedEventHandler(string texturePath);

        public async void RequestTextToImageSynthesis(string visualPrompt)
        {
            GD.Print($"[ImageSynthesis]: Dispatching prompt to ComfyUI/Flux bridge: '{visualPrompt}'");

            // Construct architectural hard-noir style modifier payload
            string stylizedPrompt = $"{visualPrompt}, 32-bit HD-2D pixel art, dark noir biomechanical architecture, chiaroscuro lighting, volumetric shadows, Zdzislaw Beksiński style, H.R. Giger organic machinery, high contrast obsidian and teal palette";

            string jsonPayload = $@"{{
                ""prompt"": {{
                    ""3"": {{
                        ""inputs"": {{
                            ""text"": ""{stylizedPrompt}"",
                            ""clip"": [""4"", 1]
                        }},
                        ""class_type"": ""CLIPTextEncode""
                    }},
                    ""4"": {{
                        ""inputs"": {{
                            ""ckpt_name"": ""flux1-schnell.safetensors""
                        }},
                        ""class_type"": ""CheckpointLoaderSimple""
                    }}
                }}
            }}";

            try
            {
                var content = new StringContent(jsonPayload, Encoding.UTF8, "application/json");
                var response = await _httpClient.PostAsync(ComfyApiEndpoint, content);

                if (response.IsSuccessStatusCode)
                {
                    GD.Print("[ImageSynthesis]: Prompt successfully queued in local pipeline. Awaiting tensor return.");
                    EmitSignal(SignalName.TextureSynthesisCompleted, "res://assets/synthesized_texture.png");
                }
                else
                {
                    GD.PrintErr($"[ImageSynthesis]: ComfyUI endpoint returned error status: {response.StatusCode}");
                }
            }
            catch (Exception ex)
            {
                GD.PrintErr($"[ImageSynthesis]: Failed to connect to local image synthesis server: {ex.Message}");
            }
        }
    }
}
// ==============================================================================
// END OF FILE: CathedralImageSynthesisBridge.cs
// ==============================================================================
