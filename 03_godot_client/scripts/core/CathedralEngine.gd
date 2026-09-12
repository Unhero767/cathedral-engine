extends Node

const Types = CathedralTypes

class StateTransition:
    var sequence: int
    var event_id: String
    var timestamp: float
    var key: String
    var previous: int
    var observed: int
    var resulting: int
    var contradiction: bool
    var causal_reference: String
    var omega_l: float
    var mitigation: int

# --- Immutable Ledger ---
var _ledger: Array[StateTransition] = []
var _states: Dictionary = {} # String -> FourValue

# --- Stress Monitor Config ---
var weights := [0.30, 0.20, 0.25, 0.25] # C, D, R, V
var thresholds := [0.25, 0.45, 0.65, 0.82, 0.95]

func _ready() -> void:
    print("=== CATHEDRAL-ENGINE INITIALIZED IN GODOT ===")

func update_state(key: String, observed: int, causal_reference: String = "", branching_depth: float = 0.0, verification_demand: float = 0.0) -> StateTransition:
    var previous: int = _states.get(key, Types.FourValue.N)
    var resulting: int = Types.join_state(previous, observed)
    
    var contradiction: bool = (resulting == Types.FourValue.B and previous != Types.FourValue.B)
    _states[key] = resulting
    
    # Compute Metrics
    var total_states = _states.size()
    var both_states = 0
    for val in _states.values():
        if val == Types.FourValue.B: both_states += 1
        
    var contradiction_density = (float(both_states) / float(total_states)) if total_states > 0 else 0.0
    var retained_state_volume = clampf(float(total_states) / 1000.0, 0.0, 1.0)
    
    var omega = (
        weights[0] * clampf(contradiction_density, 0.0, 1.0) +
        weights[1] * clampf(branching_depth, 0.0, 1.0) +
        weights[2] * clampf(retained_state_volume, 0.0, 1.0) +
        weights[3] * clampf(verification_demand, 0.0, 1.0)
    )
    
    var mitigation = _evaluate_mitigation(omega)
    
    var event = StateTransition.new()
    event.sequence = _ledger.size() + 1
    event.event_id = "Event_" + str(Time.get_ticks_msec())
    event.timestamp = Time.get_unix_time_from_system()
    event.key = key
    event.previous = previous
    event.observed = observed
    event.resulting = resulting
    event.contradiction = contradiction
    event.causal_reference = causal_reference
    event.omega_l = omega
    event.mitigation = mitigation
    
    _ledger.append(event)
    return event

func _evaluate_mitigation(omega: float) -> int:
    if omega < thresholds[0]: return Types.MitigationLevel.NOMINAL
    if omega < thresholds[1]: return Types.MitigationLevel.OBSERVE
    if omega < thresholds[2]: return Types.MitigationLevel.REDISTRIBUTE
    if omega < thresholds[3]: return Types.MitigationLevel.THROTTLE
    if omega < thresholds[4]: return Types.MitigationLevel.CONTAIN
    return Types.MitigationLevel.SURVIVE

func get_state(key: String) -> int:
    return _states.get(key, Types.FourValue.N)

func get_ledger_snapshot() -> Array[StateTransition]:
    return _ledger.duplicate()
