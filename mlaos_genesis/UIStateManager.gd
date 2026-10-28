extends Node
class_name UIStateManager

var active_interface: CanvasLayer = null

func transition_to(new_interface: CanvasLayer) -> void:
    if active_interface != null:
        active_interface.visible = false
    active_interface = new_interface
    active_interface.visible = true
