extends Node
# ArcanaEngine.gd - Operates the Living Tarot & Executable Geometry

class_name ArcanaEngine

# Mapping of Major Arcana Cards to Spectral Constants & Frequencies
const ARCANA_REGISTRY := {
	"I_THE_FIRST_CANTOR": {"constant": "Gold", "frequency_hz": 43.7, "topology": "Radial_Sun_Vault"},
	"V_THE_HARMONIC_SPHERE": {"constant": "Violet", "frequency_hz": 108.0, "topology": "Invisible_Sea"},
	"XXIV_SCALES_OF_MEMORY": {"constant": "Blue", "frequency_hz": 28.0, "topology": "Echo_Vault"},
	"XXXII_FOSSILIZED_PARADOX": {"constant": "Null", "frequency_hz": 1.5, "topology": "Obsidian_Dermis"}
}

## Draws and executes an Arcana Card, exerting narrative pressure on local space
func draw_card(card_id: String) -> Dictionary:
	if not ARCANA_REGISTRY.has(card_id):
		push_error("[ArcanaEngine] Unregistered Arcana Card: " + card_id)
		return {}
		
	var card_data: Dictionary = ARCANA_REGISTRY[card_id]
	print("[ArcanaEngine] Executing Arcana Card [%s] | Frequency: %.1f Hz | Constant: %s" % [card_id, card_data["frequency_hz"], card_data["constant"]])
	
	var execution_payload := {
		"card": card_id,
		"data": card_data,
		"executed_at": Time.get_unix_time_from_system()
	}
	
	# Request Zeke to record the Arcana execution into the Ash Archive
	SovereignInterface.request_archive_write(execution_payload)
	return card_data
