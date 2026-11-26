# ResonantDeliberation.gd
# Harmonic Senate Dissonance & Speech Bubble Jitter
class_name ResonantDeliberation extends Control

@export var max_jitter_offset: float = 6.0
@export var jitter_frequency: float = 24.0

var current_dissonance: float = 0.0 # [0.0 - 1.0]
var target_offset: Vector2 = Vector2.ZERO

func _process(delta: float) -> void:
	if current_dissonance > 0.01:
		var time = Time.get_ticks_msec() * 0.001 * jitter_frequency
		var jx = (sin(time * 1.7) + cos(time * 2.3)) * max_jitter_offset * current_dissonance
		var jy = (cos(time * 1.9) + sin(time * 2.7)) * max_jitter_offset * current_dissonance
		position = target_offset + Vector2(jx, jy)
	else:
		position = target_offset

func set_dissonance(amount: float) -> void:
	current_dissonance = clampf(amount, 0.0, 1.0)
