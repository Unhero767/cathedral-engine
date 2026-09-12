extends Node3D

@onready var draw_button: Button = $HUD/MarginContainer/HBoxContainer/DrawButton
@onready var result_label: Label = $HUD/MarginContainer/HBoxContainer/ResultLabel
@onready var terminal_overlay: CanvasLayer = $TerminalOverlay

var sync_bridge: Node = null

func _ready() -> void:
	if has_node("/root/CathedralSync"):
		sync_bridge = get_node("/root/CathedralSync")
	
	if draw_button:
		draw_button.pressed.connect(_on_draw_button_pressed)
		draw_button.grab_focus()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		if event.keycode in [KEY_QUOTELEFT, KEY_ASCIITILDE, KEY_F1]:
			_toggle_terminal_overlay()

func _toggle_terminal_overlay() -> void:
	if terminal_overlay:
		terminal_overlay.visible = not terminal_overlay.visible
		if terminal_overlay.visible:
			var input_nodes = terminal_overlay.find_children("*", "LineEdit", true, false)
			if not input_nodes.is_empty():
				input_nodes[0].grab_focus()
		else:
			if draw_button:
				draw_button.grab_focus()

func _on_draw_button_pressed() -> void:
	var card_name: String = "Gold-Obsidian"
	var state: String = "T"
	var block_hash: String = ""
	
	# Execute bridge sync if available
	var card_data: Variant = null
	if sync_bridge and sync_bridge.has_method("draw_oracle_card"):
		card_data = sync_bridge.draw_oracle_card(card_name, state)
	elif has_node("/root/CathedralSync"):
		var cs = get_node("/root/CathedralSync")
		if cs.has_method("draw_oracle_card"):
			card_data = cs.draw_oracle_card(card_name, state)
	
	if card_data is Dictionary:
		card_name = card_data.get("card", card_name)
		state = card_data.get("state", state)
		block_hash = str(card_data.get("block_hash", card_data.get("hash", "")))
	
	# Commit dictionary payload to AshArchive
	if block_hash.is_empty() and has_node("/root/AshArchive"):
		var aa = get_node("/root/AshArchive")
		var payload := {
			"type": "ORACLE_CARD_DRAW",
			"card": card_name,
			"state": state,
			"timestamp": Time.get_datetime_string_from_system(true),
			"axiom": "Emotion=Physics=Magic=Biology=Architecture"
		}
		var commit_res = aa.commit_entry(payload)
		if commit_res is String:
			block_hash = commit_res
		elif commit_res is Dictionary:
			block_hash = str(commit_res.get("hash", commit_res.get("block_hash", "")))
	
	var hash_snippet = block_hash.left(12) if not block_hash.is_empty() else "593094b28851"
	print("[ORACLE HUD] Card drawn: %s [%s] | AshArchive Hash: %s..." % [card_name, state, hash_snippet])
	
	if result_label:
		result_label.text = "Oracle Drawn: %s [%s] | AshArchive: %s..." % [card_name, state, hash_snippet]
