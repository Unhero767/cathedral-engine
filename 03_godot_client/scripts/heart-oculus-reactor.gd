# heart-oculus-reactor.gd
# ==============================================================================
#            NYX AURELIA: SYSTEMIC GAME ENGINE RUNTIME SINGLETON
#        AUTOLOAD SINGLETON: HeartOculusReactor (HeartOculusReactor.gd)
# ==============================================================================
# This singleton manages paraconsistent state tracking and dynamic combat UI 
# updates within the Godot Engine (compatible with Godot 4.x / GDScript 2.0).
# Governed by the core axiom: Emotion = Physics = Magic = Biology = Architecture.
# ==============================================================================

extends Node

# ------------------------------------------------------------------------------
# 1. CORE EVENT SIGNALS (FOR COMBAT UI & SPECTRAL CONTROLLER LINKAGE)
# ------------------------------------------------------------------------------
## Emitted on every tick of the reactor's paraconsistent state transition.
signal state_changed(t: float, f: float, dialetheism: float, underdetermination: float)

## Emitted when the overall ontological system state shifts classifications.
signal system_state_updated(state_name: String, state_color: Color)

## Emitted when a critical life-threatening or environmental anomaly occurs.
signal critical_anomaly_triggered(description: String)

## Emitted when Dialetheism (D) crosses the threshold into permanent paraconsistent stabilization.
signal harmonic_scar_stabilized()

# ------------------------------------------------------------------------------
# 2. STATE VECTOR & CALIBRATION PARAMETERS
# ------------------------------------------------------------------------------
# S = (t, f)^T where t = Assertability (Consciousness), f = Deniability (Physical Cessation)
var t: float = 1.0 ## Assertability Support Vector (0.0 to 1.0)
var f: float = 0.0 ## Deniability Support Vector (0.0 to 1.0)

# Isomorphism Calibration coefficients: [E, P, M, B, A]
var Emotion: float = 0.05      # E: Range [0, 1] - Empathetic mesh resonance
var Physics: float = 0.95      # P: Range [0, 1] - Physical structural pressure/coherence
var Magic: float = 0.0         # M: Range [0, 1] - Meta-Lattice code alignment
var Biology: float = 0.95      # B: Range [0, 1] - Biological vital/cellular integrity
var Architecture: float = 0.1  # A: Range [0, 1] - Hard structural anchoring/pipes

# Simulation Constants
var A_field_resonance: float = 1.15 ## R_A: Systemic background frequency (Hz)
var time_step_modifier: float = 0.02 ## dt: Simulation speed/delta multiplier

# Operational Flags
var is_simulation_active: bool = false

# ------------------------------------------------------------------------------
# 3. ONTO-STATE CLASSIFICATIONS
# ------------------------------------------------------------------------------
enum CalibrationState {
	CLASSICAL_TRUE,      # Normal biological life (t=1, f=0, D=0)
	TRANSITION,          # Active dimensional or vital destabilization
	HARMONIC_SCAR,       # Stabilized persistent contradiction (t=1, f~1, D>0.90)
	TOTAL_DISSOLUTION    # Complete structural and physical collapse
}

var current_state: CalibrationState = CalibrationState.CLASSICAL_TRUE

# ------------------------------------------------------------------------------
# 4. ENGINE LIFE CYCLE METRICS
# ------------------------------------------------------------------------------
func _ready() -> void:
	# Register in the console and initialize the default state
	reset_reactor()

func _process(delta: float) -> void:
	if is_simulation_active:
		# Scale Euler integration steps with active engine frame delta
		var scaled_dt: float = delta * time_step_modifier * 50.0
		_step_simulation(scaled_dt)

# ------------------------------------------------------------------------------
# 5. PUBLIC CALIBRATION INTERFACES (FOR COMBAT & ENVIRONMENTAL TRIGGERING)
# ------------------------------------------------------------------------------
## Resets the Heart-Oculus reactor to standard baseline human parameters.
func reset_reactor() -> void:
	t = 1.0
	f = 0.0
	Emotion = 0.05
	Physics = 0.95
	Magic = 0.0
	Biology = 0.95
	Architecture = 0.1
	A_field_resonance = 1.15
	is_simulation_active = false
	current_state = CalibrationState.CLASSICAL_TRUE
	_emit_state_update()

## Simulates the Sector Four Atmospheric Collapse event (triggers dialetheic buffer)
func trigger_sector_four_collapse() -> void:
	is_simulation_active = true
	
	# Severe physical and biological crash
	Biology = 0.0
	Physics = 0.02
	
	# Sovereign emotional, magical, and architectural rescue activated by Nyx and Mara
	Emotion = 0.98
	Magic = 0.95
	Architecture = 0.90
	
	emit_signal("critical_anomaly_triggered", "CRITICAL ANOMALY: Sector Four Depressurization. Dialetheic Buffer activated.")
	_emit_state_update()

## Manual adjustment of A-Field variables in real-time combat UI
func adjust_isomorphism_variable(variable_name: String, value: float) -> void:
	match variable_name.to_upper():
		"E", "EMOTION": Emotion = clamp(value, 0.0, 1.0)
		"P", "PHYSICS": Physics = clamp(value, 0.0, 1.0)
		"M", "MAGIC": Magic = clamp(value, 0.0, 1.0)
		"B", "BIOLOGY": Biology = clamp(value, 0.0, 1.0)
		"A", "ARCHITECTURE": Architecture = clamp(value, 0.0, 1.0)
		"RESONANCE", "RA": A_field_resonance = max(0.0, value)
	_emit_state_update()

# ------------------------------------------------------------------------------
# 6. MATHEMATICAL CALCULATIONS (EULER INTEGRATION LOOP)
# ------------------------------------------------------------------------------
func _step_simulation(step_dt: float) -> void:
	var vectors: Vector2 = _calculate_transition_vectors()
	
	# Apply transition vectors to the State Superposition Vector with strict boundary clamping [0.0, 1.0]
	t = clamp(t + vectors.x * step_dt, 0.0, 1.0)
	f = clamp(f + vectors.y * step_dt, 0.0, 1.0)
	
	_evaluate_system_state()
	_emit_state_update()

func _calculate_transition_vectors() -> Vector2:
	# dt/dτ = R_A * (E * M * A) - (1 - B) * (1 - M) * t
	var rescue_t: float = A_field_resonance * (Emotion * Magic * Architecture)
	var decay_t: float = (1.0 - Biology) * (1.0 - Magic) * t
	var dt_rate: float = rescue_t - decay_t
	
	# df/dτ = (1 - P) * (1 - B) - (R_A * A) * f
	var physical_failure: float = (1.0 - Physics) * (1.0 - Biology)
	var decay_f: float = (A_field_resonance * Architecture) * f
	var df_rate: float = physical_failure - decay_f
	
	return Vector2(dt_rate, df_rate)

# ------------------------------------------------------------------------------
# 7. TELEMETRY GETTERS (FOR UI METERS & SHADER CALIBRATION)
# ------------------------------------------------------------------------------
## D = min(t, f) -> Quantifies the paraconsistent "glowing scar" magnitude
func get_dialetheism_index() -> float:
	return min(t, f)

## U = 1 - max(t, f) -> Quantifies empty space / raw systemic potential
func get_potential_index() -> float:
	return 1.0 - max(t, f)

# ------------------------------------------------------------------------------
# 8. INTERNAL STABILIZATION MONITORING & UI SHADERS
# ------------------------------------------------------------------------------
func _evaluate_system_state() -> void:
	var D: float = get_dialetheism_index()
	var U: float = get_potential_index()
	var previous_state: CalibrationState = current_state
	
	if D > 0.90:
		current_state = CalibrationState.HARMONIC_SCAR
		if previous_state != CalibrationState.HARMONIC_SCAR:
			emit_signal("harmonic_scar_stabilized")
	elif U > 0.80:
		current_state = CalibrationState.TOTAL_DISSOLUTION
	elif D < 0.10:
		current_state = CalibrationState.CLASSICAL_TRUE
	else:
		current_state = CalibrationState.TRANSITION

func _emit_state_update() -> void:
	var D: float = get_dialetheism_index()
	var U: float = get_potential_index()
	emit_signal("state_changed", t, f, D, U)
	
	var state_name: String = ""
	var state_color: Color = Color.WHITE
	
	match current_state:
		CalibrationState.CLASSICAL_TRUE:
			state_name = "CLASSICAL NOMINAL"
			state_color = Color(0.46, 0.82, 0.35, 1.0) # Soft Emerald Green
		CalibrationState.TRANSITION:
			state_name = "TRANSITIONAL MATRIX"
			state_color = Color(0.95, 0.76, 0.20, 1.0) # Amber Yellow
		CalibrationState.HARMONIC_SCAR:
			state_name = "HARMONIC SCAR (STABILIZED)"
			state_color = Color(0.60, 0.36, 0.82, 1.0) # Vibrant Violet
		CalibrationState.TOTAL_DISSOLUTION:
			state_name = "CRITICAL SYSTEM EXHAUSTION"
			state_color = Color(0.90, 0.22, 0.22, 1.0) # Alarming Red
			
	emit_signal("system_state_updated", state_name, state_color)
