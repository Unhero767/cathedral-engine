class_name PlayerAvatar
extends CharacterBody2D

@export var max_speed: float = 110.0
@export var acceleration: float = 800.0
@export var friction: float = 950.0

@onready var sprite: Sprite2D = $Sprite2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

var shader_material: ShaderMaterial
var base_lumen_gain: float = 1.0
var target_lumen_gain: float = 1.0
var resonance_active: bool = false
var resonance_timer: float = 0.0

func _ready() -> void:
	add_to_group(&"player")
	if sprite and sprite.texture == null:
		var raw_path := "res://assets/textures/player_128.png"
		if FileAccess.file_exists(raw_path):
			var img := Image.load_from_file(raw_path)
			sprite.texture = ImageTexture.create_from_image(img)
			
	if sprite and sprite.material is ShaderMaterial:
		shader_material = sprite.material as ShaderMaterial

func _physics_process(delta: float) -> void:
	_handle_movement(delta)
	_handle_lumen_dynamics(delta)

func _handle_movement(delta: float) -> void:
	var input_vector := Input.get_vector("move_left", "move_right", "move_up", "move_down")
	if input_vector != Vector2.ZERO:
		velocity = velocity.move_toward(input_vector * max_speed, acceleration * delta)
		if input_vector.x < -0.1:
			sprite.flip_h = true
		elif input_vector.x > 0.1:
			sprite.flip_h = false
	else:
		velocity = velocity.move_toward(Vector2.ZERO, friction * delta)
	move_and_slide()

func _handle_lumen_dynamics(delta: float) -> void:
	if not shader_material:
		return
	if resonance_active:
		resonance_timer += delta
		var pulse := 0.5 + 0.5 * sin(2.0 * PI * 1.5 * resonance_timer)
		target_lumen_gain = lerp(1.2, 3.8, pulse)
	else:
		target_lumen_gain = base_lumen_gain

	var current_gain: float = shader_material.get_shader_parameter("u_lumen_emission_gain")
	var smoothed_gain: float = lerp(current_gain, target_lumen_gain, 12.0 * delta)
	shader_material.set_shader_parameter("u_lumen_emission_gain", smoothed_gain)

func trigger_altar_resonance(active: bool) -> void:
	resonance_active = active
	if not active:
		resonance_timer = 0.0
