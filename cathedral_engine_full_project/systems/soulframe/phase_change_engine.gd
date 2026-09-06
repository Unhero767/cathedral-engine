class_name PhaseChangeEngine
extends Node

signal phase_shifted(old_state: int, new_state: int, damping_ratio: float)

enum ElementState {
	SILVER_FLUID,  # Low damping, high evasion / reflection
	MERCURY_FLUID, # Variable damping, kinetic flux
	LEAD_STATIC,   # High damping, absolute barrier
	BRONZE_STATIC  # High damping, structural endurance
}

var current_element: ElementState = ElementState.SILVER_FLUID
var damping_ratio_zeta: float = 0.1

func shift_phase(target_element: ElementState) -> void:
	var old_state: int = current_element
	current_element = target_element
	
	match target_element:
		ElementState.SILVER_FLUID:
			damping_ratio_zeta = 0.05
		ElementState.MERCURY_FLUID:
			damping_ratio_zeta = 0.25
		ElementState.LEAD_STATIC:
			damping_ratio_zeta = 0.95
		ElementState.BRONZE_STATIC:
			damping_ratio_zeta = 0.80
	
	AshArchive.append_log("PHASE_CHANGE", {
		"from": ElementState.keys()[old_state],
		"to": ElementState.keys()[target_element],
		"zeta": damping_ratio_zeta
	})
	
	emit_signal("phase_shifted", old_state, target_element, damping_ratio_zeta)
