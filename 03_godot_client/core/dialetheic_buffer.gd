class_name DialetheicBuffer
extends Node

enum TruthValue {
	NEITHER = 0, # Empty / Unassigned / Null
	FALSE = 1,   # Pure False
	TRUE = 2,    # Pure True
	BOTH = 3     # Paraconsistent Contradiction (A and not-A)
}

func evaluate_and(a: TruthValue, b: TruthValue) -> TruthValue:
	var table: Array = [
		[TruthValue.NEITHER, TruthValue.FALSE, TruthValue.NEITHER, TruthValue.FALSE],
		[TruthValue.FALSE,   TruthValue.FALSE, TruthValue.FALSE,   TruthValue.FALSE],
		[TruthValue.NEITHER, TruthValue.FALSE, TruthValue.TRUE,    TruthValue.BOTH],
		[TruthValue.FALSE,   TruthValue.FALSE, TruthValue.BOTH,    TruthValue.BOTH]
	]
	return table[a][b]

func evaluate_or(a: TruthValue, b: TruthValue) -> TruthValue:
	var table: Array = [
		[TruthValue.NEITHER, TruthValue.NEITHER, TruthValue.TRUE, TruthValue.TRUE],
		[TruthValue.NEITHER, TruthValue.FALSE,   TruthValue.TRUE, TruthValue.BOTH],
		[TruthValue.TRUE,    TruthValue.TRUE,    TruthValue.TRUE, TruthValue.TRUE],
		[TruthValue.TRUE,    TruthValue.BOTH,    TruthValue.TRUE, TruthValue.BOTH]
	]
	return table[a][b]

func process_proposition(node_id: String, state: TruthValue) -> void:
	if state == TruthValue.BOTH:
		AshArchive.append_log("DIALETHEIC_COLLISION", {"node": node_id, "state": "BOTH"})
