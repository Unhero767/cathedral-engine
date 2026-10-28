using Godot;
using System;
using System.IO;
using System.Net.Sockets;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

public partial class SpatialSocketClient : Node
{
    private TcpClient _client;
    private StreamReader _reader;
    private bool _isRunning = false;

    [Signal]
    public delegate void TelemetryReceivedEventHandler(string entityId, string ontologicalState, float incurredCost);

    public override void _Ready()
    {
        _ = ConnectToEngineBridgeAsync();
    }

    private async Task ConnectToEngineBridgeAsync()
    {
        _client = new TcpClient();
        _isRunning = true;

        while (_isRunning && !_client.Connected)
        {
            try
            {
                await _client.ConnectAsync("127.0.0.1", 8001);
                GD.Print("[IPC CLIENT]: Connected successfully to Cathedral-Engine telemetry stream on port 8001.");
                
                var stream = _client.GetStream();
                _reader = new StreamReader(stream, Encoding.UTF8);
                
                _ = ListenForTelemetryStreamAsync();
            }
            catch (Exception)
            {
                GD.Print("[IPC CLIENT]: Attempting reconnection to Python IPC bridge...");
                await Task.Delay(3000);
            }
        }
    }

    private async Task ListenForTelemetryStreamAsync()
    {
        try
        {
            while (_isRunning && _client.Connected)
            {
                string line = await _reader.ReadLineAsync();
                if (line != null)
                {
                    ProcessIncomingPayload(line);
                }
            }
        }
        catch (Exception ex)
        {
            GD.PrintErr($"[IPC CLIENT ERROR]: Stream interrupted: {ex.Message}");
            _ = ConnectToEngineBridgeAsync();
        }
    }

    private void ProcessIncomingPayload(string jsonPayload)
    {
        try
        {
            var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
            var data = JsonSerializer.Deserialize<SpatialTelemetryModel>(jsonPayload, options);

            if (data != null && !string.IsNullOrEmpty(data.BelnapState))
            {
                GD.Print($"[SPATIAL TELEMETRY]: Entity {data.EntityId} -> State {data.BelnapState} (Cost: {data.IncurredCost})");
                EmitSignal(SignalName.TelemetryReceived, data.EntityId, data.BelnapState, data.IncurredCost);
            }
        }
        catch (Exception ex)
        {
            GD.PrintErr($"[JSON PARSE ERROR]: Failed to decode telemetry: {ex.Message}");
        }
    }

    public override void _ExitTree()
    {
        _isRunning = false;
        _reader?.Dispose();
        _client?.Close();
    }
}

public class SpatialTelemetryModel
{
    public string EntityId { get; set; }
    public string BelnapState { get; set; }
    public float IncurredCost { get; set; }
}
