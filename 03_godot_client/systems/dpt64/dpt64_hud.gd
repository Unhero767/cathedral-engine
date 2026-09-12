extends Control

@onready var hp_label = $VBoxContainer/HPLabel
@onready var caloric_label = $VBoxContainer/CaloricLabel
@onready var stats_label = $VBoxContainer/StatsLabel
@onready var controller = get_node("/root/DPT64Main/Controller")

func _ready():
    if controller:
        controller.connect("state_updated", Callable(self, "_on_state_updated"))
        _on_state_updated()

func _on_state_updated():
    hp_label.text = "Somatic Integrity: %d" % controller.player_hp
    caloric_label.text = "Caloric Buffer: %.1f%%" % controller.caloric_buffer
    stats_label.text = "STR: %d | DEX: %d | CON: %d | INT: %d | Scars: %d" % [
        controller.stats["STR"], controller.stats["DEX"],
        controller.stats["CON"], controller.stats["INT"],
        controller.harmonic_scars
    ]
