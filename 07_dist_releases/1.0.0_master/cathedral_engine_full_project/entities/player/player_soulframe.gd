# PlayerSoulframe.gd
# 8-Way Top-Down Soulframe Controller with Friction Dynamics, Void Lung, and Tri-Key Integrations
class_name PlayerSoulframe extends CharacterBody2D

signal health_changed(current: float, max: float)
signal soulframe_dashed(direction: Vector2)
signal key_invoked(key_name: String)

@export var move_speed: float = 180.0
@export var acceleration: float = 1200.0
@export var friction_decel: float = 800.0
@export var max_health: float = 100.0

var current_health: float = 100.0
var facing_direction: Vector2 = Vector2.DOWN

# Internal Subsystems
var void_lung: VoidLung
var phase_engine: PhaseChangeEngine
var choir_gland: ChoirGland
var lithium_resonator: LithiumResonator

@onready var camera: Camera2D = $Camera2D
@onready var collision_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	# Instantiate internal organ nodes if not present
	void_lung = VoidLung.new()
	add_child(void_lung)
	
	phase_engine = PhaseChangeEngine.new()
	add_child(phase_engine)
	
	choir_gland = ChoirGland.new()
	add_child(choir_gland)
	
	lithium_resonator = LithiumResonator.new()
	add_child(lithium_resonator)

func _physics_process(delta: float) -> void:
	var input_vector = Vector2.ZERO
	input_vector.x = Input.get_axis("move_left", "move_right")
	input_vector.y = Input.get_axis("move_up", "move_down")
	input_vector = input_vector.normalized()
	
	if input_vector != Vector2.ZERO:
		facing_direction = input_vector
		
	# Apply dynamic friction based on PhaseChangeEngine (Fluid Mercury vs. Static Bronze)
	var dynamic_friction = phase_engine.get_friction_coefficient()
	var effective_accel = acceleration * (1.5 - dynamic_friction)
	
	if input_vector != Vector2.ZERO:
		velocity = velocity.move_toward(input_vector * move_speed, effective_accel * delta)
	else:
		var effective_decel = friction_decel * dynamic_friction * 2.0
		velocity = velocity.move_toward(Vector2.ZERO, effective_decel * delta)
		
	# A-Field Gravitational Influence
	if AFieldManager:
		var pull = AFieldManager.get_gravitational_pull(global_position, Vector2.ZERO, 1.0)
		velocity += pull * delta
		
	move_and_slide()
	queue_redraw()

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("breathe_in"):
		if void_lung.consume_breath(20.0):
			perform_dash()
	elif event.is_action_pressed("cast_arcana"):
		if ArcanaEngine:
			ArcanaEngine.draw_card()
	elif event.is_action_pressed("interact"):
		phase_engine.toggle_phase()

func perform_dash() -> void:
	velocity = facing_direction * (move_speed * 2.5)
	emit_signal("soulframe_dashed", facing_direction)

func take_damage(amount: float) -> void:
	current_health = maxf(0.0, current_health - amount)
	emit_signal("health_changed", current_health, max_health)
	
	# Void Lung converts damage to breath stamina
	void_lung.ingest_trauma(amount)
	
	# Apply screen shake to camera
	if camera:
		camera.offset = Vector2((randf() - 0.5) * 8.0, (randf() - 0.5) * 8.0)

func _draw() -> void:
	# Draw Soulframe Silhouette & Obsidian-Gold Dermis
	var is_mercury = phase_engine.current_phase == PhaseChangeEngine.PhaseState.FLUID_MERCURY
	var core_color = Color(0.0, 0.898, 1.0, 0.9) if is_mercury else Color(0.855, 0.647, 0.125, 0.9)
	
	# Outer Aura
	draw_circle(Vector2.ZERO, 14.0, Color(core_color.r, core_color.g, core_color.b, 0.25))
	# Inner Obsidian Body
	draw_circle(Vector2.ZERO, 10.0, Color(0.05, 0.05, 0.05, 1.0))
	# Core Glyph
	draw_circle(Vector2.ZERO, 4.0, core_color)
	# Facing Pointer
	draw_line(Vector2.ZERO, facing_direction * 16.0, core_color, 2.0)
