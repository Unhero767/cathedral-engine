class_name MetamorphicSqueeze
extends Node

signal scar_formed(location: Vector2, scar_data: Dictionary)

func compress_paradox(location: Vector2, contradiction_data: Dictionary) -> Dictionary:
	var scar_id: String = AshArchive.append_log("METAMORPHIC_SQUEEZE", {
		"location": location,
		"data": contradiction_data
	})
	
	var scar: Dictionary = {
		"id": scar_id,
		"location": location,
		"structural_rigidity": 1.0,
		"obsidian_dermis": true
	}
	
	emit_signal("scar_formed", location, scar)
	return scar
