extends Node
class_name AshArchiveLedgerObserver

signal block_committed(index: int, block_hash: String, element_id: String, zone: String)
signal dialetheic_rejection_logged(record_id: String, violating_intent: String)
signal invariant_telemetry_updated(fiedler_mu2: float, friction_fs: float, carrier_hz: float)

@export var websocket_url: String = "ws://127.0.0.1:8000/v1/ledger/ws"
@export var base_reconnect_sec: float = 1.0
@export var max_reconnect_sec: float = 30.0
@export var max_packets_per_frame: int = 10

var _socket: WebSocketPeer = WebSocketPeer.new()
var _is_connected: bool = false
var _reconnect_timer: float = 0.0
var _reconnect_attempts: int = 0
var _current_wait_sec: float = 1.0

var element_nodes: Dictionary = {}

func _ready() -> void:
	_connect_to_server()

func _connect_to_server() -> void:
	var err: Error = _socket.connect_to_url(websocket_url)
	if err != OK:
		push_error("[AshArchiveLedgerObserver] Connection failed initiation: %d" % err)

func _process(delta: float) -> void:
	_socket.poll()
	var state: WebSocketPeer.State = _socket.get_ready_state()

	if state == WebSocketPeer.STATE_OPEN:
		if not _is_connected:
			_is_connected = true
			_reconnect_attempts = 0
			_current_wait_sec = base_reconnect_sec
			print("[AshArchiveLedgerObserver] Connected to Ash Archive.")

		var processed: int = 0
		while _socket.get_available_packet_count() > 0 and processed < max_packets_per_frame:
			var packet_bytes: PackedByteArray = _socket.get_packet()
			_handle_json_packet(packet_bytes.get_string_from_utf8())
			processed += 1

	elif state == WebSocketPeer.STATE_CLOSED:
		if _is_connected:
			_is_connected = false
			print("[AshArchiveLedgerObserver] WebSocket closed.")

		_reconnect_timer += delta
		if _reconnect_timer >= _current_wait_sec:
			_reconnect_timer = 0.0
			_reconnect_attempts += 1
			var exp_backoff = min(max_reconnect_sec, base_reconnect_sec * pow(2.0, _reconnect_attempts))
			_current_wait_sec = exp_backoff * randf_range(0.8, 1.2)
			_connect_to_server()

func _handle_json_packet(raw_json: String) -> void:
	var json: JSON = JSON.new()
	if json.parse(raw_json) != OK:
		return

	var packet: Dictionary = json.data
	match packet.get("event", ""):
		"BLOCK_COMMITTED":
			var d = packet.get("data", {})
			block_committed.emit(int(d.get("index", 0)), d.get("hash", ""), d.get("element_id", ""), d.get("zone", ""))
		"DIALETHEIC_REJECTION":
			var d = packet.get("data", {})
			dialetheic_rejection_logged.emit(d.get("record_id", ""), d.get("violating_intent", ""))
		"INVARIANT_TELEMETRY":
			var d = packet.get("data", {})
			var mu2 = float(d.get("fiedler_algebraic_connectivity_mu2", 0.3242))
			var fs = float(d.get("dialetheic_friction_fs", 0.3250))
			var hz = float(d.get("carrier_wave_hz", 42.0))
			invariant_telemetry_updated.emit(mu2, fs, hz)
			RenderingServer.global_shader_parameter_set("u_carrier_frequency_hz", hz)
			RenderingServer.global_shader_parameter_set("u_dialetheic_friction", fs)
			RenderingServer.global_shader_parameter_set("u_fiedler_floor_mu2", mu2)
