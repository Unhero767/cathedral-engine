# PhaseChangeEngine.gd
# Law of Friction: Fluid Mercury vs. Static Bronze Phase Transitions
class_name PhaseChangeEngine extends Node

signal phase_shifted(is_mercury: bool, dynamic_friction: float)

enum PhaseState {
	FLUID_MERCURY, # mu = 0.08: High slip, evasion, zero poise
	STATIC_BRONZE  # mu = 0.92: High traction, immovable poise, kinetic deflection
}

const FRICTION_MERCURY: float = 0.08
const FRICTION_BRONZE: float = 0.92

var current_phase: PhaseState = PhaseState.FLUID_MERCURY
var current_friction: float = FRICTION_MERCURY
var transition_progress: float = 1.0

func _physics_process(delta: float) -> void:
	var target_f = FRICTION_MERCURY if current_phase == PhaseState.FLUID_MERCURY else FRICTION_BRONZE
	current_friction = move_toward(current_friction, target_f, delta * 4.0)

func shift_phase(target_phase: PhaseState) -> void:
	if current_phase != target_phase:
		current_phase = target_phase
		var is_merc = (current_phase == PhaseState.FLUID_MERCURY)
		emit_signal("phase_shifted", is_merc, current_friction)

func toggle_phase() -> PhaseState:
	if current_phase == PhaseState.FLUID_MERCURY:
		shift_phase(PhaseState.STATIC_BRONZE)
	else:
		shift_phase(PhaseState.FLUID_MERCURY)
	return current_phase

func get_friction_coefficient() -> float:
	return current_friction
