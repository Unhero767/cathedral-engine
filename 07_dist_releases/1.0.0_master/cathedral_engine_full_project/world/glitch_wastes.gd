# GlitchWastes.gd
# High-Entropy Non-Euclidean Frontier Zone & Procedural Anomaly Wave Spawner
class_name GlitchWastes extends Node2D

signal wave_spawned(wave_number: int, anomaly_count: int)
signal non_euclidean_warp(warp_vector: Vector2)

@export var wave_interval: float = 12.0
@export var spawn_radius: float = 450.0

var wave_timer: float = 0.0
var current_wave: int = 0
var active_anomalies: Array = []

func _physics_process(delta: float) -> void:
	wave_timer += delta
	if wave_timer >= wave_interval:
		wave_timer = 0.0
		spawn_next_wave()

func spawn_next_wave() -> void:
	current_wave += 1
	var count = 3 + current_wave * 2
	emit_signal("wave_spawned", current_wave, count)
	
	if AFieldManager:
		AFieldManager.inject_entropy_perturbation(0.4 * float(current_wave), "GlitchWastesWave")
		
	for i in range(count):
		var angle = randf() * TAU
		var spawn_pos = Vector2(640, 360) + Vector2(cos(angle), sin(angle)) * spawn_radius
		_spawn_anomaly_at(spawn_pos)

func _spawn_anomaly_at(pos: Vector2) -> void:
	var anomaly_scene = load("res://entities/enemies/asema_anomaly.tscn")
	if anomaly_scene:
		var instance = anomaly_scene.instantiate()
		instance.position = pos
		add_child(instance)
		active_anomalies.append(instance)
