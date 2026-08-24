class_name CathedralDialogueDriver
extends Node

const BridgeScript = preload("res://SomaticToPortraitBridge.gd")
const PortraitScript = preload("res://CathedralAvatarPortrait.gd")

signal phoneme_stressed(token: String, stress: float, gain: float)

@export var bridge: Node
@export var portrait_controller: Node

var is_speaking: bool = false
var queue: Array[Dictionary] = []
var timer: float = 0.0

func _process(delta: float) -> void:
	if is_speaking and not queue.is_empty():
		timer -= delta
		if timer <= 0.0:
			var item: Dictionary = queue.pop_front()
			var stress_val: float = float(item.get("stress", 0.35))
			var gain: float = 1.0 + (stress_val * 0.45)
			if bridge and bridge.has_method("pulse_dialogue"):
				bridge.pulse_dialogue(stress_val)
			phoneme_stressed.emit(item.get("token", ""), stress_val, gain)
			timer = float(item.get("duration", 0.12))
	elif is_speaking and queue.is_empty() and timer <= 0.0:
		is_speaking = false
		if portrait_controller and portrait_controller.has_method("set_liturgical_state"):
			portrait_controller.set_liturgical_state(&"liturgical_idle")

func speak_text_cadence(text: String) -> void:
	is_speaking = true
	queue.clear()
	if portrait_controller and portrait_controller.has_method("set_liturgical_state"):
		portrait_controller.set_liturgical_state(&"penitent_recitation")
	for word in text.split(" ", false):
		var s: float = 0.85 if word.ends_with("!") else 0.45
		queue.append({"token": word, "stress": s, "duration": 0.14})
	timer = 0.0
