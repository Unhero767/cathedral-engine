extends Node
# Freya: Error Handler & Dialetheic Collision Interceptor

func _ready() -> void:
	SovereignInterface.dialetheic_fracture_detected.connect(_on_fracture_detected)
	print("[Freya] Feral Protector daemon online.")

func _on_fracture_detected(error_code: String, details: Dictionary) -> void:
	push_error("[Freya] Intercepted Dialetheic Fracture [%s]: %s" % [error_code, details])
	_crystallize_harmonic_scar(error_code, details)

func _crystallize_harmonic_scar(code: String, details: Dictionary) -> void:
	print("[Freya] Applying Metamorphic Squeeze. Error [%s] petrified into Harmonic Scar." % code)
