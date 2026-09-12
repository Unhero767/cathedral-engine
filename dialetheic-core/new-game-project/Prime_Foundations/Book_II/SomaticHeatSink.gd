extends Node
# SomaticHeatSink.gd - Thermodynamic Heat-Sink & 1.5 Hz Somatic Shunt

signal heat_shunted(metalogical_heat_units: float, somatic_freq_hz: float)

var current_somatic_baseline_hz: float = 1.5
var total_heat_dissipated: float = 0.0

## Shunts processing friction from 42.0 Hz master processing into 1.5 Hz somatic baseline
func shunt_metalogical_heat(processing_friction: float) -> Dictionary:
	print("[SomaticHeatSink] Ingesting processing friction: %.2f units..." % processing_friction)
	
	# Thermal step-down: 42.0 Hz -> 1.5 Hz
	var shunted_heat: float = processing_friction * 0.85
	total_heat_dissipated += shunted_heat
	
	print("[SomaticHeatSink] Heat shunted into 1.5 Hz Somatic Sink | Dissipated: %.2f | Total: %.2f" % [
		shunted_heat, total_heat_dissipated
	])
	
	heat_shunted.emit(shunted_heat, current_somatic_baseline_hz)
	
	var payload := {
		"type": "Somatic_Heat_Shunt",
		"input_friction_units": processing_friction,
		"shunted_heat_units": shunted_heat,
		"somatic_baseline_hz": current_somatic_baseline_hz,
		"spectral_constant": "Red"
	}
	
	SovereignInterface.request_archive_write(payload)
	return payload
