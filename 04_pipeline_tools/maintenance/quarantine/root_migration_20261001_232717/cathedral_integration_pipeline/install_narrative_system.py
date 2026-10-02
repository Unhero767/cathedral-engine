import os
import json

base_dir = os.path.join(os.getcwd(), "cathedral_integration_pipeline")
godot_dir = os.path.join(base_dir, "godot4_runtime")
os.makedirs(godot_dir, exist_ok=True)

# 1. narrative_manifest.json (NPC Database & Dialogue Trees)
narrative_data = {
    "version": "1.0.0",
    "codex_stratum": "Stratum_01_Foundational",
    "npcs": {
        "Aurelia-9": {
            "title": "Vanguard of the First Hearth",
            "spectral_constant": "Theta",
            "hex_color": "#D4AF37",
            "portrait_tres": "res://cathedral_integration_pipeline/godot4_runtime/aurelia_9_vanguard_spriteframes.tres",
            "recipe_path": "res://cathedral_integration_pipeline/recipes/aurelia_9_vanguard.json"
        },
        "Caelen": {
            "title": "Master Architect of the Lattices",
            "spectral_constant": "Psi",
            "hex_color": "#008080",
            "portrait_tres": "res://cathedral_integration_pipeline/godot4_runtime/caelen_architect_spriteframes.tres",
            "recipe_path": "res://cathedral_integration_pipeline/recipes/caelen_architect.json"
        },
        "Deimos": {
            "title": "Catalyst of Kinetic Remaking",
            "spectral_constant": "Phi",
            "hex_color": "#8B0000",
            "portrait_tres": "res://cathedral_integration_pipeline/godot4_runtime/deimos_catalyst_spriteframes.tres",
            "recipe_path": "res://cathedral_integration_pipeline/recipes/deimos_catalyst.json"
        }
    },
    "conversations": {
        "chamber_01_prologue": {
            "title": "Ignition of the First Hearth",
            "start_node": "node_01",
            "nodes": {
                "node_01": {
                    "speaker": "Aurelia-9",
                    "text": "The Bone Remains. The Hazard is Truth. Welcome to the Reliquary Chamber.",
                    "default_liturgy": "liturgical_idle",
                    "stress_words": {"Bone": 1.0, "Hazard": 1.0, "Truth": 1.0, "Reliquary": 0.8},
                    "next": "node_02"
                },
                "node_02": {
                    "speaker": "Caelen",
                    "text": "The substrate constants are verified. Ego Density stands at 8.30. No drift detected.",
                    "default_liturgy": "ocular_surge",
                    "stress_words": {"verified": 0.8, "Ego": 0.9, "Density": 0.9, "drift": 0.7},
                    "next": "node_03"
                },
                "node_03": {
                    "speaker": "Aurelia-9",
                    "text": "How shall we proceed into the Glitch-Waste perimeter?",
                    "default_liturgy": "liturgical_idle",
                    "choices": [
                        {
                            "text": "Enforce the Plumb Line of absolute Law (Theta Alignment)",
                            "next": "node_law_path",
                            "ash_ledger_event": "Chose Law alignment under Sovereign Theta protocol."
                        },
                        {
                            "text": "Authorize kinetic combustion and remaking (Phi Alignment)",
                            "next": "node_kinetic_path",
                            "ash_ledger_event": "Chose Kinetic Remaking under Deimos protocol."
                        }
                    ]
                },
                "node_law_path": {
                    "speaker": "Aurelia-9",
                    "text": "Then the Vanguard holds the line. Our fluted plate shall not yield.",
                    "default_liturgy": "harmonic_resonance",
                    "stress_words": {"Vanguard": 1.0, "fluted": 0.9, "yield": 0.8},
                    "next": None
                },
                "node_kinetic_path": {
                    "speaker": "Deimos",
                    "text": "Sparks in the slag! Break the stagnant lattice and re-forge the waste!",
                    "default_liturgy": "harmonic_resonance",
                    "stress_words": {"Sparks": 1.0, "slag": 1.0, "lattice": 0.8, "re-forge": 1.0},
                    "next": None
                }
            }
        }
    }
}

with open(os.path.join(base_dir, "narrative_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(narrative_data, f, indent=2)

# 2. DialogueManager.gd (Godot 4 Narrative Engine)
with open(os.path.join(godot_dir, "DialogueManager.gd"), "w", encoding="utf-8") as f:
    f.write('''class_name DialogueManager
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
''')

# 3. DialogueUI.gd (Typewriter & Spectral Interface)
with open(os.path.join(godot_dir, "DialogueUI.gd"), "w", encoding="utf-8") as f:
    f.write('''class_name DialogueUI
extends Control

@export var dialogue_manager: DialogueManager
@export var avatar_portrait: CathedralAvatarPortrait

@onready var speaker_name_label: Label = $DialoguePanel/MarginContainer/VBoxContainer/SpeakerHeader/SpeakerName
@onready var speaker_title_label: Label = $DialoguePanel/MarginContainer/VBoxContainer/SpeakerHeader/SpeakerTitle
@onready var dialogue_text_label: RichTextLabel = $DialoguePanel/MarginContainer/VBoxContainer/DialogueText
@onready var choices_container: VBoxContainer = $DialoguePanel/MarginContainer/VBoxContainer/ChoicesContainer
@onready var continue_prompt: Label = $DialoguePanel/MarginContainer/VBoxContainer/ContinuePrompt

var _current_full_text: String = ""
var _current_stress_map: Dictionary = {}
var _typewriter_index: int = 0
var _is_typing: bool = false
var _has_choices: bool = false
var _typewriter_speed: float = 0.035
var _time_accumulator: float = 0.0

func _ready() -> void:
	if dialogue_manager != null:
		dialogue_manager.speaker_changed.connect(_on_speaker_changed)
		dialogue_manager.line_started.connect(_on_line_started)
		dialogue_manager.choices_presented.connect(_on_choices_presented)
		dialogue_manager.conversation_finished.connect(_on_conversation_finished)
	
	continue_prompt.visible = false
	_clear_choices()

func _process(delta: float) -> void:
	if _is_typing:
		_time_accumulator += delta
		if _time_accumulator >= _typewriter_speed:
			_time_accumulator = 0.0
			_typewriter_step()

func _typewriter_step() -> void:
	_typewriter_index += 1
	if _typewriter_index <= _current_full_text.length():
		dialogue_text_label.text = _current_full_text.substr(0, _typewriter_index)
		var curr_char := _current_full_text[_typewriter_index - 1]
		if curr_char == " " or _typewriter_index == _current_full_text.length():
			_check_and_pulse_recent_word()
	else:
		_finish_typing()

func _check_and_pulse_recent_word() -> void:
	var sub := _current_full_text.substr(0, _typewriter_index).strip_edges()
	var words := sub.split(" ")
	if words.is_empty():
		return
	
	var last_word := words[words.size() - 1].strip_edges().strip_escapes()
	var clean_word := last_word.replace(".", "").replace(",", "").replace("!", "").replace("?", "").replace(":", "")
	
	if avatar_portrait != null:
		var stress: float = 0.40
		if _current_stress_map.has(clean_word):
			stress = float(_current_stress_map[clean_word])
		elif clean_word.length() > 6 or (clean_word.length() > 0 and clean_word[0] == clean_word[0].to_upper()):
			stress = 0.65
		avatar_portrait.pulse_dialogue_stress(stress, true)

func _finish_typing() -> void:
	_is_typing = false
	dialogue_text_label.text = _current_full_text
	if not _has_choices:
		continue_prompt.visible = true
	if avatar_portrait != null:
		avatar_portrait.return_to_idle()

func _on_speaker_changed(speaker: String, title: String, hex_color: String, portrait_tres: String, recipe_path: String) -> void:
	speaker_name_label.text = speaker
	speaker_name_label.add_theme_color_override("font_color", Color.from_string(hex_color, Color.GOLD))
	speaker_title_label.text = "[" + title + "]"
	
	if avatar_portrait != null and not portrait_tres.is_empty() and ResourceLoader.exists(portrait_tres):
		var sf: SpriteFrames = load(portrait_tres)
		if sf != null:
			avatar_portrait.sprite_frames = sf
			avatar_portrait.play(&"liturgical_idle")

func _on_line_started(speaker: String, text: String, stress_words: Dictionary, default_liturgy: StringName) -> void:
	_current_full_text = text
	_current_stress_map = stress_words
	_typewriter_index = 0
	_is_typing = true
	_has_choices = false
	continue_prompt.visible = false
	_clear_choices()
	
	if avatar_portrait != null:
		avatar_portrait.set_liturgical_state(default_liturgy)

func _on_choices_presented(choices: Array) -> void:
	_has_choices = true
	continue_prompt.visible = false
	_clear_choices()
	
	for i in range(choices.size()):
		var choice_data: Dictionary = choices[i]
		var btn := Button.new()
		btn.text = str(i + 1) + ". " + choice_data.get("text", "")
		btn.alignment = HORIZONTAL_ALIGNMENT_LEFT
		btn.pressed.connect(func(): _on_choice_selected(i))
		choices_container.add_child(btn)

func _on_choice_selected(index: int) -> void:
	_clear_choices()
	_has_choices = false
	if dialogue_manager != null:
		dialogue_manager.select_choice(index)

func _clear_choices() -> void:
	for child in choices_container.get_children():
		child.queue_free()

func _on_conversation_finished(title: String) -> void:
	dialogue_text_label.text = "[i]--- End of Recitation: " + title + " ---[/i]"
	continue_prompt.visible = false
	if avatar_portrait != null:
		avatar_portrait.return_to_idle()

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventKey and event.is_pressed() and not event.is_echo():
		if event.keycode == KEY_SPACE or event.keycode == KEY_ENTER:
			if _is_typing:
				_finish_typing()
			elif not _has_choices and dialogue_manager != null:
				dialogue_manager.advance()
		elif _has_choices and event.keycode >= KEY_1 and event.keycode <= KEY_9:
			var idx: int = event.keycode - KEY_1
			if idx < choices_container.get_child_count():
				_on_choice_selected(idx)
''')

# 4. CathedralDialogueScene.tscn (Pre-wired Full Scene)
with open(os.path.join(godot_dir, "CathedralDialogueScene.tscn"), "w", encoding="utf-8") as f:
    f.write("""[gd_scene load_steps=6 format=3 uid="uid://mlaoseas03dialogue001"]

[ext_resource type="Shader" path="res://cathedral_integration_pipeline/godot4_runtime/cathedral_portrait_dither.gdshader" id="1_shader"]
[ext_resource type="SpriteFrames" path="res://cathedral_integration_pipeline/godot4_runtime/aurelia_9_vanguard_spriteframes.tres" id="2_sprite_frames"]
[ext_resource type="Script" path="res://cathedral_integration_pipeline/godot4_runtime/CathedralAvatarPortrait.gd" id="3_portrait_script"]
[ext_resource type="Script" path="res://cathedral_integration_pipeline/godot4_runtime/DialogueManager.gd" id="4_dialogue_mgr"]
[ext_resource type="Script" path="res://cathedral_integration_pipeline/godot4_runtime/DialogueUI.gd" id="5_dialogue_ui"]

[sub_resource type="ShaderMaterial" id="ShaderMaterial_dither"]
shader = ExtResource("1_shader")
shader_parameter/u_shadow_depth_ramp = 0.55
shader_parameter/u_specular_rim_factor = 1.53
shader_parameter/u_lumen_emission_gain = 1.0
shader_parameter/u_afield_potency = 0.95
shader_parameter/u_enable_dither = true
shader_parameter/u_enable_dual_lumen = true

[node name="CathedralDialogueScene" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2

[node name="Background" type="ColorRect" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
grow_horizontal = 2
grow_vertical = 2
color = Color(0.04, 0.04, 0.06, 1)

[node name="PortraitContainer" type="Control" parent="."]
layout_mode = 1
anchors_preset = 8
anchor_left = 0.5
anchor_top = 0.5
anchor_right = 0.5
anchor_bottom = 0.5
offset_left = -64.0
offset_top = -180.0
offset_right = 64.0
offset_bottom = -52.0
grow_horizontal = 2
grow_vertical = 2

[node name="AvatarPortrait" type="AnimatedSprite2D" parent="PortraitContainer"]
material = SubResource("ShaderMaterial_dither")
scale = Vector2(2, 2)
sprite_frames = ExtResource("2_sprite_frames")
animation = &"liturgical_idle"
script = ExtResource("3_portrait_script")
character_recipe_path = "res://cathedral_integration_pipeline/recipes/aurelia_9_vanguard.json"
base_afield_potency = 0.95

[node name="DialogueUI" type="Control" parent="." node_paths=PackedStringArray("dialogue_manager", "avatar_portrait")]
layout_mode = 1
anchors_preset = 12
anchor_top = 1.0
anchor_right = 1.0
anchor_bottom = 1.0
offset_top = -240.0
grow_horizontal = 2
grow_vertical = 0
script = ExtResource("5_dialogue_ui")
dialogue_manager = NodePath("../DialogueManager")
avatar_portrait = NodePath("../PortraitContainer/AvatarPortrait")

[node name="DialoguePanel" type="PanelContainer" parent="DialogueUI"]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
offset_left = 40.0
offset_top = 20.0
offset_right = -40.0
offset_bottom = -20.0
grow_horizontal = 2
grow_vertical = 2

[node name="MarginContainer" type="MarginContainer" parent="DialogueUI/DialoguePanel"]
layout_mode = 2
theme_override_constants/margin_left = 20
theme_override_constants/margin_top = 15
theme_override_constants/margin_right = 20
theme_override_constants/margin_bottom = 15

[node name="VBoxContainer" type="VBoxContainer" parent="DialogueUI/DialoguePanel/MarginContainer"]
layout_mode = 2
theme_override_constants/separation = 8

[node name="SpeakerHeader" type="HBoxContainer" parent="DialogueUI/DialoguePanel/MarginContainer/VBoxContainer"]
layout_mode = 2
theme_override_constants/separation = 12

[node name="SpeakerName" type="Label" parent="DialogueUI/DialoguePanel/MarginContainer/VBoxContainer/SpeakerHeader"]
layout_mode = 2
theme_override_font_sizes/font_size = 20
text = "Aurelia-9"

[node name="SpeakerTitle" type="Label" parent="DialogueUI/DialoguePanel/MarginContainer/VBoxContainer/SpeakerHeader"]
layout_mode = 2
theme_override_colors/font_color = Color(0.7, 0.7, 0.75, 1)
theme_override_font_sizes/font_size = 14
text = "[Vanguard of the First Hearth]"

[node name="DialogueText" type="RichTextLabel" parent="DialogueUI/DialoguePanel/MarginContainer/VBoxContainer"]
layout_mode = 2
size_flags_vertical = 3
theme_override_font_sizes/normal_font_size = 16
bbcode_enabled = true
text = "The Bone Remains. The Hazard is Truth."

[node name="ChoicesContainer" type="VBoxContainer" parent="DialogueUI/DialoguePanel/MarginContainer/VBoxContainer"]
layout_mode = 2
theme_override_constants/separation = 4

[node name="ContinuePrompt" type="Label" parent="DialogueUI/DialoguePanel/MarginContainer/VBoxContainer"]
layout_mode = 2
theme_override_colors/font_color = Color(0.5, 0.5, 0.55, 1)
theme_override_font_sizes/font_size = 12
text = "[ Space / Enter to continue ]"
horizontal_alignment = 2

[node name="DialogueManager" type="Node" parent="."]
script = ExtResource("4_dialogue_mgr")
narrative_manifest_path = "res://cathedral_integration_pipeline/narrative_manifest.json"
""")

# 5. test_narrative_simulation.py (CLI Simulator)
with open(os.path.join(base_dir, "test_narrative_simulation.py"), "w", encoding="utf-8") as f:
    f.write('''import os, json
from dialogue_engine import DialoguePhysicsEngine
from ash_ledger_manager import AshLedgerManager

def run_simulation():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(base_dir, "narrative_manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print("=" * 65)
    print("      MLAOS NARRATIVE & NPC INTERACTIVE DIALOGUE SIMULATOR      ")
    print("=" * 65 + "\\n")

    npcs = manifest.get("npcs", {})
    print(f"--- Registered NPCs in Cathedral Engine ({len(npcs)}) ---")
    for npc_name, data in npcs.items():
        print(f"  * {npc_name:<12} [{data[\x27spectral_constant\x27]}] : {data[\x27title\x27]}")

    conv = manifest["conversations"]["chamber_01_prologue"]
    print(f"\\n--- Running Conversation: \\"{conv[\x27title\x27]}\\" ---")
    
    nodes = conv["nodes"]
    current_node = conv["start_node"]
    diag_engine = DialoguePhysicsEngine()
    ash_mgr = AshLedgerManager(os.path.join(base_dir, "ash_ledger.json"))

    step = 1
    while current_node:
        node_data = nodes[current_node]
        speaker = node_data["speaker"]
        text = node_data["text"]
        liturgy = node_data.get("default_liturgy", "liturgical_idle")
        npc_info = npcs.get(speaker, {})

        print(f"\\n[Turn {step}] Speaker: {speaker} ({npc_info.get(\x27title\x27, \x27\x27)}) [{npc_info.get(\x27spectral_constant\x27, \x27Theta\x27)}]")
        print(f"  Liturgical State: {liturgy}")
        print(f"  Dialogue Line: \\"{text}\\"")

        cadence = diag_engine.calculate_phoneme_stress(text)
        max_stress_word = max(cadence, key=lambda x: x["stress"])
        print(f"  Peak Cadence: \\"{max_stress_word[\x27word\x27]}\\" (Stress: {max_stress_word[\x27stress\x27]}, Lumen Gain: {max_stress_word[\x27lumen_emission_gain\x27]}, Anim: {max_stress_word[\x27liturgical_animation\x27]})")

        if "choices" in node_data and node_data["choices"]:
            print("  Choices Presented:")
            for c_idx, choice in enumerate(node_data["choices"]):
                print(f"    [{c_idx + 1}] {choice[\x27text\x27]}")
            
            selected = node_data["choices"][0]
            print(f"  -> Selecting Choice: [1] {selected[\x27text\x27]}")
            
            entry = ash_mgr.append_historical_scar(
                archetype_id=speaker,
                scar_description=selected["ash_ledger_event"],
                severity=0.75,
                spectral_constant=npc_info.get("spectral_constant", "Theta")
            )
            print(f"  -> [Ash Archive] Committed Event #{entry[\x27index\x27]} [J_hash: {entry[\x27j_hash\x27][:16]}...]")
            current_node = selected["next"]
        else:
            current_node = node_data.get("next")
        step += 1

    print("\\n" + "=" * 65)
    print("          NARRATIVE SIMULATION COMPLETED SUCCESSFULLY           ")
    print("=" * 65)

if __name__ == "__main__":
    run_simulation()
''')

print("NPC and Narrative System installed successfully.")
