extends VBoxContainer
class_name DialetheicMatrixHUD

var title_label: Label
var status_label: Label

func _ready() -> void:
	custom_minimum_size = Vector2(240, 100)
	
	title_label = Label.new()
	title_label.text = "--- DIALETHEIC MATRIX ---"
	title_label.add_theme_color_override("font_color", Color(0.85, 0.65, 0.20, 1.0)) # Gold Joy resonance
	add_child(title_label)

	status_label = Label.new()
	status_label.text = "Status: Awaiting State Telemetry..."
	status_label.add_theme_color_override("font_color", Color(0.9, 0.9, 0.9, 0.9))
	add_child(status_label)

func update_matrix_display(key: String, state_str: String) -> void:
	status_label.text = "Claim [%s]: %s" % [key, state_str]
