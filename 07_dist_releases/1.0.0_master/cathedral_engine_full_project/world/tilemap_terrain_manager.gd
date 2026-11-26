# TilemapTerrainManager.gd
# 12-Submode Terrain Shader & Dynamic Friction Hook
class_name TilemapTerrainManager extends Node2D

signal terrain_mode_switched(mode_index: int, mode_name: String, friction_val: float)

const SUBMODES: Array[Dictionary] = [
	{"name": "Obsidian Pavement", "friction": 0.1, "shader_idx": 0},
	{"name": "Burnished Gold Floor", "friction": 0.7, "shader_idx": 1},
	{"name": "Static Bronze Dais", "friction": 0.95, "shader_idx": 2},
	{"name": "Liquid Mercury River", "friction": 0.05, "shader_idx": 3},
	{"name": "Matte Teal Grid", "friction": 0.5, "shader_idx": 4},
	{"name": "Ash Bedrock", "friction": 0.8, "shader_idx": 5},
	{"name": "Crystalline Quartz", "friction": 0.3, "shader_idx": 6},
	{"name": "Crimson Entropy Slag", "friction": 0.4, "shader_idx": 7},
	{"name": "Violet Non-Euclidean Glass", "friction": 0.15, "shader_idx": 8},
	{"name": "Emerald Bio-Silicate", "friction": 0.65, "shader_idx": 9},
	{"name": "Kenoma Abyss Edge", "friction": 0.2, "shader_idx": 10},
	{"name": "Harmonic Scar Lattice", "friction": 0.85, "shader_idx": 11}
]

var active_submode: int = 1 # Burnished Gold Floor

func set_submode(mode_idx: int) -> void:
	if mode_idx >= 0 and mode_idx < SUBMODES.size():
		active_submode = mode_idx
		var mode = SUBMODES[active_submode]
		emit_signal("terrain_mode_switched", active_submode, mode["name"], mode["friction"])

func get_current_friction() -> float:
	return SUBMODES[active_submode]["friction"]
