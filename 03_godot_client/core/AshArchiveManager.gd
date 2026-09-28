extends Node
class_name AshArchiveManager

var http_request: HTTPRequest
var archive_endpoint: String = "http://localhost:8000/api/v1/ash-archive/commit"

func _ready() -> void:
	http_request = HTTPRequest.new()
	add_child(http_request)
	http_request.request_completed.connect(_on_archive_completed)

func commit_state(merkle_hash: String, payload: Dictionary) -> void:
	var headers = ["Content-Type: application/json"]
	var query_params = "?merkle_hash=%s" % merkle_hash
	var body = JSON.stringify(payload)
	var error = http_request.request(archive_endpoint + query_params, headers, HTTPClient.METHOD_POST, body)
	if error != OK:
		push_warning("[AshArchiveManager] Failed to dispatch archive commit request.")

func _on_archive_completed(_result: int, response_code: int, _headers: PackedStringArray, body: PackedByteArray) -> void:
	if response_code == 200:
		var json = JSON.new()
		if json.parse(body.get_string_from_utf8()) == OK:
			print("[AshArchiveManager] State successfully anchored to Ash Archive DAG.")
