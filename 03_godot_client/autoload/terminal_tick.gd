extends Node
# Axiom: The Bone Remains. Terminal Tick v7.4-TERMINUS schema.
# Residue decays asymptotically at δ=0.001.

const ASYMPTOTIC_DECAY: float = 0.001
var _terminal_tick: int = 0 # Hidden from agents
var ledger: Array[Dictionary] = []

func log_command(command: String, output: String, hazard_level: int = 0):
	_terminal_tick += 1
	var entry = {
		"tick": _terminal_tick,
		"timestamp": Time.get_unix_time_from_system(),
		"command": command,
		"output": output,
		"hazard": hazard_level, # The Hazard is Truth
		"residue": 1.0
	}
	ledger.append(entry)
	_decay_residue()

func _decay_residue():
	# Asymptotic decay of older records (memory management + narrative flavor)
	for i in range(ledger.size()):
		if ledger[i].residue > ASYMPTOTIC_DECAY:
			ledger[i].residue -= ASYMPTOTIC_DECAY
		else:
			ledger[i].residue = ASYMPTOTIC_DECAY

# Optional: Helper to retrieve ledger state for debugging or UI display
func get_ledger_summary() -> String:
	var summary = "TERMINAL TICK: %d\n---\n" % _terminal_tick
	for entry in ledger:
		if entry.residue > 0.01: # Only show records that haven't fully decayed
			summary += "[Tick %d] > %s (Residue: %.3f)\n" % [entry.tick, entry.command, entry.residue]
	return summary
