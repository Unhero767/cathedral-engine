class_name AltarInteractable
extends Area2D

signal altar_resonance_toggled(is_resonating: bool)

@export var pulse_frequency: float = 1.5 # 1.5 Hz = 90 BPM
@export var base_energy: float = 1.0
@export var pulse_amplitude: float = 0.8
@export var resonance_boost: float = 2.0

@onready var light: PointLight2D = $PointLight2D
@onready var prompt_label: Label = $PromptLabel
@onready var sprite: Sprite2D = $Sprite2D

var elapsed_time: float = 0.0
var player_in_range: Node2D = null
var is_resonating: bool = false

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)
	prompt_label.visible = false
	
	if sprite and sprite.texture == null:
		var raw_path := "res://assets/textures/altar_stone.png"
		if FileAccess.file_exists(raw_path):
			var img := Image.load_from_file(raw_path)
			sprite.texture = ImageTexture.create_from_image(img)

func _process(delta: float) -> void:
	elapsed_time += delta
	var sine_val := 0.5 + 0.5 * sin(2.0 * PI * pulse_frequency * elapsed_time)
	var current_amplitude := pulse_amplitude * (resonance_boost if is_resonating else 1.0)
	var target_energy := base_energy + (sine_val * current_amplitude)
	
	if light:
		light.energy = target_energy
		light.texture_scale = 1.6 + (0.35 * sine_val)

func _unhandled_input(event: InputEvent) -> void:
	if player_in_range and event.is_action_pressed("interact"):
		_toggle_altar()
		get_viewport().set_input_as_handled()

func _toggle_altar() -> void:
	is_resonating = !is_resonating
	altar_resonance_toggled.emit(is_resonating)
	if player_in_range and player_in_range.has_method("trigger_altar_resonance"):
		player_in_range.trigger_altar_resonance(is_resonating)
	prompt_label.text = "[RESONATING]" if is_resonating else "[E / A: COMMUNE]"

func _on_body_entered(body: Node2D) -> void:
	if body.is_in_group(&"player") or body.has_method("trigger_altar_resonance"):
		player_in_range = body
		prompt_label.text = "[RESONATING]" if is_resonating else "[E / A: COMMUNE]"
		prompt_label.visible = true

func _on_body_exited(body: Node2D) -> void:
	if body == player_in_range:
		if is_resonating:
			_toggle_altar()
		player_in_range = null
		prompt_label.visible = false
