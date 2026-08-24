#==============================================================================
# CathedralSync.gd - Godot 4.x Singleton Bridge
# Strata: Books I–XL (Prime Foundations, Inner Mandala, Outer Choirs, Inner Shadow Canon)
# Dual Mode: HTTP Polling (/api/rpg/state) & Direct SQLite Driver Binding
#==============================================================================
extends Node

signal state_updated(state: Dictionary)
signal chamber_loaded(chamber_data: Dictionary)
signal flux_updated(carrier_hz: float, dphi_dt: float)
signal card_drawn(result: Dictionary)
signal sqlite_bound(status: bool)

@export var backend_url: String = "http://127.0.0.1:5000"
@export var poll_interval: float = 0.5
@export var sqlite_db_path: String = "res://strata/ash_archive.db"
@export var enable_direct_sqlite: bool = true

var http_state_client: HTTPRequest
var http_chamber_client: HTTPRequest
var http_oracle_client: HTTPRequest
var poll_timer: Timer

# Live Telemetry Cache
var current_turn: int = 1
var tau_pol: float = 0.44
var rho_res: float = 0.38
var delta_fac: float = 0.35
var sigma_coh: float = 0.72
var carrier_hz: float = 130.81
var flux_dphi_dt: float = 0.428
var active_spectral: String = "RED"
var active_chamber_id: int = 5

# Direct SQLite Driver reference (godot-sqlite or C# GDExtension)
var db_instance: Variant = null

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	_setup_http_clients()
	_setup_poll_timer()
	if enable_direct_sqlite:
		_bind_direct_sqlite()
	# Initial fetch
	fetch_rpg_state()
	fetch_chamber(active_chamber_id)

func _setup_http_clients() -> void:
	http_state_client = HTTPRequest.new()
	add_child(http_state_client)
	http_state_client.request_completed.connect(_on_state_request_completed)

	http_chamber_client = HTTPRequest.new()
	add_child(http_chamber_client)
	http_chamber_client.request_completed.connect(_on_chamber_request_completed)

	http_oracle_client = HTTPRequest.new()
	add_child(http_oracle_client)
	http_oracle_client.request_completed.connect(_on_oracle_request_completed)

func _setup_poll_timer() -> void:
	poll_timer = Timer.new()
	poll_timer.wait_time = poll_interval
	poll_timer.autostart = true
	poll_timer.one_shot = false
	add_child(poll_timer)
	poll_timer.timeout.connect(fetch_rpg_state)

func _bind_direct_sqlite() -> void:
	# Binds directly to SQLite strata if SQLite GDExtension is present
	if ClassDB.class_exists("SQLite"):
		db_instance = ClassDB.instantiate("SQLite")
		db_instance.path = sqlite_db_path
		if db_instance.open_db():
			print("[CathedralSync] Direct SQLite strata binding established at: ", sqlite_db_path)
			emit_signal("sqlite_bound", true)
		else:
			print("[CathedralSync] SQLite open failed. Falling back to HTTP backend.")
			emit_signal("sqlite_bound", false)
	else:
		print("[CathedralSync] SQLite GDExtension not loaded in engine binary. Running in HTTP REST mode.")
		emit_signal("sqlite_bound", false)

# -----------------------------------------------------------------------------
# Public API Commands
# -----------------------------------------------------------------------------
func fetch_rpg_state() -> void:
	if http_state_client.get_http_client_status() == HTTPClient.STATUS_DISCONNECTED:
		http_state_client.request(backend_url + "/api/rpg/state")

func fetch_chamber(chamber_id: int) -> void:
	active_chamber_id = chamber_id
	if http_chamber_client.get_http_client_status() == HTTPClient.STATUS_DISCONNECTED:
		http_chamber_client.request(backend_url + "/api/rpg/chamber?id=" + str(chamber_id))

func draw_oracle_card(spectrum_mode: String = "Gold-Obsidian", player_assertion: String = "T", card_id: int = -1) -> void:
	var payload = {
		"spectrum_mode": spectrum_mode,
		"player_assertion": player_assertion,
		"active_spectrum": active_spectral
	}
	if card_id > 0:
		payload["card_id"] = card_id
	var json_str = JSON.stringify(payload)
	var headers = ["Content-Type: application/json"]
	http_oracle_client.request(backend_url + "/api/oracle/draw", headers, HTTPClient.METHOD_POST, json_str)

# -----------------------------------------------------------------------------
# HTTP Response Callbacks
# -----------------------------------------------------------------------------
func _on_state_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code != 200:
		return
	var json = JSON.new()
	if json.parse(body.get_string_from_utf8()) == OK:
		var data = json.data
		current_turn = data.get("turn", current_turn)
		tau_pol = data.get("tau_pol", tau_pol)
		rho_res = data.get("rho_res", rho_res)
		delta_fac = data.get("delta_fac", delta_fac)
		sigma_coh = data.get("sigma_coh", sigma_coh)
		carrier_hz = data.get("carrier_hz", carrier_hz)
		flux_dphi_dt = data.get("flux_dphi_dt", flux_dphi_dt)
		active_spectral = data.get("active_spectral", active_spectral)

		emit_signal("state_updated", data)
		emit_signal("flux_updated", carrier_hz, flux_dphi_dt)

func _on_chamber_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code != 200:
		return
	var json = JSON.new()
	if json.parse(body.get_string_from_utf8()) == OK:
		emit_signal("chamber_loaded", json.data)

func _on_oracle_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code != 200:
		return
	var json = JSON.new()
	if json.parse(body.get_string_from_utf8()) == OK:
		emit_signal("card_drawn", json.data)
		# Immediately refresh state
		fetch_rpg_state()
