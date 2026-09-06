class_name ChoirGland
extends Node

signal terrain_overwritten(terrain_type: String, bounds: Rect2)

enum TerrainType {
	HOLY_GROUND,
	MUD,
	FALLOUT_ZONE,
	GLASS_MATRIX
}

func project_terrain(terrain: TerrainType, target_bounds: Rect2, cost: float) -> bool:
	var lung: VoidLung = get_parent().get_node_or_null("VoidLung")
	if lung and lung.breath_pool >= cost:
		lung.breath_pool -= cost
		emit_signal("terrain_overwritten", TerrainType.keys()[terrain], target_bounds)
		AshArchive.append_log("TERRAIN_OVERWRITE", {
			"terrain": TerrainType.keys()[terrain],
			"bounds": target_bounds
		})
		return true
	return false
