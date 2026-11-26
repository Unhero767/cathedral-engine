# AFieldManager.gd
# Architectonic Field (A-Field) Gravitational Curvature: C_l = nabla . L & K-Index Dynamics
class_name AFieldManager extends Node

signal field_curvature_changed(new_curvature: float, gradient: Vector2)
signal k_index_spiked(k_index: float, warning_level: String)
signal metalogical_crystallization(consistency_coeff: float)

const BASE_RADIUS: float = 240.0
const K_INDEX_THRESHOLD_CRITICAL: float = 7.5
const DELTA_CRITICAL: float = 0.65

# Field Telemetry
var field_curvature: float = 0.0          # C_l = ∇·L
var field_gradient: Vector2 = Vector2.ZERO # ∇L
var k_index: float = 1.2                  # Kenoma / Chaos Turbulence index [0.0 - 9.0]
var divergence_vector: float = 0.0142     # ∇ Ex°
var consistency_coefficient: float = 0.948 # C_tau = W_circ_A / epsilon_local
var metalogical_burn_risk: float = 0.0

# Update field physics at 60 Hz
func _physics_process(delta: float) -> void:
	# Subtle autonomic decay / baseline fluctuation
	var target_k = clampf(k_index + sin(Time.get_ticks_msec() * 0.001) * 0.02 * delta, 0.0, 9.0)
	k_index = move_toward(k_index, target_k, delta * 0.1)

# Calculates localized field curvature C_l = div(L)
func calculate_curvature(lattice_vectors: Array[Vector2], spacing: float = 32.0) -> float:
	if lattice_vectors.size() < 2:
		return 0.0
	var sum_div: float = 0.0
	for i in range(lattice_vectors.size() - 1):
		var delta_v = lattice_vectors[i + 1] - lattice_vectors[i]
		sum_div += (delta_v.x + delta_v.y) / spacing
	
	field_curvature = sum_div / float(lattice_vectors.size())
	emit_signal("field_curvature_changed", field_curvature, field_gradient)
	return field_curvature

# Ingest an entropy / trauma spike to modulate K-Index
func inject_entropy_perturbation(magnitude: float, source: String = "GlitchWastes") -> void:
	k_index = clampf(k_index + magnitude, 0.0, 9.0)
	divergence_vector = clampf(divergence_vector + magnitude * 0.01, 0.0, 1.0)
	
	# Update consistency coefficient: C_tau = W_circ_A / (1.0 + k_index * 0.2)
	consistency_coefficient = clampf(1.0 / (1.0 + k_index * 0.15), 0.05, 1.0)
	
	if k_index >= K_INDEX_THRESHOLD_CRITICAL:
		emit_signal("k_index_spiked", k_index, "CRITICAL_KENOMA_SHEAR")
	elif k_index >= 4.5:
		emit_signal("k_index_spiked", k_index, "HIGH_TURBULENCE")
		
	if consistency_coefficient < DELTA_CRITICAL:
		emit_signal("metalogical_crystallization", consistency_coefficient)

# Apply gravitational pull calculation on an entity
func get_gravitational_pull(entity_position: Vector2, center_position: Vector2, entity_mass: float) -> Vector2:
	var diff = center_position - entity_position
	var dist = maxf(diff.length(), 16.0)
	var force_mag = (field_curvature * 500.0 + k_index * 20.0) * entity_mass / (dist * dist)
	return diff.normalized() * clampf(force_mag, -200.0, 200.0)

# Resets or dampens K-index via Somatic Carrier lock
func stabilize_field(amount: float) -> void:
	k_index = maxf(0.5, k_index - amount)
	consistency_coefficient = minf(1.0, consistency_coefficient + amount * 0.2)
	metalogical_burn_risk = maxf(0.0, metalogical_burn_risk - amount)
