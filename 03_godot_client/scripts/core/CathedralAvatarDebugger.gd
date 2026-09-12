class_name CathedralAvatarDebugger
extends Node

@export var target_harness_path: NodePath
var harness_node: Node

func _ready() -> void:
	if not target_harness_path.is_empty():
		harness_node = get_node_or_null(target_harness_path)
		print("[CathedralAvatarDebugger] Debugger harness synchronized.")
