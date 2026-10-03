# File: scripts/cathedral_presentation_client.gd
# Binds verified projection frames to HeartOculus ShaderMaterial uniforms and Spectral Constants.
extends Node
class_name CathedralPresentationClient

@export var websocket_url: String = "ws://127.0.0.1:8765/ws/manifold"
@export var target_mesh: MeshInstance3D = null

var _socket: WebSocketPeer = WebSocketPeer.new()
var is_connected: bool = false

signal projection_updated(atom_key: String, state_data: Dictionary)
signal connection_established()

const SPECTRAL_CONSTANTS: Dictionary = {
	"GOLD": Color(0.95, 0.82, 0.35, 1.0),     # Joy / Revelatory Synthesis
	"BLUE": Color(0.20, 0.45, 0.90, 1.0),     # Sorrow / Historical Excavation
	"TEAL": Color(0.15, 0.75, 0.70, 1.0),     # Curiosity / Exploratory Mechanics
	"RED": Color(0.85, 0.20, 0.20, 1.0),      # Anger / Fracture
	"VIOLET": Color(0.60, 0.25, 0.85, 1.0),   # Fear / Horizon Collapse
	"EMERALD": Color(0.20, 0.80, 0.40, 1.0),  # Love / Binding Mortar
	"BRONZE": Color(0.65, 0.45, 0.25, 1.0)    # Null / Grounding Stratum
}

func _ready() -> void:
	var err = _socket.connect_to_url(websocket_url)
	if err != OK:
		printerr("[Client] Failed to initiate connection: ", err)

func _process(_delta: float) -> void:
	_socket.poll()
	var state = _socket.get_ready_state()

	if state == WebSocketPeer.STATE_OPEN:
		if not is_connected:
			is_connected = true
			emit_signal("connection_established")

		while _socket.get_available_packet_count() > 0:
			var packet = _socket.get_packet()
			var payload_str = packet.get_string_from_utf8()
			_handle_projection_snapshot(payload_str)
	elif state == WebSocketPeer.STATE_CLOSED:
		is_connected = false

func _handle_projection_snapshot(payload_str: String) -> void:
	var parsed = JSON.parse_string(payload_str)
	if typeof(parsed) == TYPE_DICTIONARY:
		var atom_key: String = parsed.get("provenance", {}).get("context", "UNKNOWN")
		emit_signal("projection_updated", atom_key, parsed)
		_transduce_to_shader(parsed)

func _transduce_to_shader(data: Dictionary) -> void:
	if target_mesh == null:
		return

	var mat: ShaderMaterial = null
	if target_mesh.material_override is ShaderMaterial:
		mat = target_mesh.material_override as ShaderMaterial
	elif target_mesh.get_active_material(0) is ShaderMaterial:
		mat = target_mesh.get_active_material(0) as ShaderMaterial

	if mat == null:
		return

	var unc = data.get("uncertainty_metadata", {})
	var belnap = unc.get("belnap_state", "N")
	var is_scar = unc.get("is_harmonic_scar", false)
	var val = data.get("value", {})
	var atom_key: String = data.get("provenance", {}).get("context", "")

	# 1. Resolve Spectral Dominant
	var dominant_color: Color = SPECTRAL_CONSTANTS["GOLD"]
	if atom_key.begins_with("Spire"):
		dominant_color = SPECTRAL_CONSTANTS["GOLD"]
	elif atom_key.begins_with("Mortar"):
		dominant_color = SPECTRAL_CONSTANTS["EMERALD"]
	elif atom_key.begins_with("Shadow"):
		dominant_color = SPECTRAL_CONSTANTS["VIOLET"]

	mat.set_shader_parameter("u_albedo", dominant_color)
	mat.set_shader_parameter("u_emission_color", dominant_color)

	# 2. Transduce Belnap-Dunn Semantics to Fog & Kenomic Entropy
	if is_scar or belnap == "B":
		mat.set_shader_parameter("belnap_fog_level", 2)
		mat.set_shader_parameter("kenomic_entropy", 75.0)
		mat.set_shader_parameter("u_emission_multiplier", 8.5)
	elif belnap == "T":
		mat.set_shader_parameter("belnap_fog_level", 0)
		mat.set_shader_parameter("kenomic_entropy", 5.0)
		mat.set_shader_parameter("u_emission_multiplier", 2.0)
	elif belnap == "F":
		mat.set_shader_parameter("belnap_fog_level", 1)
		mat.set_shader_parameter("kenomic_entropy", 35.0)
		mat.set_shader_parameter("u_emission_multiplier", 1.0)
	else:
		mat.set_shader_parameter("belnap_fog_level", 0)
		mat.set_shader_parameter("kenomic_entropy", 0.0)
		mat.set_shader_parameter("u_emission_multiplier", 0.5)

	# 3. Transduce Scalar Strain to Glow Gain
	if typeof(val) == TYPE_DICTIONARY and val.has("strain"):
		mat.set_shader_parameter("u_strain_glow_gain", float(val["strain"]) * 2.5)
