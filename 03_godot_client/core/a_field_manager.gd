# class_name AFieldManager
extends Node

signal field_distorted(divergence: Vector2, dominant_constant: int)
signal k_index_changed(new_k: int)

var ego_density: float = SpectralConstants.BASELINE_EGO_DENSITY
var k_index: int = 0
var spectral_weights: Dictionary = {}

func _ready() -> void:
	for constant in SpectralConstants.Constant.values():
		spectral_weights[constant] = 0.0

func update_emotional_vector(constant: int, intensity: float) -> void:
	spectral_weights[constant] = clamp(intensity, 0.0, 100.0)
	_evaluate_field_state()

func _evaluate_field_state() -> void:
	var total_intensity: float = 0.0
	var dominant: int = SpectralConstants.Constant.THETA_GOLD
	var max_val: float = -1.0
	
	for constant in spectral_weights.keys():
		var val: float = spectral_weights[constant]
		total_intensity += val
		if val > max_val:
			max_val = val
			dominant = constant
	
	if spectral_weights.has(SpectralConstants.Constant.NULL_OBSIDIAN) and spectral_weights[SpectralConstants.Constant.NULL_OBSIDIAN] > 50.0:
		k_index = int(clamp(spectral_weights[SpectralConstants.Constant.NULL_OBSIDIAN] / 15.0, 0, 7))
	else:
		k_index = int(clamp(total_intensity / 40.0, 0, 7))
	
	emit_signal("k_index_changed", k_index)
	emit_signal("field_distorted", Vector2(total_intensity * 0.1, max_val * 0.1), dominant)
