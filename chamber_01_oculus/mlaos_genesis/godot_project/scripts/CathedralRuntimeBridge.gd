extends Node
class_name CathedralRuntimeBridge

@export var websocket_url: String = "ws://127.0.0.1:8765/ws/manifold"
var socket := WebSocketPeer.new()
var current_strain_gain: float = 0.5
var reconnect_timer: float = 0.0

signal strain_gain_updated(gain: float)

func _ready() -> void:
    _connect_socket()

func _connect_socket() -> void:
    print("[CATHE-RT] Connecting to Telemetry Manifold at: ", websocket_url)
    var err := socket.connect_to_url(websocket_url)
    if err != OK:
        printerr("[CATHE-RT] WebSocket connection failed with error: ", err)

func _process(delta: float) -> void:
    socket.poll()
    var state := socket.get_ready_state()

    if state == WebSocketPeer.STATE_OPEN:
        reconnect_timer = 0.0
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

    elif state == WebSocketPeer.STATE_CLOSED:
        reconnect_timer += delta
        if reconnect_timer >= 2.0: # Cooldown before reconnecting
            reconnect_timer = 0.0
            print("[CATHE-RT] Attempting WebSocket reconnection...")
            _connect_socket()

func _apply_shader_strain(gain: float) -> void:
    var target_mesh = get_node_or_null("../SplatMeshInstance3D")
    if target_mesh and target_mesh.material_override is StandardMaterial3D:
        target_mesh.material_override.emission_energy_multiplier = 2.5 * gain
