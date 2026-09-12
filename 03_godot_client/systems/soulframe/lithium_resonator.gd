class_name LithiumResonator
extends Node

signal scan_completed(differential: float, harmonic_lock: bool)

var is_locked: bool = false
var target_frequency: float = 42.0

func scan_lattice(soul_freq: float, env_freq: float, stress: float) -> float:
	var safe_stress: float = max(stress, 0.1)
	var resonance_diff: float = (soul_freq - env_freq) / safe_stress
	emit_signal("scan_completed", resonance_diff, is_locked)
	return resonance_diff

func toggle_harmonic_lock(locked: bool, freq: float = 42.0) -> void:
	is_locked = locked
	target_frequency = freq
	AshArchive.append_log("LITHIUM_LOCK", {"locked": locked, "freq": freq})
