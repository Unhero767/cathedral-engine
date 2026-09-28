extends Node
class_name ShaderStateBridge

@onready var buffer = DialetheicBuffer.new()

func _ready() -> void:
	# Seed an initial test claim so the buffer has data to evaluate
	buffer.insert_claim("system_active", true, true)

func _process(_delta: float) -> void:
	var state_str = buffer.evaluate_state("system_active")
	print("Current Buffer State: ", state_str)
	
	var state_value = 0.0
	match state_str:
		"True":
			state_value = 1.0
		"False":
			state_value = 2.0
		"Both (Dialetheic / Harmonic Scar)":
			state_value = 3.0
		_:
			state_value = 0.0
			
	RenderingServer.global_shader_parameter_set("global_logic_state", state_value)
