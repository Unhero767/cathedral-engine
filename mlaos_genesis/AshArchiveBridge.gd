extends Node
class_name AshArchiveBridge

signal stratum_appended(hash_string)
signal temporal_history_received(data_dict)

var http_post: HTTPRequest
var http_get: HTTPRequest

func _ready() -> void:
    http_post = HTTPRequest.new()
    http_get = HTTPRequest.new()
    add_child(http_post)
    add_child(http_get)
    http_post.request_completed.connect(self._on_post_completed)
    http_get.request_completed.connect(self._on_get_completed)

func transmit_transition(entity_id: String, payload: Dictionary) -> void:
    var body = JSON.stringify({"entity_id": entity_id, "state_payload": payload})
    var headers = ["Content-Type: application/json"]
    http_post.request("http://127.0.0.1:8000/archive/transition", headers, HTTPClient.METHOD_POST, body)

func request_temporal_grammar(entity_id: String) -> void:
    http_get.request("http://127.0.0.1:8000/archive/history/" + entity_id)

func _on_post_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
    if response_code == 200:
        var json_response = JSON.parse_string(body.get_string_from_utf8())
        stratum_appended.emit(json_response["hash"])

func _on_get_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
    if response_code == 200:
        var json_response = JSON.parse_string(body.get_string_from_utf8())
        temporal_history_received.emit(json_response)
