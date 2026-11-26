# TilemapAnamorphicRenderer.gd
# 1.5 Hz Somatic Emission & Anamorphic Light Projection
class_name TilemapAnamorphicRenderer extends Node2D

@export var light_radius: float = 320.0
@export var light_color: Color = Color(0.855, 0.647, 0.125, 0.3)

func _physics_process(_delta: float) -> void:
	queue_redraw()

func _draw() -> void:
	var pulse: float = 1.0
	if SomaticBaseline:
		pulse = SomaticBaseline.get_somatic_pulse_intensity()
		
	var dynamic_radius = light_radius * (0.85 + pulse * 0.3)
	var col = light_color
	col.a = col.a * (0.6 + pulse * 0.4)
	
	# Anamorphic Light Ellipse
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(1.6, 0.9))
	draw_circle(Vector2.ZERO, dynamic_radius, col)
	draw_set_transform(Vector2.ZERO, 0.0, Vector2(1.0, 1.0))
