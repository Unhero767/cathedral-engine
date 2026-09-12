class_name CathedralAvatarPortrait
extends Control

const AtlasBuilder = preload("res://03_godot_client/scripts/core/CathedralAtlasBuilder.gd")

signal liturgical_state_changed(previous_state: StringName, new_state: StringName)
signal dialogue_cadence_pulsed(gain_value: float)
signal overlay_injected(layer_id: int, overlay_texture: Texture2D)

@export var recipe_path: String = ""
@export var master_texture: Texture2D
@export var portrait_shader: Shader

var animated_sprite: AnimatedSprite2D
var overlay_sprite: Sprite2D

var character_recipe: Dictionary = {}
var current_liturgical_state: StringName = &"liturgical_idle"
var base_afield_potency: float = 0.87
var current_lumen_gain: float = 1.0

func _ready() -> void:
	_initialize_node_hierarchy()
	if not recipe_path.is_empty():
		load_character_recipe(recipe_path)
	elif master_texture != null:
		setup_from_texture(master_texture)

func _initialize_node_hierarchy() -> void:
	if not has_node("AnimatedSprite2D"):
		animated_sprite = AnimatedSprite2D.new()
		animated_sprite.name = "AnimatedSprite2D"
		animated_sprite.centered = false
		add_child(animated_sprite)
	else:
		animated_sprite = get_node("AnimatedSprite2D") as AnimatedSprite2D

	if not has_node("OverlaySprite2D"):
		overlay_sprite = Sprite2D.new()
		overlay_sprite.name = "OverlaySprite2D"
		overlay_sprite.centered = false
		overlay_sprite.z_index = 11
		add_child(overlay_sprite)
	else:
		overlay_sprite = get_node("OverlaySprite2D") as Sprite2D

func load_character_recipe(path: String) -> bool:
	if not FileAccess.file_exists(path):
		return false
	var file := FileAccess.open(path, FileAccess.READ)
	var json := JSON.new()
	if json.parse(file.get_as_text()) != OK:
		return false
	character_recipe = json.data as Dictionary
	_apply_recipe(character_recipe)
	return true

static func load_texture_safe(path: String) -> Texture2D:
	if ResourceLoader.exists(path):
		var res = load(path)
		if res is Texture2D:
			return res as Texture2D
	var global_path := ProjectSettings.globalize_path(path)
	if FileAccess.file_exists(global_path):
		var img := Image.load_from_file(global_path)
		if img:
			return ImageTexture.create_from_image(img)
	return null

func setup_from_texture(texture: Texture2D) -> void:
	master_texture = texture
	if not animated_sprite:
		_initialize_node_hierarchy()
	animated_sprite.sprite_frames = AtlasBuilder.build_sprite_frames(master_texture)
	if portrait_shader:
		var mat := ShaderMaterial.new()
		mat.shader = portrait_shader
		mat.set_shader_parameter("u_afield_potency", base_afield_potency)
		mat.set_shader_parameter("u_lumen_emission_gain", current_lumen_gain)
		mat.set_shader_parameter("u_shadow_depth_ramp", 0.65)
		mat.set_shader_parameter("u_specular_rim_factor", 1.35)
		animated_sprite.material = mat
	set_liturgical_state(&"liturgical_idle")

func _apply_recipe(recipe: Dictionary) -> void:
	if recipe.has("dialetheic_afield"):
		base_afield_potency = float(recipe["dialetheic_afield"])
	if recipe.has("master_texture_path"):
		var tex := load_texture_safe(recipe["master_texture_path"])
		if tex:
			setup_from_texture(tex)
	if animated_sprite and animated_sprite.material:
		var mat := animated_sprite.material as ShaderMaterial
		mat.set_shader_parameter("u_afield_potency", base_afield_potency)

func set_liturgical_state(new_state: StringName) -> void:
	if not animated_sprite or not animated_sprite.sprite_frames or not animated_sprite.sprite_frames.has_animation(new_state):
		return
	var prev := current_liturgical_state
	current_liturgical_state = new_state
	animated_sprite.play(new_state)
	liturgical_state_changed.emit(prev, new_state)

func pulse_dialogue_speech(syllable_stress: float) -> void:
	if not animated_sprite or not animated_sprite.material:
		return
	var speech_boost: float = 1.0 + (syllable_stress * 0.45)
	var mat := animated_sprite.material as ShaderMaterial
	mat.set_shader_parameter("u_lumen_emission_gain", speech_boost)
	dialogue_cadence_pulsed.emit(speech_boost)

func inject_custom_pixel_layer(layer_texture: Texture2D) -> void:
	if not overlay_sprite:
		return
	overlay_sprite.texture = layer_texture
	overlay_sprite.visible = (layer_texture != null)
	overlay_injected.emit(11, layer_texture)
