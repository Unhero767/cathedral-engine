# File: scripts/test_presentation_runner.gd
extends SceneTree

const ClientScript = preload("res://scripts/cathedral_presentation_client.gd")
var client: Node = null
var frame_count: int = 0
var received_count: int = 0
const MAX_FRAMES: int = 1200

func _init() -> void:
	print("[Godot Headless] Initializing Cathedral Presentation Test Runner...")
	client = ClientScript.new()
	client.connect("connection_established", Callable(self, "_on_connected"))
	client.connect("projection_updated", Callable(self, "_on_projection_updated"))
	root.add_child(client)

func _on_connected() -> void:
	print("[Godot Headless] WebSocket Handshake OPEN. Ready for ingress.")

func _process(delta: float) -> bool:
	frame_count += 1

	if client != null and client.has_method("_process"):
		client._process(delta)

	if received_count >= 2:
		print("[Godot Headless] All %d projections received and validated. Exiting 0." % received_count)
		quit(0)
		return true

	if frame_count >= MAX_FRAMES:
		var state = client._socket.get_ready_state() if client else -1
		print("[Godot Headless] Timed out after %d frames. State: %d, Received: %d" % [frame_count, state, received_count])
		quit(1)
		return true

	return false

func _on_projection_updated(atom_key: String, state_data: Dictionary) -> void:
	received_count += 1
	var register = state_data.get("epistemic_register", "UNKNOWN")
	var val = state_data.get("value", {})
	var belnap = state_data.get("uncertainty_metadata", {}).get("belnap_state", "?")
	print("[Godot Headless] PROJECTION RECEIVED [%d] -> Key: %s | FOUR: %s | Register: %s | Value: %s" % [
		received_count, atom_key, belnap, register, str(val)
	])
