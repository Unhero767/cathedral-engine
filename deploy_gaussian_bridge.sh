#!/usr/bin/env bash
set -e

echo "[CATHE-BUILD] Constructing Cathedral-Engine Gaussian Splat & Strain Bridge..."

mkdir -p strata/models/models/godot/scripts
mkdir -p strata/models/models/csharp

# 1. Write Godot Runtime WebSocket Bridge (GDScript)
cat << 'EDOC' > strata/models/models/godot/scripts/CathedralRuntimeBridge.gd
extends Node

class_name CathedralRuntimeBridge

@export var websocket_url: String = "ws://localhost:8765/ws/manifold"
var socket := WebSocketPeer.new()
var current_strain_gain: float = 0.5

signal strain_gain_updated(gain: float)

func _ready() -> void:
    print("[CATHE-RT] Connecting to Telemetry Manifold at: ", websocket_url)
    var err := socket.connect_to_url(websocket_url)
    if err != ok:
        printerr("[CATHE-RT] WebSocket connection failed with error: ", err)

func _process(delta: float) -> void:
    socket.poll()
    var state := socket.get_ready_state()
    
    if state == WebSocketPeer.STATE_OPEN:
        while socket.get_available_packet_count() > 0:
            var packet := socket.get_packet()
            var data_string := packet.get_string_from_utf8()
            var json = JSON.new()
            var parse_err = json.parse(data_string)
            if parse_err == OK:
                var dict = json.get_data()
                if dict.has("metrics") and dict["metrics"].has("u_strain_glow_gain"):
                    current_strain_gain = float(dict["metrics"]["u_strain_glow_gain"])
                    emit_signal("strain_gain_updated", current_strain_gain)
                    _apply_shader_strain(current_strain_gain)
            
    elif state == WebSocketPeer.STATE_CLOSING:
        pass
    elif state == WebSocketPeer.STATE_CLOSED:
        var code := socket.get_close_code()
        var reason := socket.get_close_reason()
        print("[CATHE-RT] WebSocket closed: %d - %s. Reconnecting..." % [code, reason])
        socket.connect_to_url(websocket_url)

func _apply_shader_strain(gain: float) -> void:
    var target_mesh = get_node_or_null("../SplatMeshInstance3D")
    if target_mesh and target_mesh.material_override is ShaderMaterial:
        target_mesh.material_override.set_shader_parameter("u_strain_glow_gain", gain)
EDOC

# 2. Write C# Gaussian Splat Buffer Bridge
cat << 'EDOC' > strata/models/models/csharp/GaussianSplatBufferBridge.cs
using Godot;
using System;

public partial class GaussianSplatBufferBridge : Node
{
    [Export] public int TargetSplats { get; set; } = 18400;
    [Export] public int MonadStrataCount { get; set; } = 36;
    
    private float[] _splatStrainBuffer;
    private double _accumulatedEntropy;

    public override void _Ready()
    {
        _splatStrainBuffer = new float[TargetSplats];
        InitializeStrataBuffers();
        GD.Print($"[CATHE-CS] Initialized GaussianSplatBufferBridge with {_splatStrainBuffer.Length} splat registers across {MonadStrataCount} strata.");
    }

    private void InitializeStrataBuffers()
    {
        Random rand = new Random(0x35);
        for (int i = 0; i < TargetSplats; i++)
        {
            _splatStrainBuffer[i] = (float)(rand.NextDouble() * 0.8 + 0.2);
        }
    }

    public void UpdateStrainMatrix(float globalGain)
    {
        for (int i = 0; i < TargetSplats; i++)
        {
            _splatStrainBuffer[i] = Mathf.Clamp(_splatStrainBuffer[i] * (globalGain * 0.95f), 0.0f, 5.0f);
        }
        _accumulatedEntropy += globalGain * 0.02;
    }

    public float GetLandauerEntropy()
    {
        return (float)_accumulatedEntropy;
    }
}
EDOC

echo "[CATHE-BUILD] Gaussian Splat strain integration bridge successfully deployed to repository strata."
