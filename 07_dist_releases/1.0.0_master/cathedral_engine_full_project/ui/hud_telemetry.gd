# HUDTelemetry.gd
# In-Game Telemetry: 36-Chamber Oculus Dial, Pneumatic Breath Bar, Tri-Key Icons, K-Index Dial
class_name HUDTelemetry extends CanvasLayer

@onready var breath_bar: ProgressBar = $Control/BottomPanel/BreathBar
@onready var k_index_label: Label = $Control/TopPanel/KIndexLabel
@onready var logic_label: Label = $Control/TopPanel/LogicLabel
@onready var lead_icon: ColorRect = $Control/TriKeyPanel/LeadKeyIcon
@onready var cyan_icon: ColorRect = $Control/TriKeyPanel/CyanKeyIcon
@onready var iron_icon: ColorRect = $Control/TriKeyPanel/IronKeyIcon
@onready var oculus_dial: Control = $Control/OculusDial

var current_k_index: float = 1.2
var breath_val: float = 100.0
var max_breath_val: float = 100.0

func _ready() -> void:
	if TriKeyController:
		TriKeyController.key_state_changed.connect(_on_key_state_changed)
	if AFieldManager:
		AFieldManager.k_index_spiked.connect(_on_k_index_spiked)
	if DialetheicBuffer:
		DialetheicBuffer.logic_state_changed.connect(_on_logic_state_changed)

func _process(_delta: float) -> void:
	if AFieldManager:
		current_k_index = AFieldManager.k_index
		if k_index_label:
			k_index_label.text = "K-INDEX: %.2f" % current_k_index
			if current_k_index >= 7.0:
				k_index_label.modulate = Color(1.0, 0.2, 0.2)
			else:
				k_index_label.modulate = Color(0.0, 0.898, 1.0)
				
	if DialetheicBuffer and logic_label:
		logic_label.text = "LOGIC: " + DialetheicBuffer.get_state_string()
		
	if oculus_dial:
		oculus_dial.queue_redraw()

func _on_key_state_changed(lead: bool, cyan: bool, iron: bool) -> void:
	if lead_icon:
		lead_icon.modulate = Color(0.855, 0.647, 0.125) if lead else Color(0.2, 0.2, 0.2)
	if cyan_icon:
		cyan_icon.modulate = Color(0.0, 0.898, 1.0) if cyan else Color(0.2, 0.2, 0.2)
	if iron_icon:
		iron_icon.modulate = Color(0.863, 0.078, 0.235) if iron else Color(0.2, 0.2, 0.2)

func _on_k_index_spiked(k_val: float, warning: String) -> void:
	current_k_index = k_val

func _on_logic_state_changed(_prev: int, new_val: int) -> void:
	if logic_label:
		logic_label.text = "LOGIC: " + DialetheicBuffer.get_state_string(new_val)

func update_breath(current: float, max_b: float) -> void:
	breath_val = current
	max_breath_val = max_b
	if breath_bar:
		breath_bar.max_value = max_b
		breath_bar.value = current
