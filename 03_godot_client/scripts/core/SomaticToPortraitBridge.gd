class_name SomaticToPortraitBridge
extends Node

@export var portrait_path: NodePath
var portrait: Control

func _ready() -> void:
	if not portrait_path.is_empty():
		portrait = get_node_or_null(portrait_path) as Control
