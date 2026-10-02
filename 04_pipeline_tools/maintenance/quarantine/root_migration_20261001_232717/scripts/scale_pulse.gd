extends Control

@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var speed_slider: Slider = $SpeedSlider
@onready var target_node: Control = $TargetNode
@onready var toggle_button: Button = $ToggleButton

func _ready() -> void:
    if target_node is Control:
        target_node.pivot_offset = target_node.size / 2.0
    if toggle_button and not toggle_button.pressed.is_connected(_on_toggle_button_pressed):
        toggle_button.pressed.connect(_on_toggle_button_pressed)
    if speed_slider and not speed_slider.value_changed.is_connected(_on_speed_slider_value_changed):
        speed_slider.value_changed.connect(_on_speed_slider_value_changed)
    animation_player.speed_scale = speed_slider.value
    animation_player.play("pulse")

func _on_toggle_button_pressed() -> void:
    if animation_player.is_playing():
        animation_player.stop()
    else:
        animation_player.play("pulse")

func _on_speed_slider_value_changed(value: float) -> void:
    animation_player.speed_scale = value
