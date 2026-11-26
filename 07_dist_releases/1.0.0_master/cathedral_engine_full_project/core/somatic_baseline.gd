# SomaticBaseline.gd
# 42.0 Hz Carrier Wave & 1.5 Hz Somatic Clock with Neuro-Respiratory Synchronization
class_name SomaticBaseline extends Node

signal somatic_tick_1_5hz(phase: float, amplitude: float)
signal carrier_tick_42hz(phase: float)
signal breathe_cycle_event(is_inhale: bool, compliance_kpa: float)

# Frequency Constants
const CARRIER_FREQ_HZ: float = 42.0   # Autopoietic Seed & Civic Processing
const SOMATIC_FREQ_HZ: float = 1.5    # Somatic Heartbeat / Delta Pulse
const RESPIRATORY_CADENCE_HZ: float = 0.1667 # 10 breaths/minute (6.0s cycle)
const ALVEOLAR_COMPLIANCE_KPA: float = 1.618  # Golden Ratio Pressure Modulation

# Phase Accumulators
var carrier_phase: float = 0.0
var somatic_phase: float = 0.0
var breath_phase: float = 0.0

var total_elapsed_time: float = 0.0
var is_inhaling: bool = true
var last_somatic_pulse: float = 0.0

func _physics_process(delta: float) -> void:
	total_elapsed_time += delta
	
	# Advance 42.0 Hz carrier
	carrier_phase = fmod(carrier_phase + CARRIER_FREQ_HZ * delta, 1.0)
	emit_signal("carrier_tick_42hz", carrier_phase)
	
	# Advance 1.5 Hz somatic clock
	var prev_somatic_phase = somatic_phase
	somatic_phase = fmod(somatic_phase + SOMATIC_FREQ_HZ * delta, 1.0)
	var somatic_amp = sin(somatic_phase * TAU)
	
	if prev_somatic_phase > somatic_phase: # Completed a 1.5 Hz cycle
		emit_signal("somatic_tick_1_5hz", somatic_phase, somatic_amp)
		
	# Advance 0.1667 Hz respiratory rhythm
	var prev_breath = breath_phase
	breath_phase = fmod(breath_phase + RESPIRATORY_CADENCE_HZ * delta, 1.0)
	var now_inhaling = breath_phase < 0.5
	if now_inhaling != is_inhaling:
		is_inhaling = now_inhaling
		emit_signal("breathe_cycle_event", is_inhaling, ALVEOLAR_COMPLIANCE_KPA)

# Get synchronized somatic pulse intensity [0.0 - 1.0] for shaders & lights
func get_somatic_pulse_intensity() -> float:
	return (sin(somatic_phase * TAU) + 1.0) * 0.5

# Get carrier high-frequency modulation value [-1.0, 1.0]
func get_carrier_modulation() -> float:
	return sin(carrier_phase * TAU)

# Returns the current lung pressure in kPa
func get_current_respiratory_pressure() -> float:
	var factor = sin(breath_phase * TAU)
	return ALVEOLAR_COMPLIANCE_KPA * factor
