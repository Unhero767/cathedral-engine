class_name CathedralDialogueDriver
extends Node

signal dialogue_started
signal dialogue_finished

func trigger_dialogue(text: String) -> void:
	emit_signal("dialogue_started")
	# Dialogue pipeline execution stub
	emit_signal("dialogue_finished")
