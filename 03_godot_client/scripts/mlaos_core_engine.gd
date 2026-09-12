# ==============================================================================
# SCRIPT: mlaos_core_engine.gd
# SUBSYSTEM: Functional Mechanics Architecture / Vertical Slice Minimum Core
# SYSTEM: MLAOS-Prime RPG (The Cathedral-Engine)
# ==============================================================================
class_name MLAOSCoreEngine
extends Node

# --- ENUMERATIONS ---
enum BelnapState { TRUE, FALSE, BOTH, NONE }
enum SpectralDomain { BLUE, RED, GOLD, GREEN, VIOLET, WHITE, BLACK }

# --- DATA STRUCTURES ---
class StateNode:
	var id: String
	var state: BelnapState
	var age: float
	var metadata: Dictionary

	func _init(p_id: String, p_state: BelnapState, p_meta: Dictionary = {}) -> void:
		id = p_id
		state = p_state
		age = 0.0
		metadata = p_meta


class WorldEvent:
	var event_id: String
	var timestamp: int
	var actor: String
	var action: String
	var resulting_state: String
	var provenance: Dictionary

	func _init(p_id: String, p_actor: String, p_action: String, p_result: String, p_prov: Dictionary) -> void:
		event_id = p_id
		timestamp = Time.get_unix_time_from_system()
		actor = p_actor
		action = p_action
		resulting_state = p_result
		provenance = p_prov


# --- ENGINE STATE SUBSYSTEM ---
static var instance: MLAOSCoreEngine

var _state_buffer: Dictionary = {}
var _ash_archive_ledger: Array[WorldEvent] = []
var player_spectral_vector: Dictionary = {
	SpectralDomain.BLUE: 0.7,
	SpectralDomain.RED: 0.2,
	SpectralDomain.BLACK: 0.8
}


func _ready() -> void:
	instance = self
	print("[MLAOS-Engine] Sovereign Interface online. Initializing Ashen Basilica Vertical Slice...")
	_run_vertical_slice_simulation()


# --- PARACONSISTENT LOGIC & PROPOSITIONS ---
func evaluate_proposition(prop_id: String, incoming_evidence: BelnapState) -> BelnapState:
	if not _state_buffer.has(prop_id):
		_state_buffer[prop_id] = StateNode.new(prop_id, incoming_evidence)
		return incoming_evidence

	var node: StateNode = _state_buffer[prop_id]
	var current_state = node.state

	# Belnap-Dunn Paraconsistent State Matrix Resolution
	if current_state == BelnapState.NONE:
		node.state = incoming_evidence
	elif current_state != incoming_evidence and incoming_evidence != BelnapState.NONE:
		# Contradictory evidence detected -> Crystallize into BOTH (Harmonic Scar)
		node.state = BelnapState.BOTH
		print("[Dialetheic Engine] Conflict registered for [%s]. Crystallized into BOTH." % prop_id)
	
	return node.state


# --- PERSISTENT WORLD INSCRIPTION (ASH ARCHIVE) ---
func commit_world_event(actor: String, action: String, result: String, provenance_meta: Dictionary) -> void:
	var event_id = "EVT_%d" % (_ash_archive_ledger.size() + 1)
	var world_event = WorldEvent.new(event_id, actor, action, result, provenance_meta)
	_ash_archive_ledger.append(world_event)
	print("[Ash Archive] Inscribed Event %s: Actor [%s] performed [%s] -> Result: [%s]" % [event_id, actor, action, result])


# --- SPECTRAL COMBAT & INTERACTION MODIFIER ---
func calculate_effective_damage(base_damage: float, attacker_spectrum: SpectralDomain, target_state: BelnapState) -> float:
	var spectrum_multiplier = player_spectral_vector.get(attacker_spectrum, 1.0)
	var state_multiplier = 1.0
	
	if target_state == BelnapState.BOTH:
		state_multiplier = 1.5 # Dialetheic vulnerability
	elif target_state == BelnapState.FALSE:
		state_multiplier = 0.5 # Suppressed target resistance

	return base_damage * spectrum_multiplier * state_multiplier


# --- VERTICAL SLICE PROTOTYPE EXECUTION ---
func _run_vertical_slice_simulation() -> void:
	print("\n--- BEGINNING VERTICAL SLICE: ASHEN BASILICA NAVE ---")

	# 1. Proposition Initialization (The Cathedral Collapse)
	var prop_key = "prop_cathedral_collapse_cause"
	print("Initial State Evaluation:")
	
	# Knight Evidence (False / Denies)
	var state_1 = evaluate_proposition(prop_key, BelnapState.FALSE)
	print(" -> Knight testimony ingested. State: FALSE")

	# Archivist Evidence (True / Supports) -> Causes Dialetheic Collision (BOTH)
	var state_2 = evaluate_proposition(prop_key, BelnapState.TRUE)
	print(" -> Archivist archive ingested. State: %s (Harmonic Scar Formed)" % BelnapState.keys()[state_2])

	# 2. Gameplay Consequence (Content Availability unlocked by BOTH state)
	if state_2 == BelnapState.BOTH:
		print("[Gameplay Event] Logical State == BOTH. Invisible staircase materialized in Ashen Basilica.")

	# 3. Persistent World Inscription (Player Action & Environmental Scar)
	commit_world_event(
		"Meridian Walker",
		"Descent via Structural Witness Arena",
		"Boss Defeated / Architectural Scar Inscribed",
		{"location": "Ashen Basilica Nave", "elevation": -1}
	)

	print("--- VERTICAL SLICE SIMULATION COMPLETE ---\n")
