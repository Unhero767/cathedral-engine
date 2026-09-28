extends PanelContainer
class_name OracleHUDController

var http_request: HTTPRequest
var endpoint: String = "http://localhost:8000/api/v1/oracle/draw"
var hash_val: String = ""

func _ready() -> void:
	apply_cathedral_obsidian_style()
	
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_oracle_request_completed)
	print("[ORACLE HUD] Subsystem initialized with Obsidian-Gold resonance. Awaiting invocation.")

func apply_cathedral_obsidian_style() -> void:
	var style = StyleBoxFlat.new()
	style.bg_color = Color(0.05, 0.05, 0.07, 0.92)
	style.border_color = Color(0.85, 0.65, 0.20, 1.0)
	style.set_border_width_all(2)
	style.corner_radius_top_left = 4
	style.corner_radius_top_right = 4
	style.corner_radius_bottom_left = 4
	style.corner_radius_bottom_right = 4
	style.shadow_color = Color(0.85, 0.65, 0.20, 0.25)
	style.shadow_size = 8
	
	add_theme_stylebox_override("panel", style)

func request_card_draw() -> void:
	var error = http_request.request(endpoint)
	if error != OK:
		push_error("[ORACLE HUD] Failed to dispatch card draw request.")

func _on_oracle_request_completed(_result: int, response_code: int, _headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var json = JSON.new()
		if json.parse(body.get_string_from_utf8()) == OK:
			var data = json.get_data() as Dictionary
			var card = data.get("card_name", "Unknown")
			hash_val = data.get("merkle_hash", "")
			print("[ORACLE HUD] Card drawn: %s | AshArchive Hash: %s..." % [card, hash_val])
	else:
		push_warning("[ORACLE HUD] Response failed with code: %d" % response_code)
