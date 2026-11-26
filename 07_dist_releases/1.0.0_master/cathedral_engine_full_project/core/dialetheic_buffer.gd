# DialetheicBuffer.gd
# Belnap-Dunn 4-Valued Logic Matrix (B4): Neither (0), False (1), True (2), Both (3)
# Manages non-classical paraconsistent collisions, contradiction detection, and Metamorphic Squeeze
class_name DialetheicBuffer extends Node

signal contradiction_detected(source_a: String, source_b: String, context: String)
signal metamorphic_squeeze_triggered(scar_intensity: float, location: Vector2)
signal logic_state_changed(previous_state: int, new_state: int)

enum B4Value {
	NEITHER = 0, # Empty / N / Kenoma
	FALSE = 1,   # F / Refuted
	TRUE = 2,    # T / Verified
	BOTH = 3     # B / Dialetheia / Contradiction (A and not A)
}

# Current system-wide dialetheic state
var current_state: B4Value = B4Value.TRUE
var contradiction_count: int = 0
var active_harmonic_scars: Array = []

# Truth ordering: False <= (Neither, Both) <= True
# Information ordering: Neither <= (False, True) <= Both

# Belnap-Dunn Negation (~t)
# ~N = N, ~F = T, ~T = F, ~B = B
func b4_not(val: B4Value) -> B4Value:
	match val:
		B4Value.NEITHER:
			return B4Value.NEITHER
		B4Value.FALSE:
			return B4Value.TRUE
		B4Value.TRUE:
			return B4Value.FALSE
		B4Value.BOTH:
			return B4Value.BOTH
	return B4Value.NEITHER

# Belnap-Dunn Conflation (-k)
# -N = B, -F = F, -T = T, -B = N
func b4_conflation(val: B4Value) -> B4Value:
	match val:
		B4Value.NEITHER:
			return B4Value.BOTH
		B4Value.FALSE:
			return B4Value.FALSE
		B4Value.TRUE:
			return B4Value.TRUE
		B4Value.BOTH:
			return B4Value.NEITHER
	return B4Value.NEITHER

# Belnap-Dunn Conjunction / AND (meet in truth lattice)
# Truth table for AND:
#     N  F  T  B
#  N  N  F  N  F
#  F  F  F  F  F
#  T  N  F  T  B
#  B  F  F  B  B
func b4_and(a: B4Value, b: B4Value) -> B4Value:
	if a == B4Value.FALSE or b == B4Value.FALSE:
		return B4Value.FALSE
	if a == B4Value.BOTH and b == B4Value.BOTH:
		return B4Value.BOTH
	if a == B4Value.TRUE:
		return b
	if b == B4Value.TRUE:
		return a
	# Neither & Both = False
	if (a == B4Value.NEITHER and b == B4Value.BOTH) or (a == B4Value.BOTH and b == B4Value.NEITHER):
		return B4Value.FALSE
	return B4Value.NEITHER

# Belnap-Dunn Disjunction / OR (join in truth lattice)
# Truth table for OR:
#     N  F  T  B
#  N  N  N  T  T
#  F  N  F  T  B
#  T  T  T  T  T
#  B  T  B  T  B
func b4_or(a: B4Value, b: B4Value) -> B4Value:
	if a == B4Value.TRUE or b == B4Value.TRUE:
		return B4Value.TRUE
	if a == B4Value.FALSE:
		return b
	if b == B4Value.FALSE:
		return a
	if a == B4Value.BOTH and b == B4Value.BOTH:
		return B4Value.BOTH
	if (a == B4Value.NEITHER and b == B4Value.BOTH) or (a == B4Value.BOTH and b == B4Value.NEITHER):
		return B4Value.TRUE
	return B4Value.NEITHER

# Information Join / Gullibility (join in information lattice: combines all evidence)
# N join X = X, F join T = B, B join X = B
func b4_info_join(a: B4Value, b: B4Value) -> B4Value:
	if a == B4Value.BOTH or b == B4Value.BOTH:
		return B4Value.BOTH
	if a == B4Value.NEITHER:
		return b
	if b == B4Value.NEITHER:
		return a
	if a == b:
		return a
	# One is TRUE and other is FALSE => BOTH (Collision!)
	return B4Value.BOTH

# Information Meet / Consensus (meet in information lattice: shared evidence)
func b4_info_meet(a: B4Value, b: B4Value) -> B4Value:
	if a == B4Value.NEITHER or b == B4Value.NEITHER:
		return B4Value.NEITHER
	if a == B4Value.BOTH:
		return b
	if b == B4Value.BOTH:
		return a
	if a == b:
		return a
	return B4Value.NEITHER

# Ingest and resolve opposing statements / truth inputs
func ingest_statement(assertion_a: bool, assertion_b: bool, source_a: String = "Caelen", source_b: String = "Deimos", world_pos: Vector2 = Vector2.ZERO) -> B4Value:
	var val_a: B4Value = B4Value.TRUE if assertion_a else B4Value.FALSE
	var val_b: B4Value = B4Value.TRUE if assertion_b else B4Value.FALSE
	
	var resolved: B4Value = b4_info_join(val_a, val_b)
	var prev: B4Value = current_state
	current_state = resolved
	
	if resolved == B4Value.BOTH:
		contradiction_count += 1
		emit_signal("contradiction_detected", source_a, source_b, "Paraconsistent Dialetheia Encountered")
		trigger_metamorphic_squeeze(1.0, world_pos)
		
	if prev != current_state:
		emit_signal("logic_state_changed", prev, current_state)
		
	return resolved

# Resolves contradiction into a load-bearing Harmonic Scar (TRIZ Ideality Trimming)
func trigger_metamorphic_squeeze(intensity: float, world_pos: Vector2) -> Dictionary:
	var scar = {
		"id": "scar_" + str(active_harmonic_scars.size() + 1),
		"position": world_pos,
		"intensity": intensity,
		"load_bearing_capacity": 1.618 * intensity,
		"obsidian_core": true,
		"gold_boundary": true,
		"cost_reduction": 0.3 # TRIZ optimization drops cost from 0.6 to 0.3
	}
	active_harmonic_scars.append(scar)
	emit_signal("metamorphic_squeeze_triggered", intensity, world_pos)
	return scar

func get_state_string(val: B4Value = current_state) -> String:
	match val:
		B4Value.NEITHER:
			return "NEITHER (Empty Kenoma)"
		B4Value.FALSE:
			return "FALSE (Refuted)"
		B4Value.TRUE:
			return "TRUE (Axiomatic)"
		B4Value.BOTH:
			return "BOTH (Dialetheic Scar)"
	return "UNKNOWN"
