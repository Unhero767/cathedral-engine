extends Node
# DialetheicBuffer.gd - Handles Paraconsistent Dialogue & State Contradictions

class_name DialetheicBuffer

var active_contradictions: Dictionary = {}

## Ingests two conflicting dialogue statements or state flags
func submit_contradiction(node_id: String, option_a: Dictionary, option_b: Dictionary) -> void:
	print("[DialetheicBuffer] Ingesting contradictory inputs at node: ", node_id)
	
	active_contradictions[node_id] = {
		"state_a": option_a,
		"state_b": option_b,
		"timestamp": Time.get_unix_time_from_system()
	}
	
	# Alert Zoe (Event Bus Mediator) to untangle the cross-node traffic
	SovereignInterface.trigger_dialogue_conflict(node_id, option_a, option_b)

## Resolves a buffered contradiction into a synthesized Harmonic Scar
func resolve_contradiction(node_id: String, synthesized_choice: Dictionary) -> void:
	if active_contradictions.has(node_id):
		print("[DialetheicBuffer] Synthesizing contradiction at [%s]" % node_id)
		
		var log_payload := {
			"node_id": node_id,
			"original_contradiction": active_contradictions[node_id],
			"synthesized_resolution": synthesized_choice
		}
		
		# Commit the synthesized resolution to the Ash Archive via Zeke
		SovereignInterface.request_archive_write(log_payload)
		
		active_contradictions.erase(node_id)
	else:
		push_warning("[DialetheicBuffer] No active contradiction found for node: " + node_id)
