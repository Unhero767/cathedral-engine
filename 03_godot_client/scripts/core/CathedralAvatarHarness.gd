class_name CathedralAvatarHarness
extends Node

@export var avatar_portrait_path: NodePath
var portrait_node: Control

func _ready() -> void:
	if not avatar_portrait_path.is_empty():
		portrait_node = get_node_or_null(avatar_portrait_path) as Control
