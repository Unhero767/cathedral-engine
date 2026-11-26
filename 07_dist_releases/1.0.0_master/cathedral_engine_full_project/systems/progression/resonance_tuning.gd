# ResonanceTuning.gd
# 63-Day, 10-Phase Metamorphic Progression Pipeline
class_name ResonanceTuning extends Node

signal phase_advanced(new_phase: int, phase_name: String)
signal day_advanced(current_day: int, total_days: int)
signal ontological_density_increased(new_density: float)

const TOTAL_DAYS: int = 63
const TOTAL_PHASES: int = 10

const PHASES_INFO: Array[Dictionary] = [
	{"phase": 1, "name": "Substrate Awakening", "day_start": 1, "day_end": 6},
	{"phase": 2, "name": "Lattice Weaving", "day_start": 7, "day_end": 12},
	{"phase": 3, "name": "Merkle Carbonization", "day_start": 13, "day_end": 18},
	{"phase": 4, "name": "Mortar Domain Validation", "day_start": 19, "day_end": 24},
	{"phase": 5, "name": "Panopticon Echolocation", "day_start": 25, "day_end": 30},
	{"phase": 6, "name": "Recursive Lemma Synchronization", "day_start": 31, "day_end": 37},
	{"phase": 7, "name": "Kinetic Deimos Remaking", "day_start": 38, "day_end": 44},
	{"phase": 8, "name": "Dialetheic Collision Navigation", "day_start": 45, "day_end": 51},
	{"phase": 9, "name": "Ideality Phase Trimming", "day_start": 52, "day_end": 57},
	{"phase": 10, "name": "Lithic Stabilization & Sovereign Genesis", "day_start": 58, "day_end": 63}
]

var current_day: int = 1
var current_phase_index: int = 0
var ontological_density: float = 8.3 # rho_onto

func advance_day() -> void:
	if current_day < TOTAL_DAYS:
		current_day += 1
		ontological_density += 0.12
		emit_signal("day_advanced", current_day, TOTAL_DAYS)
		emit_signal("ontological_density_increased", ontological_density)
		_check_phase_advancement()

func _check_phase_advancement() -> void:
	for i in range(PHASES_INFO.size()):
		var p = PHASES_INFO[i]
		if current_day >= p["day_start"] and current_day <= p["day_end"]:
			if current_phase_index != i:
				current_phase_index = i
				emit_signal("phase_advanced", p["phase"], p["name"])
			break

func get_current_phase() -> Dictionary:
	return PHASES_INFO[current_phase_index]
