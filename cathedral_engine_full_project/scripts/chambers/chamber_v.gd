extends Node

const BASE_URL = "http://127.0.0.1:5001"

@export var tension_threshold: float = 0.50

func _ready() -> void:
	print("[Chamber V] Initializing spatial resonance chamber...")
	poll_strata_state()

func poll_strata_state() -> void:
	var http = HTTPRequest.new()
	add_child(http)
	http.request_completed.connect(_on_strata_polled)
	http.request(BASE_URL + "/api/rpg/state")

func _on_strata_polled(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var json = JSON.parse_string(body.get_string_from_utf8())
		if json:
			var current_tension: float = json.get("tension", 0.0)
			var current_hz: float = json.get("carrier_hz", 0.0)
			print("[Chamber V] Strata Resonating -> Carrier Frequency: %.2Hz | Tension Vector: %.2f" % [current_hz, current_tension])
			
			if current_tension >= tension_threshold:
				trigger_harmonic_scar()

func trigger_harmonic_scar() -> void:
	print("[Chamber V] Harmonic Scar crystallized. Dialetheic buffer engaged.")
