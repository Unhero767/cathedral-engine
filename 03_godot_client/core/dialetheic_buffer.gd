class_name DialetheicBuffer
extends Node

enum TruthValue {
	NEITHER = 0, # Empty / Unassigned / Null
	FALSE = 1,   # Pure False
	TRUE = 2,    # Pure True
	BOTH = 3     # Paraconsistent Contradiction (A and not-A)
}

var sync_request: HTTPRequest
var poll_interval: float = 1.0
var timer: float = 0.0

func _ready() -> void:
	sync_request = HTTPRequest.new()
	add_child(sync_request)
	sync_request.request_completed.connect(_on_telemetry_fetched)

func _process(delta: float) -> void:
	timer += delta
	if timer >= poll_interval:
		timer = 0.0
		# Request current state from the backend
		sync_request.request("http://localhost:8000/api/v1/telemetry/state")

func _on_telemetry_fetched(_result: int, response_code: int, _headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var json = JSON.new()
		if json.parse(body.get_string_from_utf8()) == OK:
			var data = json.get_data() as Dictionary
			var z_val = data.get("z_active", 1.0)
			var contradiction = data.get("active_contradiction", false)
			
			# Push live values directly into the global shader parameters
			RenderingServer.global_shader_parameter_set("global_z_active", z_val)
			RenderingServer.global_shader_parameter_set("global_contradiction_flag", 1.0 if contradiction else 0.0)
func evaluate_and(a: TruthValue, b: TruthValue) -> TruthValue:
	var table: Array = [
		[TruthValue.NEITHER, TruthValue.FALSE, TruthValue.NEITHER, TruthValue.FALSE],
		[TruthValue.FALSE,   TruthValue.FALSE, TruthValue.FALSE,   TruthValue.FALSE],
		[TruthValue.NEITHER, TruthValue.FALSE, TruthValue.TRUE,    TruthValue.BOTH],
		[TruthValue.FALSE,   TruthValue.FALSE, TruthValue.BOTH,    TruthValue.BOTH]
	]
	return table[a][b]

func evaluate_or(a: TruthValue, b: TruthValue) -> TruthValue:
	var table: Array = [
		[TruthValue.NEITHER, TruthValue.NEITHER, TruthValue.TRUE, TruthValue.TRUE],
		[TruthValue.NEITHER, TruthValue.FALSE,   TruthValue.TRUE, TruthValue.BOTH],
		[TruthValue.TRUE,    TruthValue.TRUE,    TruthValue.TRUE, TruthValue.TRUE],
		[TruthValue.TRUE,    TruthValue.BOTH,    TruthValue.TRUE, TruthValue.BOTH]
	]
	return table[a][b]

func process_proposition(node_id: String, state: TruthValue) -> void:
	if state == TruthValue.BOTH:
		AshArchive.append_log("DIALETHEIC_COLLISION", {"node": node_id, "state": "BOTH"})
