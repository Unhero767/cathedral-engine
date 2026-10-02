extends Node
# TriKeySovereignty.gd - Tri-Key Sovereignty & Executive Authority

signal key_executed(key_type: String, effect: String)

enum KeyType { LEAD, CYAN, IRON }

const KEY_PROPERTIES := {
	KeyType.LEAD: {
		"name": "Lead_Key",
		"right": "Duration",
		"effect": "Permineralize_Moment_Against_Decay",
		"constant": "Gold"
	},
	KeyType.CYAN: {
		"name": "Cyan_Key",
		"right": "Breadth",
		"effect": "Enforce_Network_Invariance",
		"constant": "Teal"
	},
	KeyType.IRON: {
		"name": "Iron_Key",
		"right": "Authority",
		"effect": "Kinetic_Scalpel_Excision",
		"constant": "Red"
	}
}

## Executes a Tri-Key executive decree
func execute_key(key_type: KeyType) -> Dictionary:
	if not KEY_PROPERTIES.has(key_type):
		push_error("[TriKeySovereignty] Invalid KeyType: " + str(key_type))
		return {}
		
	var key_info: Dictionary = KEY_PROPERTIES[key_type]
	print("[TriKeySovereignty] Executing %s (Right of %s) | Effect: %s" % [
		key_info["name"], key_info["right"], key_info["effect"]
	])
	
	key_executed.emit(key_info["name"], key_info["effect"])
	
	var payload := {
		"type": "TriKey_Executive_Decree",
		"key_name": key_info["name"],
		"right": key_info["right"],
		"effect": key_info["effect"],
		"spectral_constant": key_info["constant"]
	}
	
	SovereignInterface.request_archive_write(payload)
	return payload
