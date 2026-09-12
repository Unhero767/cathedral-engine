extends Node
# ChoirGland.gd - Reality Overwrite & Terrain Projection

signal terrain_overwritten(terrain_type: String, spectral_constant: String, breath_cost: float)

const TERRAIN_CATALOG := {
	"Holy_Ground": {"constant": "Gold", "effect": "Stasis_Vitality_Regen", "breath_cost": 25.0},
	"Mud": {"constant": "Blue", "effect": "Viscosity_Frame_Dilation", "breath_cost": 30.0},
	"Fallout_Zone": {"constant": "Red", "effect": "Continuous_Decay_Loop", "breath_cost": 40.0},
	"Glass_Matrix": {"constant": "Teal", "effect": "Refraction_Brittleness", "breath_cost": 35.0}
}

## Projects a terrain overwrite onto local spatial coordinates
func project_terrain(terrain_name: String) -> Dictionary:
	if not TERRAIN_CATALOG.has(terrain_name):
		push_error("[ChoirGland] Unregistered Terrain: " + terrain_name)
		return {}
		
	var terrain_data: Dictionary = TERRAIN_CATALOG[terrain_name]
	
	print("[ChoirGland] Projecting Terrain [%s] | Effect: %s | Constant: %s" % [
		terrain_name, terrain_data["effect"], terrain_data["constant"]
	])
	
	terrain_overwritten.emit(terrain_name, terrain_data["constant"], terrain_data["breath_cost"])
	
	var payload := {
		"type": "Terrain_Overwrite_Projection",
		"terrain": terrain_name,
		"effect": terrain_data["effect"],
		"breath_cost": terrain_data["breath_cost"],
		"spectral_constant": terrain_data["constant"]
	}
	
	SovereignInterface.request_archive_write(payload)
	return payload
