extends Node
class_name CampaignBridge

## Cathedral-Engine Godot 4 Native Campaign Bridge
## Connects Godot 4 scenes to the Cathedral master game loop and procedural chamber maps.

const API_BASE_URL: String = "http://127.0.0.1:5050"
var http_request: HTTPRequest
var current_chamber_index: int = 1
var active_game_state: Dictionary = {}

signal state_updated(state: Dictionary)
signal chamber_loaded(chamber_data: Dictionary)

func _ready() -> void:
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_request_completed)
	fetch_latest_state()

func fetch_latest_state() -> void:
	var url = API_BASE_URL + "/api/rpg/state"
	var err = http_request.request(url)
	if err != OK:
		push_warning("[CampaignBridge] Failed to connect to Cathedral Server on port 5050.")

func move_player(target_x: int, target_y: int) -> void:
	var url = API_BASE_URL + "/api/rpg/move?x=" + str(target_x) + "&y=" + str(target_y)
	http_request.request(url)

func player_attack(target_uid: String, action_name: String, spectrum: String = "Gold") -> void:
	var url = API_BASE_URL + "/api/rpg/attack?target_uid=" + target_uid + "&action=" + action_name.uri_encode() + "&spectrum=" + spectrum
	http_request.request(url)

func end_turn() -> void:
	var url = API_BASE_URL + "/api/rpg/end_turn"
	http_request.request(url)

func _on_request_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var json = JSON.new()
		var parse_result = json.parse(body.get_string_from_utf8())
		if parse_result == OK and typeof(json.data) == TYPE_DICTIONARY:
			active_game_state = json.data
			emit_signal("state_updated", active_game_state)
