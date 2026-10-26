extends Node

@export var telemetry_url: String = "ws://127.0.0.1:8765/ws/manifold"
var websocket = WebSocketPeer.new()

func _ready() -> void:
    print("[Cathedral-Engine] Connecting runtime bridge to WebSocket telemetry manifold: ", telemetry_url)
    websocket.connect_to_url(telemetry_url)

func _process(delta: float) -> void:
    websocket.poll()
    var state = websocket.get_ready_state()
    if state == WebSocketPeer.STATE_OPEN:
        while websocket.get_available_packet_count() > 0:
            var packet = websocket.get_packet()
            var json_string = packet.get_string_from_utf8()
            var json = JSON.new()
            if json.parse(json_string) == OK:
                var data = json.get_data()
                if data is Dictionary:
                    apply_manifold_telemetry(data)
    elif state == WebSocketPeer.STATE_CLOSED:
        var code = websocket.get_close_code()
        var reason = websocket.get_close_reason()
        print("[Cathedral-Engine] WebSocket closed: %d - %s. Reconnecting..." % [code, reason])
        websocket.connect_to_url(telemetry_url)

func apply_manifold_telemetry(data: Dictionary) -> void:
    var strain = data.get("strain_threshold", 2.56)
    var spectral = data.get("spectral_constant", "EMERALD/LOVE")
    var mesh_node = get_node_or_null("../SplatMeshInstance3D")
    if mesh_node and mesh_node.material_override is ShaderMaterial:
        mesh_node.material_override.set_shader_parameter("u_strain_glow_gain", strain)
        print("[Cathedral-Engine] Applied telemetry -> Spectral: %s | Strain Gain: %.2f" % [spectral, strain])
