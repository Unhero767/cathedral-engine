class_name DPT64Controller
extends Node

signal state_updated

var player_hp = 100
var caloric_buffer = 100.0
var stats = {"STR": 14, "DEX": 12, "CON": 13, "INT": 15}
var harmonic_scars = 0
var current_torch = 580

func _unhandled_input(event: InputEvent):
    var moved = false
    if event.is_action_pressed("ui_up") or Input.is_key_pressed(KEY_W):
        moved = true
    elif event.is_action_pressed("ui_down") or Input.is_key_pressed(KEY_S):
        moved = true
    elif event.is_action_pressed("ui_left") or Input.is_key_pressed(KEY_A):
        moved = true
    elif event.is_action_pressed("ui_right") or Input.is_key_pressed(KEY_D):
        moved = true
        
    if moved:
        somatic_tick()

func somatic_tick():
    caloric_buffer -= 0.5
    if caloric_buffer <= 0.0:
        player_hp -= 2
        harmonic_scars += 1
    emit_signal("state_updated")
