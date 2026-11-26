# LithiumResonator.gd
# Sonic Anxiety Tuning Fork & Harmonic Lock Dampening
class_name LithiumResonator extends Node

signal harmonic_lock_engaged(dampening_power: float)
signal anxiety_neutralized(entropy_reduced: float)

var tuning_fork_frequency: float = 432.0 # Hz
var harmonic_lock_active: bool = false
var dampening_factor: float = 0.75

func engage_harmonic_lock() -> void:
	harmonic_lock_active = true
	emit_signal("harmonic_lock_engaged", dampening_factor)
	
	if AFieldManager:
		AFieldManager.stabilize_field(1.5)
		emit_signal("anxiety_neutralized", 1.5)

func release_harmonic_lock() -> void:
	harmonic_lock_active = false
