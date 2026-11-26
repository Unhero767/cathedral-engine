# TriKeyController.gd
# Tri-Key Sovereign Governance: Lead (Saturn), Cyan (Juno), Iron (Mars)
class_name TriKeyController extends Node

signal key_authorized(key_type: String, authority_token: String)
signal key_state_changed(lead_active: bool, cyan_active: bool, iron_active: bool)
signal triad_concurrence_achieved(signature: String)

enum KeyType {
	LEAD, # Saturn / Duration / Permineralization of Substrate Constants
	CYAN, # Juno / Breadth / Invariance / Multi-Node Sync
	IRON  # Mars / Authority / Kinetic Excision / Volatility
}

var lead_active: bool = false
var cyan_active: bool = false
var iron_active: bool = false

var authority_signatures: Dictionary = {
	"LEAD": "",
	"CYAN": "",
	"IRON": ""
}

# Input handling for quick key toggling
func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("tri_key_lead"):
		toggle_key(KeyType.LEAD)
	elif event.is_action_pressed("tri_key_cyan"):
		toggle_key(KeyType.CYAN)
	elif event.is_action_pressed("tri_key_iron"):
		toggle_key(KeyType.IRON)

func toggle_key(type: KeyType) -> bool:
	match type:
		KeyType.LEAD:
			lead_active = not lead_active
			if lead_active:
				authority_signatures["LEAD"] = _generate_key_signature("SATURN_PERMINERALIZATION")
				emit_signal("key_authorized", "LEAD", authority_signatures["LEAD"])
		KeyType.CYAN:
			cyan_active = not cyan_active
			if cyan_active:
				authority_signatures["CYAN"] = _generate_key_signature("JUNO_INVARIANCE_SYNC")
				emit_signal("key_authorized", "CYAN", authority_signatures["CYAN"])
		KeyType.IRON:
			iron_active = not iron_active
			if iron_active:
				authority_signatures["IRON"] = _generate_key_signature("MARS_KINETIC_EXCISION")
				emit_signal("key_authorized", "IRON", authority_signatures["IRON"])
				
	emit_signal("key_state_changed", lead_active, cyan_active, iron_active)
	
	if is_triad_concurrence():
		var combined_sig = (authority_signatures["LEAD"] + authority_signatures["CYAN"] + authority_signatures["IRON"]).sha256_text()
		emit_signal("triad_concurrence_achieved", combined_sig)
		
	return is_key_active(type)

func is_key_active(type: KeyType) -> bool:
	match type:
		KeyType.LEAD: return lead_active
		KeyType.CYAN: return cyan_active
		KeyType.IRON: return iron_active
	return false

func is_triad_concurrence() -> bool:
	return lead_active and cyan_active and iron_active

func _generate_key_signature(domain: String) -> String:
	var seed_str = domain + ":" + str(Time.get_ticks_usec()) + ":SOVEREIGN_COVENANT"
	return seed_str.sha256_text()
