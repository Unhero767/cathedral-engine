extends Node

func _ready() -> void:
	var buffer = DialetheicBuffer.new()
	buffer.insert_claim("system_active", true, false)
	print("State 'system_active': ", buffer.evaluate_state("system_active"))
