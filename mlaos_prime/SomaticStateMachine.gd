extends Node
# ====================================================================
# MLAOS-Prime :: Somatic State Machine (Godot 4)
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
# Role: Polls Backend Telemetry & Ledger at 1.500 Hz
# ====================================================================

const BASE_URL: String = "http://127.0.0.1:8000"
const POLL_INTERVAL_SEC: float = 0.666

var http_telemetry: HTTPRequest
var http_ledger: HTTPRequest
var poll_timer: Timer

var current_ego_density: float = 8.30
var current_spectral_coherence: float = 1.0

signal telemetry_updated(ego_density: float, coherence: float)
signal ledger_updated(scar_count: int)

func _ready() -> void:
	# Initialize Telemetry HTTP Node
	http_telemetry = HTTPRequest.new()
	add_child(http_telemetry)
	http_telemetry.request_completed.connect(_on_telemetry_received)
	
	# Initialize Ledger HTTP Node
	http_ledger = HTTPRequest.new()
	add_child(http_ledger)
	http_ledger.request_completed.connect(_on_ledger_received)
	
	# Initialize Polling Timer
	poll_timer = Timer.new()
	poll_timer.wait_time = POLL_INTERVAL_SEC
	poll_timer.autostart = true
	poll_timer.timeout.connect(_poll_backend)
	add_child(poll_timer)
	
	print("[SomaticStateMachine] Polling continuum at 1.500 Hz.")

func _poll_backend() -> void:
	if http_telemetry.get_http_client_status() == HTTPClient.STATUS_DISCONNECTED:
		http_telemetry.request(BASE_URL + "/telemetry")
	if http_ledger.get_http_client_status() == HTTPClient.STATUS_DISCONNECTED:
		http_ledger.request(BASE_URL + "/ledger")

func _on_telemetry_received(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var json = JSON.parse_string(body.get_string_from_utf8())
		if json and typeof(json) == TYPE_DICTIONARY:
			var datum = json.get("datum", {})
			var vector = json.get("nonary_vector", {})
			
			if vector.has("spectral_coherence"):
				current_spectral_coherence = vector.get("spectral_coherence", 1.0)
			if datum.has("ego_density"):
				current_ego_density = datum.get("ego_density", "8.30").to_float()
				
			telemetry_updated.emit(current_ego_density, current_spectral_coherence)
			_update_shader_parameters()

func _on_ledger_received(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var json = JSON.parse_string(body.get_string_from_utf8())
		if json and typeof(json) == TYPE_DICTIONARY:
			var scar_count = json.get("load_bearing_scars_inscribed", 0)
			ledger_updated.emit(scar_count)

func _update_shader_parameters() -> void:
	var parent = get_parent()
	if parent and parent is CanvasItem and parent.material and parent.material is ShaderMaterial:
		parent.material.set_shader_parameter("ego_density", current_ego_density)
		parent.material.set_shader_parameter("spectral_coherence", current_spectral_coherence)
