class_name DialogueManager
extends Node

## Manages narrative tree parsing, speaker swapping, choice resolution,
## and Ash Archive ledger event dispatching for the Cathedral Engine.

signal speaker_changed(speaker_name: String, title: String, hex_color: String, portrait_tres: String, recipe_path: String)
signal line_started(speaker_name: String, text: String, stress_words: Dictionary, default_liturgy: StringName)
signal choices_presented(choices: Array)
signal conversation_finished(conversation_id: String)
signal ash_ledger_event_triggered(event_description: String)

@export var narrative_manifest_path: String = "res://cathedral_integration_pipeline/narrative_manifest.json"
@export var auto_start_conversation: String = "chamber_01_prologue"

var _manifest: Dictionary = {}
var _current_conversation: Dictionary = {}
var _current_node_id: String = ""
var _is_active: bool = false

func _ready() -> void:
	load_narrative_manifest(narrative_manifest_path)
	if not auto_start_conversation.is_empty():
		call_deferred("start_conversation", auto_start_conversation)

func load_narrative_manifest(path: String) -> void:
	if not FileAccess.file_exists(path):
		push_warning("[DialogueManager] Manifest file not found: " + path)
		return
	
	var file := FileAccess.open(path, FileAccess.READ)
	var json_text := file.get_as_text()
	var json := JSON.new()
	var err := json.parse(json_text)
	if err == OK and json.data is Dictionary:
		_manifest = json.data
		print("[DialogueManager] Loaded narrative manifest successfully.")
	else:
		push_error("[DialogueManager] Failed to parse manifest JSON: " + str(err))

func start_conversation(conv_id: String) -> void:
	var convs: Dictionary = _manifest.get("conversations", {})
	if not convs.has(conv_id):
		push_error("[DialogueManager] Conversation not found: " + conv_id)
		return
	
	_current_conversation = convs[conv_id]
	_current_node_id = _current_conversation.get("start_node", "")
	_is_active = true
	print("[DialogueManager] Starting conversation: ", conv_id)
	_display_current_node()

func advance() -> void:
	if not _is_active or _current_node_id.is_empty():
		return
	
	var nodes: Dictionary = _current_conversation.get("nodes", {})
	var curr_node: Dictionary = nodes.get(_current_node_id, {})
	
	if curr_node.has("choices") and not curr_node["choices"].is_empty():
		return
	
	var next_node = curr_node.get("next", null)
	if next_node == null or str(next_node).is_empty():
		_end_conversation()
	else:
		_current_node_id = str(next_node)
		_display_current_node()

func select_choice(choice_index: int) -> void:
	var nodes: Dictionary = _current_conversation.get("nodes", {})
	var curr_node: Dictionary = nodes.get(_current_node_id, {})
	var choices: Array = curr_node.get("choices", [])
	
	if choice_index >= 0 and choice_index < choices.size():
		var chosen: Dictionary = choices[choice_index]
		var ash_event: String = chosen.get("ash_ledger_event", "")
		if not ash_event.is_empty():
			print("[Ash Archive] Dialogue choice committed: ", ash_event)
			ash_ledger_event_triggered.emit(ash_event)
		
		var next_node = chosen.get("next", null)
		if next_node == null or str(next_node).is_empty():
			_end_conversation()
		else:
			_current_node_id = str(next_node)
			_display_current_node()

func _display_current_node() -> void:
	var nodes: Dictionary = _current_conversation.get("nodes", {})
	if not nodes.has(_current_node_id):
		_end_conversation()
		return
	
	var node_data: Dictionary = nodes[_current_node_id]
	var speaker: String = node_data.get("speaker", "Unknown")
	var text: String = node_data.get("text", "")
	var stress_words: Dictionary = node_data.get("stress_words", {})
	var default_liturgy: StringName = StringName(node_data.get("default_liturgy", "liturgical_idle"))
	
	var npcs: Dictionary = _manifest.get("npcs", {})
	if npcs.has(speaker):
		var npc_info: Dictionary = npcs[speaker]
		speaker_changed.emit(
			speaker,
			npc_info.get("title", ""),
			npc_info.get("hex_color", "#D4AF37"),
			npc_info.get("portrait_tres", ""),
			npc_info.get("recipe_path", "")
		)
	
	line_started.emit(speaker, text, stress_words, default_liturgy)
	
	if node_data.has("choices") and not node_data["choices"].is_empty():
		choices_presented.emit(node_data["choices"])

func _end_conversation() -> void:
	_is_active = false
	var title: String = _current_conversation.get("title", "")
	print("[DialogueManager] Conversation finished: ", title)
	conversation_finished.emit(title)
