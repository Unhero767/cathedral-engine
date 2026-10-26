extends Node

class_name CathedralRuntimeBridge

@export var telemetry_url: String = "http://127.0.0.1:8765/stream/state"
@export var poll_interval: float = 1.0

var http_client: HTTPClient = HTTPClient.new()
var current_strain_glow: float = 1.0
var a_field_temp: float = 300.0

signal telemetry_updated(strain_glow: float, temp: float)

func _ready() -> void:
	set_process(true)

var _timer: float = 0.0
func _process(delta: float) -> void:
	_timer += delta
	if _timer >= poll_interval:
		_timer = 0.0
		_poll_telemetry()

func _poll_telemetry() -> void:
	var err = http_client.connect_to_host("127.0.0.1", 8765)
	if err != OK:
		return
	
	var request_err = http_client.request(HTTPClient.METHOD_GET, "/health", [])
	if request_err == OK:
		while http_client.get_status() == HTTPClient.STATUS_REQUESTING:
			http_client.poll()
			os_delay_msec(10)
		
		if http_client.get_status() == HTTPClient.STATUS_BODY:
			var rb = http_client.read_response_body_chunk()
			var json = JSON.parse_string(rb.get_string_from_utf8())
			if json and json.has("afield_temp"):
				a_field_temp = json["afield_temp"]
				current_strain_glow = 1.0 + (json.get("flux", 0.0) * 0.5)
				emit_signal("telemetry_updated", current_strain_glow, a_field_temp)
	http_client.close()

func os_delay_msec(msec: int) -> void:
	OS.delay_msec(msec)
