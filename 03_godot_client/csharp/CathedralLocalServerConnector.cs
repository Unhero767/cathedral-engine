using Godot;
using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace MLAOS.Runtime
{
    /// <summary>
    /// Manages real-time connection status handshakes with local AI synthesis endpoints
    /// (Ollama, LM Studio, vLLM, and ComfyUI) to verify local server readiness.
    /// </summary>
    public partial class CathedralLocalServerConnector : Node
    {
        [Export] public string ServerBaseUrl = "http://127.0.0.1:8188";
        private readonly HttpClient _httpClient = new HttpClient();

        [Signal]
        public delegate void ServerConnectedEventHandler(string endpoint);

        [Signal]
        public delegate void ServerConnectionFailedEventHandler(string errorReason);

        public async Task<bool> VerifyLocalServerConnectionAsync()
        {
            GD.Print($"[ServerConnector]: Pinging local server handshake at {ServerBaseUrl}...");

            try
            {
                var response = await _httpClient.GetAsync(ServerBaseUrl);
                if (response.IsSuccessStatusCode)
                {
                    EmitSignal(SignalName.ServerConnected, ServerBaseUrl);
                    GD.Print($"[ServerConnector]: Handshake verified. Local server active at {ServerBaseUrl}.");
                    return true;
                }
                else
                {
                    string reason = $"HTTP Status: {response.StatusCode}";
                    EmitSignal(SignalName.ServerConnectionFailed, reason);
                    GD.PrintErr($"[ServerConnector]: Server responded with error: {reason}");
                    return false;
                }
            }
            catch (Exception ex)
            {
                string reason = ex.Message;
                EmitSignal(SignalName.ServerConnectionFailed, reason);
                GD.PrintErr($"[ServerConnector]: Connection refused. Ensure local server is running: {reason}");
                return false;
            }
        }
    }
}
// ==============================================================================
// END OF FILE: CathedralLocalServerConnector.cs
// ==============================================================================
