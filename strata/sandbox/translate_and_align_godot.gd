extends Node3D

class_name CathedralEngineBridge

@export var target_node_path: NodePath
@export var sync_frequency_hz: float = 1.5

var ws: WebSocketPeer = null
var current_url: String = "ws://localhost:8001/ws/telemetry"
var connected: bool = false
var chamber_meshes: Array[MeshInstance3D] = []

func _ready() -> void:
ws = WebSocketPeer.new()
_connect_to_server()
_setup_chambers()

func _connect_to_server() -> void:
var err = ws.connect_to_url(current_url)
if err != OK:
print("Cathedral Engine Bridge Error: Failed to connect to WebSocket telemetry server at ", current_url)
connected = false
else:
print("Cathedral Engine Bridge: Initializing WebSocket handshake with Sovereign Runtime...")
connected = true

func _setup_chambers() -> void:
var ring_configs = [
{ "count": 18, "radius": 16.0, "color": Color(0, 0.8, 0.8), "y": 0.0 },
{ "count": 12, "radius": 10.5, "color": Color(0.31, 0.78, 0.47), "y": -1.5 },
{ "count": 6,  "radius": 5.5,  "color": Color(1, 0.84, 0.0), "y": 1.5 }
]

for ring in ring_configs:
    for i in range(ring["count"]):
        var theta = (float(i) / float(ring["count"])) * TAU
        var x = cos(theta) * ring["radius"]
        var z = sin(theta) * ring["radius"]
        
        var mesh_instance = MeshInstance3D.new()
        var box = BoxMesh.new()
        box.size = Vector3(0.8, 0.8, 0.8)
        mesh_instance.mesh = box
        
        var mat = StandardMaterial3D.new()
        mat.albedo_color = ring["color"]
        mat.emission_enabled = true
        mat.emission = ring["color"]
        mat.emission_energy_multiplier = 0.5
        mesh_instance.material_override = mat
        
        mesh_instance.position = Vector3(x, ring["y"], z)
        add_child(mesh_instance)
        chamber_meshes.append(mesh_instance)
func _process(delta: float) -> void:
if ws == null:
return

ws.poll()
var state = ws.get_ready_state()

if state == WebSocketPeer.STATE_OPEN:
    while ws.get_available_packet_count() > 0:
        var pkt = ws.get_packet()
        var json_str = pkt.get_string_from_utf8()
        _parse_telemetry_frame(json_str)
        
elif state == WebSocketPeer.STATE_CLOSED:
    connected = false
    # Attempt reconnection retry
    ws.connect_to_url(current_url)
func _parse_telemetry_frame(json_string: String) -> void:
var json = JSON.new()
var error = json.parse(json_string)
if error == OK:
var data = json.get_data()
if data is Dictionary and data.has("treasury"):
var granite = data["treasury"]["total_granite"]
var obsidian = data["treasury"]["total_obsidian"]
# Apply somatic pulse wave alignment across chambers
var time_sec = Time.get_ticks_msec() * 0.001
for idx in range(chamber_meshes.size()):
var mesh = chamber_meshes[idx]
var pulse = sin(time_sec * sync_frequency_hz * TAU + (float(idx) * 0.2)) * 0.3 + 1.0
mesh.scale = Vector3(pulse, pulse, pulse)
