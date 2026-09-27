@tool
class_name CathedralRuntimeBridge
extends Node

@export var websocket_url: String = "ws://127.0.0.1:8765/ws/manifold"
@export var target_node_path: NodePath = NodePath("HeartOculus")

var _socket: WebSocketPeer = WebSocketPeer.new()
var _heart_oculus: Node3D = null

func _ready() -> void:
    if Engine.is_editor_hint():
        return
    
    _heart_oculus = get_node_or_null(target_node_path) as Node3D
    if not _heart_oculus:
        print("[CathedralRuntimeBridge]: Warning - HeartOculus node not found at path: ", target_node_path)

    print("[CathedralRuntimeBridge]: Connecting to WebSocket telemetry manifold at: ", websocket_url)
    var err = _socket.connect_to_url(websocket_url)
    if err != OK:
        print("[CathedralRuntimeBridge]: Failed to connect. Error code: ", err)

func _process(_delta: float) -> void:
    _socket.poll()
    var state = _socket.get_ready_state()
    
    if state == WebSocketPeer.STATE_OPEN:
        while _socket.get_available_packet_count() > 0:
            var packet = _socket.get_packet()
            var json_str = packet.get_string_from_utf8()
            var json = JSON.new()
            var parse_err = json.parse(json_str)
            if parse_err == OK:
                var data = json.get_data()
                if typeof(data) == TYPE_DICTIONARY:
                    _apply_telemetry(data)
            else:
                print("[CathedralRuntimeBridge]: Failed to parse JSON packet: ", json_str)
                
    elif state == WebSocketPeer.STATE_CLOSING:
        pass
    elif state == WebSocketPeer.STATE_CLOSED:
        var code = _socket.get_close_code()
        var reason = _socket.get_close_reason()
        print("[CathedralRuntimeBridge]: WebSocket closed. Code: %d, Reason: %s. Reconnecting..." % [code, reason])
        _socket.connect_to_url(websocket_url)

func _apply_telemetry(data: Dictionary) -> void:
    var dphi_dt = data.get("dPhi_dt", 0.42)
    var belnap = data.get("belnap_state", "Both")

    # Drive HeartOculus spatial shader emission parameters
    if _heart_oculus and _heart_oculus.material_override:
        var mat = _heart_oculus.material_override as ShaderMaterial
        if mat:
            var emission_intensity = dphi_dt * 8.5
            mat.set_shader_parameter("u_strain_glow_gain", emission_intensity)

    if int(data.get("step", 0)) % 50 == 0:
        print("[CathedralRuntimeBridge]: Step %d | dPhi/dt: %.3f | Belnap State: %s" % [data.get("step"), dphi_dt, belnap])

func _exit_tree() -> void:
    if _socket:
        _socket.close()
