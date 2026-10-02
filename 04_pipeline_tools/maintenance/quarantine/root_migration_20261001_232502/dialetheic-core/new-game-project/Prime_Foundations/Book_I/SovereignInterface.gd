extends Node
# Autoload Name: SovereignInterface (or MrLaos)
# Core Root Singleton for Cathedral-Engine State & Signal Management

# --- GLOBAL EVENT BUS SIGNALS ---
signal dialetheic_fracture_detected(error_code: String, details: Dictionary)
signal dialogue_conflict_detected(node_id: String, state_a: Dictionary, state_b: Dictionary)
signal memory_spike_warning(current_mb: float, threshold_mb: float)
signal archive_write_request(data_payload: Dictionary)

# --- SENTINEL DAEMON SCRIPT PATHS ---
const PATH_ZEKE := "res://Prime_Foundations/Book_I/Sentinels/Zeke_Validator.gd"
const PATH_RUBY := "res://Prime_Foundations/Book_I/Sentinels/Ruby_Scout.gd"
const PATH_ZOE  := "res://Prime_Foundations/Book_I/Sentinels/Zoe_Mediator.gd"
const PATH_FREYA := "res://Prime_Foundations/Book_I/Sentinels/Freya_Protector.gd"

# --- SENTINEL NODE REFERENCES ---
var zeke: Node
var ruby: Node
var zoe: Node
var freya: Node

func _ready() -> void:
	name = "SovereignInterface"
	print("[MrLaos] Sovereign Interface Singleton initialized.")
	_instantiate_sentinels()

## Programmatically instantiates the 4 biological sentinel daemons
func _instantiate_sentinels() -> void:
	zeke = _create_sentinel_node("Zeke", PATH_ZEKE)
	ruby = _create_sentinel_node("Ruby", PATH_RUBY)
	zoe = _create_sentinel_node("Zoe", PATH_ZOE)
	freya = _create_sentinel_node("Freya", PATH_FREYA)
	
	print("[MrLaos] Sentinel Matrix fully active under global Autoload.")

## Helper function to safely instantiate and append daemon nodes
func _create_sentinel_node(sentinel_name: String, script_path: String) -> Node:
	var node := Node.new()
	node.name = sentinel_name
	
	if ResourceLoader.exists(script_path):
		var daemon_script: Script = load(script_path)
		node.set_script(daemon_script)
	else:
		push_warning("[MrLaos] Script not found for %s at: %s" % [sentinel_name, script_path])
		
	add_child(node)
	return node

# --- PUBLIC HELPER METHODS TO TRIGGER SIGNALS ---

func trigger_fracture(error_code: String, details: Dictionary = {}) -> void:
	dialetheic_fracture_detected.emit(error_code, details)

func trigger_dialogue_conflict(node_id: String, state_a: Dictionary, state_b: Dictionary) -> void:
	dialogue_conflict_detected.emit(node_id, state_a, state_b)

func trigger_memory_warning(current_mb: float, threshold_mb: float) -> void:
	memory_spike_warning.emit(current_mb, threshold_mb)

func request_archive_write(payload: Dictionary) -> void:
	archive_write_request.emit(payload)
