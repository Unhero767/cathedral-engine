extends ColorRect
class_name HeartOculusManifoldClient

@export var manifold_url: String = "ws://127.0.0.1:8765/ws/manifold"
var _ws: WebSocketPeer = WebSocketPeer.new()
var _shader_mat: ShaderMaterial

func _ready() -> void:
	_shader_mat = material as ShaderMaterial
	var err := _ws.connect_to_url(manifold_url)
	if err != OK:
		push_error("[HeartOculus] Failed to bind /ws/manifold: %s" % err)

func _process(_delta: float) -> void:
	_ws.poll()
	if _ws.get_ready_state() == WebSocketPeer.STATE_OPEN:
		while _ws.get_available_packet_count() > 0:
			var raw_str := _ws.get_packet().get_string_from_utf8()
			var msg: Variant = JSON.parse_string(raw_str)
			if typeof(msg) == TYPE_DICTIONARY and msg.get("event") == "STRATUM_TRANSITION":
				_apply_dossier_telemetry(msg["dossier"])

func _apply_dossier_telemetry(dossier: Dictionary) -> void:
	if _shader_mat == null:
		return
	var tv: Array = dossier.get("truth_vector", [0, 0])
	var d_phi_dt: float = float(dossier.get("d_phi_dt", 0.0))
	var scar_idx: float = 0.0
	if dossier.has("harmonic_scar"):
		scar_idx = float(dossier["harmonic_scar"].get("load_bearing_index", 0.942))
	
	_shader_mat.set_shader_parameter("u_truth_vector", Vector2(float(tv[0]), float(tv[1])))
	_shader_mat.set_shader_parameter("u_d_phi_dt", d_phi_dt)
	_shader_mat.set_shader_parameter("u_scar_load_index", scar_idx)
