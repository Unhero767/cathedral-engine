extends Node
# SoulframeEngine.gd - Phase Change Engine & Damping Ratio Modulation

signal phase_changed(previous_phase: String, new_phase: String, zeta: float)

const ELEMENT_PROPERTIES := {
	"Silver": {"polarity": "FLUID", "zeta": 0.15, "constant": "Teal"},
	"Mercury": {"polarity": "FLUID", "zeta": 0.25, "constant": "Teal"},
	"Lead": {"polarity": "STATIC", "zeta": 0.95, "constant": "Blue"},
	"Bronze": {"polarity": "STATIC", "zeta": 0.85, "constant": "Gold"}
}

var current_phase := "Lead" # Default static anchor
var current_zeta := 0.95

## Triggers an elemental Phase Change between Fluid and Static states
func execute_phase_change(target_element: String) -> Dictionary:
	if not ELEMENT_PROPERTIES.has(target_element):
		push_error("[SoulframeEngine] Invalid element: " + target_element)
		return {}
		
	var element_data: Dictionary = ELEMENT_PROPERTIES[target_element]
	var previous_phase := current_phase
	
	current_phase = target_element
	current_zeta = element_data["zeta"]
	
	print("[SoulframeEngine] Phase Change: %s -> %s | Damping Ratio (zeta): %.2f" % [
		previous_phase, current_phase, current_zeta
	])
	
	phase_changed.emit(previous_phase, current_phase, current_zeta)
	
	var payload := {
		"type": "Phase_Change_Execution",
		"previous_phase": previous_phase,
		"new_phase": current_phase,
		"damping_ratio_zeta": current_zeta,
		"spectral_constant": element_data["constant"]
	}
	
	SovereignInterface.request_archive_write(payload)
	return payload
