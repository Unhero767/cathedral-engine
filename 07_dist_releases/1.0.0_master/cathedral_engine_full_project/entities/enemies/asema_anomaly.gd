# AsemaAnomaly.gd
# 4-Phase Anomaly State Machine: Latent (0), Spawning (1), Agitated (2), Supercritical (3)
class_name AsemaAnomaly extends CharacterBody2D

signal phase_transitioned(old_phase: int, new_phase: int)
signal dialetheic_burst_emitted(origin: Vector2, entropy_power: float)
signal anomaly_banished(anomaly_id: String)

enum AnomalyPhase {
	LATENT = 0,       # Subtle spatial ripple, low threat
	SPAWNING = 1,     # Lattice tear, void ingestion
	AGITATED = 2,     # Erratic kinetic lunges, entropy pulses
	SUPERCRITICAL = 3 # Dialetheic burst, singularity pull
}

@export var max_entropy_hp: float = 60.0
@export var base_speed: float = 90.0

var current_hp: float = 60.0
var current_phase: AnomalyPhase = AnomalyPhase.LATENT
var target_player: Node2D = null
var phase_timer: float = 0.0

func _ready() -> void:
	_transition_to_phase(AnomalyPhase.LATENT)

func _physics_process(delta: float) -> void:
	phase_timer += delta
	
	match current_phase:
		AnomalyPhase.LATENT:
			if phase_timer > 3.0:
				_transition_to_phase(AnomalyPhase.SPAWNING)
		AnomalyPhase.SPAWNING:
			if phase_timer > 2.0:
				_transition_to_phase(AnomalyPhase.AGITATED)
		AnomalyPhase.AGITATED:
			_hunt_player(delta)
			if current_hp < max_entropy_hp * 0.3 or phase_timer > 15.0:
				_transition_to_phase(AnomalyPhase.SUPERCRITICAL)
		AnomalyPhase.SUPERCRITICAL:
			_supercritical_pulsing(delta)
			
	move_and_slide()
	queue_redraw()

func _transition_to_phase(new_phase: AnomalyPhase) -> void:
	var prev = current_phase
	current_phase = new_phase
	phase_timer = 0.0
	emit_signal("phase_transitioned", prev, new_phase)

func _hunt_player(delta: float) -> void:
	if not target_player:
		target_player = get_tree().get_first_node_in_group("Player")
	if target_player:
		var dir = (target_player.global_position - global_position).normalized()
		velocity = dir * base_speed
	else:
		velocity = Vector2.ZERO

func _supercritical_pulsing(delta: float) -> void:
	velocity = Vector2.ZERO
	if int(phase_timer * 10) % 20 == 0:
		emit_signal("dialetheic_burst_emitted", global_position, 25.0)
		if AFieldManager:
			AFieldManager.inject_entropy_perturbation(0.8, "AsemaSupercritical")

func apply_damage(damage: float) -> void:
	current_hp -= damage
	if current_hp <= 0.0:
		emit_signal("anomaly_banished", name)
		queue_free()

func _draw() -> void:
	var phase_color = Color(0.541, 0.169, 0.886, 0.8) # Violet Omega
	match current_phase:
		AnomalyPhase.LATENT:
			phase_color = Color(0.2, 0.2, 0.2, 0.4)
			draw_arc(Vector2.ZERO, 10.0, 0, TAU, 16, phase_color, 1.0)
		AnomalyPhase.SPAWNING:
			phase_color = Color(0.863, 0.078, 0.235, 0.6) # Crimson
			draw_circle(Vector2.ZERO, 12.0, phase_color)
		AnomalyPhase.AGITATED:
			phase_color = Color(0.541, 0.169, 0.886, 0.9) # Violet
			draw_circle(Vector2.ZERO, 14.0, phase_color)
			draw_circle(Vector2.ZERO, 6.0, Color(0.05, 0.05, 0.05))
		AnomalyPhase.SUPERCRITICAL:
			phase_color = Color(0.9, 0.1, 0.1, 1.0)
			draw_circle(Vector2.ZERO, 18.0 + sin(phase_timer * 20.0) * 4.0, phase_color)
