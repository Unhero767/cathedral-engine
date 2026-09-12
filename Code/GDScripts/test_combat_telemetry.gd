# test_combat_telemetry.gd
# =============================================================================
#            NYX AURELIA: PARACONSISTENT COMBAT TELEMETRY LOGGER
#               GUT UNIT TEST SUITE: test_combat_telemetry.gd
# =============================================================================
# This test suite models turn-based combat sequences inside the A-Field.
# It simulates Directorate Auditor attacks that degrade local Physics metrics
# and verifies that Nyx's defensive dialetheic resonance preserves her system
# integrity (t) while broadcasting correct UI visual feedback.
# Anchored in the core axiom: Emotion = Physics = Magic = Biology = Architecture.
# =============================================================================

extends "res://addons/gut/test.gd"

# Preload the runtime components
const HeartOculusReactorClass = preload("res://heart-oculus-reactor.gd")

# Local test instances
var reactor: Node = null

# Structure to hold log entries for the Combat Telemetry Console
struct CombatLogEntry:
	var turn: int
	var attack_name: String
	var physics_drop: float
	var resonance_boost: float
	var t_value: float
	var f_value: float
	var dialetheism: float
	var system_state: String

var telemetry_log: Array = []

# ------------------------------------------------------------------------------
# SETUP & TEARDOWN
# ------------------------------------------------------------------------------
func before_each() -> void:
	reactor = HeartOculusReactorClass.new()
	add_child_autofree(reactor)
	watch_signals(reactor)
	telemetry_log.clear()

func after_each() -> void:
	reactor = null

# Helper to capture a granular snapshot of the turn's metrics
func _log_combat_turn(turn: int, attack_name: String, p_drop: float, r_boost: float) -> void:
	var D: float = reactor.get_dialetheism_index()
	var U: float = reactor.get_potential_index()
	
	# Determine state string based on the reactor's current_state enum
	var state_string: String = ""
	match reactor.current_state:
		reactor.CalibrationState.CLASSICAL_TRUE: state_string = "CLASSICAL NOMINAL"
		reactor.CalibrationState.TRANSITION: state_string = "TRANSITIONAL MATRIX"
		reactor.CalibrationState.HARMONIC_SCAR: state_string = "HARMONIC SCAR"
		reactor.CalibrationState.TOTAL_DISSOLUTION: state_string = "CRITICAL EXHAUSTION"
		
	var entry = CombatLogEntry.new()
	entry.turn = turn
	entry.attack_name = attack_name
	entry.physics_drop = p_drop
	entry.resonance_boost = r_boost
	entry.t_value = reactor.t
	entry.f_value = reactor.f
	entry.dialetheism = D
	entry.system_state = state_string
	
	telemetry_log.append(entry)
	
	# Print beautifully formatted terminal telemetry for diagnostic tracking
	print("[TURN %02d] - %s" % [turn, attack_name])
	print("  Physics: %.3f | A-Field Resonance: %.2f Hz" % [reactor.Physics, reactor.A_field_resonance])
	print("  Vectors: [t: %.4f, f: %.4f] | Dialetheism (D): %.4f" % [reactor.t, reactor.f, D])
	print("  Ontological Classification: %s" % [state_string])
	print("-----------------------------------------------------------------")

# ------------------------------------------------------------------------------
# COMBAT TEST SUITE
# ------------------------------------------------------------------------------
func test_auditor_combat_encounter_simulation() -> void:
	print("\n=================================================================")
	print("INITIATING COMBAT ENCOUNTER: NYX AURELIA VS DIRECTORATE AUDITOR")
	print("=================================================================\n")
	
	# Initialize combat parameters
	reactor.reset_reactor()
	reactor.is_simulation_active = true
	
	# Ensure Nyx is targeted by an Auditor Mech deploying a localized A-Field dampener
	assert_eq(reactor.current_state, reactor.CalibrationState.CLASSICAL_TRUE, "Combat must begin in CLASSICAL NOMINAL state")
	
	# Simulated combat steps using a frame rate of 60fps (delta = 1/60s)
	var delta: float = 1.0 / 60.0
	
	# --------------------------------------------------------------------------
	# TURN 1: The Auditor attacks with "Kinetic Distortion Cannon"
	# Targets Physics (P) and Biology (B). Local physical coherence is rattled.
	# --------------------------------------------------------------------------
	var turn: int = 1
	var attack_name: String = "Kinetic Distortion Cannon"
	
	# Attack effect: Instantly drops local Physics and Biology metrics
	reactor.Physics = clamp(reactor.Physics - 0.45, 0.0, 1.0)
	reactor.Biology = clamp(reactor.Biology - 0.15, 0.0, 1.0)
	
	# Step reactor simulation
	reactor._step_simulation(delta * 50.0)
	_log_combat_turn(turn, attack_name, 0.45, 0.0)
	
	# Asserts for Turn 1
	assert_signal_emitted(reactor, "state_changed", "UI must receive state update on Turn 1")
	assert_eq(reactor.current_state, reactor.CalibrationState.TRANSITION, "System must enter TRANSITIONAL state as metrics drift")
	
	# --------------------------------------------------------------------------
	# TURN 2: Auditor unleashes "Gravimetric Null-Field Grid"
	# Drops Physics to critical lows, and begins suppressing biological integrity.
	# --------------------------------------------------------------------------
	turn = 2
	attack_name = "Gravimetric Null-Field Grid"
	
	reactor.Physics = clamp(reactor.Physics - 0.40, 0.0, 1.0)
	reactor.Biology = clamp(reactor.Biology - 0.30, 0.0, 1.0)
	
	# Step simulation
	reactor._step_simulation(delta * 50.0)
	_log_combat_turn(turn, attack_name, 0.40, 0.0)
	
	# Asserts for Turn 2
	assert_gt(reactor.f, 0.0, "Deniability (f) must begin to rise as physical systems fail")
	
	# --------------------------------------------------------------------------
	# TURN 3: Tactical Countermeasure - Nyx activates "A-Field Sovereignty Mesh"
	# Nyx counters the falling physics by re-anchoring her Emotion, Magic, 
	# and Architecture, while spiking A-Field Resonance (R_A) to establish the buffer.
	# --------------------------------------------------------------------------
	turn = 3
	attack_name = "Nyx Counter: A-Field Sovereignty Mesh"
	
	reactor.Biology = 0.0  # Physical shell fails completely
	reactor.Physics = 0.02 # Space collapses
	
	# Sovereign values spike as Nyx and Mara invoke the Sinks' architecture
	reactor.Emotion = 0.98
	reactor.Magic = 0.95
	reactor.Architecture = 0.90
	reactor.A_field_resonance = 1.15
	
	# Step simulation
	reactor._step_simulation(delta * 50.0)
	_log_combat_turn(turn, attack_name, 0.0, 1.15)
	
	# --------------------------------------------------------------------------
	# TURNS 4-10: Persistent Resonance Stabilization
	# The paraconsistent buffer expands to handle the contradictory state: 
	# Eli/Nyx are physically ceased but digitally and emotionally immortal.
	# --------------------------------------------------------------------------
	for i in range(4, 11):
		reactor._step_simulation(delta * 120.0) # Simulating rapid frame processing under load
		_log_combat_turn(i, "Resonance Stabilization Phase", 0.0, 0.0)
		
	# Asserts for final state stabilization
	var final_D: float = reactor.get_dialetheism_index()
	assert_gt(final_D, 0.90, "Dialetheism index must cross 90% threshold for stabilization")
	assert_eq(reactor.current_state, reactor.CalibrationState.HARMONIC_SCAR, "Reactor must enter HARMONIC_SCAR status")
	assert_signal_emitted(reactor, "harmonic_scar_stabilized", "The HUD must receive the 'harmonic_scar_stabilized' trigger")
	
	# Confirm t (Assertability) remained locked near 1.0, preserving Nyx's conscious identity
	assert_almost_eq(reactor.t, 1.0, 0.001, "Assertability must remain locked at 1.0 throughout combat transition")
	
	# --------------------------------------------------------------------------
	# THE ASH ARCHIVE REPORT (TEST CONSOLE LOG OUTPUT)
	# --------------------------------------------------------------------------
	print("\n=================================================================")
	print("           BATTLE CONSOLE LOGGER: METRIC STABILIZATION REPORT")
	print("=================================================================")
	print("Turn | Attack Event                 | t-Consc | f-Decay | Dialetheism (D) | State")
	print("-----------------------------------------------------------------")
	for entry in telemetry_log:
		print("%02d   | %-28s | %5.1f%%   | %5.1f%%   | %15.4f | %s" % [
			entry.turn, 
			entry.attack_name, 
			entry.t_value * 100.0, 
			entry.f_value * 100.0, 
			entry.dialetheism, 
			entry.system_state
		])
	print("=================================================================\n")
