# DialogueEngine.gd
# AAB Syntactic Dialogue & Cinematic Cutscene Director
class_name DialogueEngine extends Node

signal cutscene_started(cutscene_id: String, title: String)
signal dialogue_line_delivered(speaker: String, text: String, syntax_type: String)
signal cutscene_completed(cutscene_id: String)

const DIALOGUE_TREE_PATH: String = "res://data/dialogue_tree.json"

var cutscenes_data: Dictionary = {}
var current_cutscene: Dictionary = {}
var current_line_index: int = 0
var is_playing: bool = false

func _ready() -> void:
	load_dialogue_trees()

func load_dialogue_trees() -> bool:
	if not FileAccess.file_exists(DIALOGUE_TREE_PATH):
		push_warning("[DialogueEngine] Tree JSON missing: " + DIALOGUE_TREE_PATH)
		return false
		
	var file = FileAccess.open(DIALOGUE_TREE_PATH, FileAccess.READ)
	var content = file.get_as_text()
	file.close()
	
	var json = JSON.new()
	if json.parse(content) == OK:
		cutscenes_data = json.get_data()
		print("[DialogueEngine] Successfully loaded dialogue database.")
		return true
	return false

func play_cutscene(cutscene_id: String) -> bool:
	if cutscenes_data.has(cutscene_id):
		current_cutscene = cutscenes_data[cutscene_id]
		current_line_index = 0
		is_playing = true
		emit_signal("cutscene_started", cutscene_id, current_cutscene.get("title", ""))
		advance_dialogue()
		return true
	return false

func advance_dialogue() -> bool:
	if not is_playing:
		return false
	var lines = current_cutscene.get("lines", [])
	if current_line_index < lines.size():
		var line_data = lines[current_line_index]
		current_line_index += 1
		emit_signal("dialogue_line_delivered", line_data.get("speaker", ""), line_data.get("text", ""), line_data.get("syntax", "AAB"))
		return true
	else:
		is_playing = false
		emit_signal("cutscene_completed", current_cutscene.get("id", ""))
		return false
