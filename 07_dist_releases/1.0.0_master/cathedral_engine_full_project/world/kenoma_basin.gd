# KenomaBasin.gd
# Deep Abyss & Singularity Inversion Trigger
class_name KenomaBasin extends Node2D

signal singularity_inversion_initiated(shear_factor: float)
signal void_absorption(mass_absorbed: float)

@export var singularity_center: Vector2 = Vector2(640, 360)
@export var event_horizon_radius: float = 180.0

var inversion_active: bool = false
var shear_intensity: float = 0.0

func _physics_process(delta: float) -> void:
	if inversion_active:
		shear_intensity += delta * 0.2
		emit_signal("singularity_inversion_initiated", shear_intensity)
		
	queue_redraw()

func trigger_inversion() -> void:
	inversion_active = true
	if AshArchive:
		AshArchive.commit_entry({
			"event": "SINGULARITY_INVERSION_TRIGGERED",
			"radius": event_horizon_radius,
			"stratum": "Inner Shadow Canon"
		}, ["KENOMA", "EVENT_HORIZON"])

func _draw() -> void:
	# Draw Obsidian Abyss & Singularity Gate
	draw_circle(singularity_center, event_horizon_radius, Color(0.02, 0.02, 0.02, 1.0))
	draw_arc(singularity_center, event_horizon_radius, 0, TAU, 64, Color(0.541, 0.169, 0.886, 0.8), 2.0)
	draw_arc(singularity_center, event_horizon_radius * 0.5, 0, TAU, 32, Color(0.0, 0.898, 1.0, 0.5), 1.0)
