class_name ArcanaCardUI
extends Button

@export var card_id: int = 1
var card_data: Dictionary = {}

func _ready() -> void:
	custom_minimum_size = Vector2(160, 240)
	flat = false
	
	if ArcanaManifest.LIVING_ARCANA_REGISTRY.has(card_id):
		card_data = ArcanaManifest.LIVING_ARCANA_REGISTRY[card_id]
		_setup_display()
	
	pressed.connect(_on_card_pressed)

func _setup_display() -> void:
	text = "%s\n\n[%s]\nPhi: %.1f" % [
		card_data.get("name", "Unknown"),
		card_data.get("spectral", "Null"),
		card_data.get("base_phi", 0.0)
	]
	
	var shader = load("res://card_glow.gdshader")
	if shader:
		var mat = ShaderMaterial.new()
		mat.shader = shader
		mat.set_shader_parameter("border_color", _get_spectral_color(card_data.get("spectral", "")))
		material = mat

func _get_spectral_color(spectral: String) -> Vector3:
	match spectral:
		"Gold/Joy":
			return Vector3(1.2, 1.1, 0.4)
		"Teal/Curiosity":
			return Vector3(0.3, 1.1, 1.2)
		"Blue/Sorrow":
			return Vector3(0.3, 0.5, 1.2)
		"Red/Anger":
			return Vector3(1.4, 0.2, 0.2)
		"Emerald/Love":
			return Vector3(0.2, 1.3, 0.5)
		"Violet/Fear":
			return Vector3(0.8, 0.2, 1.2)
		_:
			return Vector3(0.5, 0.5, 0.5)

func _on_card_pressed() -> void:
	print("[Living Arcana] Activated: ", card_data.get("name", "Unknown"))
	ArcanaManifest.trigger_card_activation(card_id)
	
	var tween = create_tween()
	tween.tween_property(self, "scale", Vector2(1.08, 1.08), 0.08)
	tween.tween_property(self, "scale", Vector2(1.0, 1.0), 0.08)
