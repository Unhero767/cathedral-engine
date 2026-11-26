# SanctuaryArvonlae.gd
# [Scene 1] Prime Nave & Central Heart-Oculus: Autopoietic Heartbeat & Vitality Logic
class_name SanctuaryArvonlae extends Node2D

signal sanctuary_vitality_updated(vitality: float)
signal sanctuary_breached(breach_severity: float)

@export var max_vitality: float = 1000.0
var current_vitality: float = 1000.0

@onready var heart_oculus: HeartOculus = $HeartOculus
@onready var player: PlayerSoulframe = $PlayerSoulframe
@onready var hud: HUDTelemetry = $HUDTelemetry

func _ready() -> void:
	print("[SanctuaryArvonlae] Initialized Prime Nave.")
	if AshArchive:
		AshArchive.commit_entry({
			"location": "Sanctuary Arvonlae",
			"event": "PRIME_NAVE_ONLINE",
			"status": "AUTOPOIETIC_RESONANCE"
		}, ["WORLD", "SANCTUARY"])

func _physics_process(delta: float) -> void:
	# Autopoietic Vitality regeneration
	if current_vitality < max_vitality:
		current_vitality = minf(max_vitality, current_vitality + 5.0 * delta)
		emit_signal("sanctuary_vitality_updated", current_vitality)

func damage_sanctuary(amount: float) -> void:
	current_vitality = maxf(0.0, current_vitality - amount)
	emit_signal("sanctuary_vitality_updated", current_vitality)
	if current_vitality <= 0.0:
		emit_signal("sanctuary_breached", amount)
