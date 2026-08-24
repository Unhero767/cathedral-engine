class_name DialogueUI
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
