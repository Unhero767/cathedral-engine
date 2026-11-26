# TilemapElevationManager.gd
# 4-Tier Vertical Scaffolding & Height Collision (Tier 0 Basin to Tier 3 High Spires)
class_name TilemapElevationManager extends Node

signal elevation_tier_changed(entity: Node2D, old_tier: int, new_tier: int)

enum ElevationTier {
	TIER_0_BASIN = 0,      # Deep Kenoma floor
	TIER_1_NAVE_FLOOR = 1, # Prime Sanctuary ground
	TIER_2_CLERESTORY = 2, # Elevated choirs & flying buttresses
	TIER_3_SPIRES = 3      # High cathedral vaults & apex oculus
}

var entity_elevations: Dictionary = {} # Node2D -> int

func set_entity_elevation(entity: Node2D, tier: ElevationTier) -> void:
	var old_tier = entity_elevations.get(entity, ElevationTier.TIER_1_NAVE_FLOOR)
	entity_elevations[entity] = tier
	if old_tier != tier:
		emit_signal("elevation_tier_changed", entity, old_tier, tier)

func can_interact_across_tiers(tier_a: ElevationTier, tier_b: ElevationTier) -> bool:
	return abs(int(tier_a) - int(tier_b)) <= 1
