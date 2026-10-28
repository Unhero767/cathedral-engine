class_name OculusCamera
extends Camera2D

@export var target_node: Node2D
@export var smooth_speed: float = 6.0
@export var deadzone_radius: float = 6.0

func _ready() -> void:
	position_smoothing_enabled = false
	if not target_node:
		var players := get_tree().get_nodes_in_group(&"player")
		if players.size() > 0:
			target_node = players[0] as Node2D

func _physics_process(delta: float) -> void:
	if not is_instance_valid(target_node):
		return
	var target_pos := target_node.global_position
	var diff := target_pos - global_position
	if diff.length() > deadzone_radius:
		var target_destination := global_position + diff.normalized() * (diff.length() - deadzone_radius)
		global_position = global_position.lerp(target_destination, 1.0 - exp(-smooth_speed * delta))
