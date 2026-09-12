# test_reactor_integration.gd
# =============================================================================
#            NYX AURELIA: SYSTEMIC GAME ENGINE RUNTIME INTEGRATION TEST
#               GUT UNIT TEST SUITE: test_reactor_integration.gd
# =============================================================================
# This test suite verifies paraconsistent state transitions, extreme boundary 
# clamping, signal broadcasts, and isomorphic calibration variables under GUT 4.x.
# Anchored in the core axiom: Emotion = Physics = Magic = Biology = Architecture.
# =============================================================================

extends "res://addons/gut/test.gd"

# Preload the runtime singleton class for isolated testing
const HeartOculusReactorClass = preload("res://heart-oculus-reactor.gd")

# Local test instance to avoid global state pollution
var reactor: Node = null

# ------------------------------------------------------------------------------
# SETUP & TEARDOWN
# ------------------------------------------------------------------------------
func before_each() -> void:
	# Instantiate a clean reactor node for each test case
	reactor = HeartOculusReactorClass.new()
	add_child_autofree(reactor)
	watch_signals(reactor)

func after_each() -> void:
	# Clean up is handled automatically by GUT's autofree, 
	# but we explicitly null the reference to be safe
	reactor = null

# ------------------------------------------------------------------------------
# 1. INITIALIZATION & CALIBRATION TESTS
# ------------------------------------------------------------------------------
func test_initialization_defaults() -> void:
	# Assert baseline parameters match the Directorate's pristine starting parameters
	assert_eq(reactor.t, 1.0, "Initial Assertability (t) must be exactly 1.0 (Classical True)")
	assert_eq(reactor.f, 0.0, "Initial Deniability (f) must be exactly 0.0 (Classical True)")
	assert_eq(reactor.Emotion, 0.05, "Initial Emotion (E) must start at 0.05")
	assert_eq(reactor.Physics, 0.95, "Initial Physics (P) must start at 0.95")
	assert_eq(reactor.Magic, 0.0, "Initial Magic (M) must start at 0.0")
	assert_eq(reactor.Biology, 0.95, "Initial Biology (B) must start at 0.95")
	assert_eq(reactor.Architecture, 0.1, "Initial Architecture (A) must start at 0.1")
	assert_eq(reactor.A_field_resonance, 1.15, "Initial A-Field Resonance must be 1.15 Hz")
	assert_false(reactor.is_simulation_active, "The simulation must be inactive by default")
	assert_eq(reactor.current_state, reactor.CalibrationState.CLASSICAL_TRUE, "System state must start as CLASSICAL_TRUE")

func test_reset_reactor() -> void:
	# Distort parameters to extreme non-equilibrium values
	reactor.t = 0.45
	reactor.f = 0.85
	reactor.Emotion = 0.99
	reactor.Biology = 0.0
	reactor.current_state = reactor.CalibrationState.TRANSITION
	reactor.is_simulation_active = true
	
	# Execute reset sequence
	reactor.reset_reactor()
	
	# Assert all variables are restored to their pristine defaults
	assert_eq(reactor.t, 1.0, "Reset must restore t to 1.0")
	assert_eq(reactor.f, 0.0, "Reset must restore f to 0.0")
	assert_eq(reactor.Emotion, 0.05, "Reset must restore Emotion to 0.05")
	assert_eq(reactor.Biology, 0.95, "Reset must restore Biology to 0.95")
	assert_false(reactor.is_simulation_active, "Reset must deactivate the simulation loop")
	assert_eq(reactor.current_state, reactor.CalibrationState.CLASSICAL_TRUE, "Reset must return state to CLASSICAL_TRUE")

# ------------------------------------------------------------------------------
# 2. VARIABLE ADJUSTMENT & CLAMPING TESTS
# ------------------------------------------------------------------------------
func test_adjust_isomorphism_variables() -> void:
	# Test nominal adjustments
	reactor.adjust_isomorphism_variable("E", 0.75)
	assert_eq(reactor.Emotion, 0.75, "Emotion (E) adjustment failed")
	
	reactor.adjust_isomorphism_variable("PHYSICS", 0.50)
	assert_eq(reactor.Physics, 0.50, "Physics (P) adjustment failed")

	reactor.adjust_isomorphism_variable("resonance", 2.5)
	assert_eq(reactor.A_field_resonance, 2.5, "A-Field Resonance adjustment failed")

func test_isomorphism_variable_clamping() -> void:
	# Test upper boundary clamping [1.0]
	reactor.adjust_isomorphism_variable("M", 5.5)
	assert_eq(reactor.Magic, 1.0, "Magic (M) must clamp at a maximum of 1.0")
	
	reactor.adjust_isomorphism_variable("B", 1.05)
	assert_eq(reactor.Biology, 1.0, "Biology (B) must clamp at a maximum of 1.0")

	# Test lower boundary clamping [0.0]
	reactor.adjust_isomorphism_variable("A", -0.2)
	assert_eq(reactor.Architecture, 0.0, "Architecture (A) must clamp at a minimum of 0.0")
	
	reactor.adjust_isomorphism_variable("RESONANCE", -10.0)
	assert_eq(reactor.A_field_resonance, 0.0, "A-Field Resonance must clamp at a minimum of 0.0")

# ------------------------------------------------------------------------------
# 3. EXTREME DELTA BOUNDARY PROTECTION
# ------------------------------------------------------------------------------
func test_boundary_clamping_under_massive_positive_delta() -> void:
	reactor.trigger_sector_four_collapse()
	
	# Inject an absurdly high delta step (simulating a severe engine lag spike or system hang)
	# This massive delta would classically cause an explosive overshoot of the vectors
	var massive_delta: float = 100000.0
	reactor._step_simulation(massive_delta)
	
	# Verify that the boundary protection system successfully restricted both parameters to [0.0, 1.0]
	assert_ge(reactor.t, 0.0, "Assertability must never drop below 0.0 even under massive delta")
	assert_le(reactor.t, 1.0, "Assertability must never exceed 1.0 even under massive delta")
	assert_ge(reactor.f, 0.0, "Deniability must never drop below 0.0 even under massive delta")
	assert_le(reactor.f, 1.0, "Deniability must never exceed 1.0 even under massive delta")

func test_boundary_clamping_under_massive_negative_delta() -> void:
	reactor.trigger_sector_four_collapse()
	
	# Inject an absurdly low/negative delta step (simulating reverse temporal flow or clock glitches)
	var massive_negative_delta: float = -100000.0
	reactor._step_simulation(massive_negative_delta)
	
	# Verify that the boundary protection system successfully restricted both parameters to [0.0, 1.0]
	assert_ge(reactor.t, 0.0, "Assertability must remain within safe bound [0.0] under negative delta")
	assert_le(reactor.t, 1.0, "Assertability must remain within safe bound [1.0] under negative delta")
	assert_ge(reactor.f, 0.0, "Deniability must remain within safe bound [0.0] under negative delta")
	assert_le(reactor.f, 1.0, "Deniability must remain within safe bound [1.0] under negative delta")

# ------------------------------------------------------------------------------
# 4. TRANSITION LOGIC & REAL-TIME SIGNAL VERIFICATION
# ------------------------------------------------------------------------------
func test_sector_four_collapse_trigger_and_anomaly_signal() -> void:
	# Trigger the event
	reactor.trigger_sector_four_collapse()
	
	# Assert that the critical anomaly signal was immediately emitted to alert the combat UI
	assert_signal_emitted(reactor, "critical_anomaly_triggered", "The 'critical_anomaly_triggered' signal was not broadcasted")
	
	# Assert that the system loaded the exact parameters of the Sector Four Collapse Case Study
	assert_eq(reactor.Biology, 0.0, "Sector Four Collapse must reduce Biology to 0.0")
	assert_eq(reactor.Physics, 0.02, "Sector Four Collapse must reduce Physics to 0.02")
	assert_eq(reactor.Emotion, 0.98, "Sector Four Collapse must raise Emotion to 0.98")
	assert_eq(reactor.Magic, 0.95, "Sector Four Collapse must raise Magic to 0.95")
	assert_eq(reactor.Architecture, 0.90, "Sector Four Collapse must raise Architecture to 0.90")
	assert_true(reactor.is_simulation_active, "The simulation loop must be active after a collapse trigger")

func test_asymptotic_convergence_to_harmonic_scar() -> void:
	reactor.trigger_sector_four_collapse()
	
	# Step the simulation forward. At delta = 1.0, the scaled_dt is:
	# delta * time_step_modifier * 50 = 1.0 * 0.02 * 50 = 1.0
	# We saw in the Python simulation that f rises asymptotically toward 0.9469.
	# Let's run multiple smaller steps to simulate smooth progression.
	var steps: int = 15
	var delta_step: float = 0.5 # scaled_dt per step = 50 * 0.5 * 0.02 = 0.5
	
	for i in range(steps):
		reactor._step_simulation(delta_step)
	
	# Quantify the Dialetheism Index (D = min(t, f))
	var D: float = reactor.get_dialetheism_index()
	var U: float = reactor.get_potential_index()
	
	# Assert mathematical alignment with our Python core expectations
	assert_almost_eq(reactor.t, 1.0, 0.0001, "Assertability must remain locked at 1.0 (rescued by emotional resonance)")
	assert_almost_eq(reactor.f, 0.9469, 0.01, "Deniability must reach its mathematical asymptotic limit (~0.9469)")
	assert_almost_eq(D, 0.9469, 0.01, "Dialetheism Index must reflect the paraconsistent superposition")
	assert_almost_eq(U, 0.0, 0.01, "Underdetermination (U) must drop to zero, representing absolute historical certainty")
	
	# Assert that the reactor successfully stabilized into a HARMONIC SCAR
	assert_eq(reactor.current_state, reactor.CalibrationState.HARMONIC_SCAR, "Reactor must stabilize into CalibrationState.HARMONIC_SCAR")
	
	# Assert that all corresponding UI and system signals were broadcasted successfully
	assert_signal_emitted(reactor, "harmonic_scar_stabilized", "The 'harmonic_scar_stabilized' signal must fire when D > 0.90")
	assert_signal_emitted(reactor, "state_changed", "The 'state_changed' telemetry signal was not emitted during steps")
	assert_signal_emitted(reactor, "system_state_updated", "The HUD 'system_state_updated' signal was not emitted")

func test_total_dissolution_state_transition() -> void:
	# Force both Assertability and Deniability near zero (such that U = 1 - max(t, f) > 0.80)
	# This represents absolute environmental emptiness or total structural dissolution
	reactor.t = 0.1
	reactor.f = 0.1
	
	# Force evaluation
	reactor._evaluate_system_state()
	
	# Assert the state has transitioned to TOTAL_DISSOLUTION
	assert_eq(reactor.current_state, reactor.CalibrationState.TOTAL_DISSOLUTION, "System must enter CalibrationState.TOTAL_DISSOLUTION when U > 0.80")
