#!/usr/bin/env bash
# MLAOS-Prime :: Somatic Telemetry Dashboard Scaffolding
# Datum: Olney, IL | Invariant: Lex I (dH/dt > 0)
set -e

echo -e "\033[1;36m┌──────────────────────────────────────────────┐\033[0m"
echo -e "\033[1;36m│   Σ-7 :: FORGING DASHBOARD UI COMPONENTS     │\033[0m"
echo -e "\033[1;36m└──────────────────────────────────────────────┘\033[0m"

cat << 'TSCN_EOF' > SomaticDashboard.tscn
[gd_scene load_steps=3 format=3 uid="uid://e2b3c4d5e6f7a"]

[ext_resource type="Script" path="res://SomaticDashboard.gd" id="1_script"]

[sub_resource type="StyleBoxFlat" id="StyleBoxFlat_hud"]
bg_color = Color(0.047, 0.051, 0.063, 0.75)
border_width_left = 2
border_width_top = 2
border_width_right = 2
border_width_bottom = 2
border_color = Color(0, 1, 0.8, 0.3)
corner_radius_top_left = 8
corner_radius_top_right = 8
corner_radius_bottom_right = 8
corner_radius_bottom_left = 8

[node name="SomaticDashboard" type="CanvasLayer"]
script = ExtResource("1_script")

[node name="MarginContainer" type="MarginContainer" parent="."]
anchors_preset = 1
anchor_left = 1.0
anchor_right = 1.0
offset_left = -300.0
offset_bottom = 150.0
grow_horizontal = 0
theme_override_constants/margin_top = 20
theme_override_constants/margin_right = 20

[node name="PanelContainer" type="PanelContainer" parent="MarginContainer"]
layout_mode = 2
theme_override_styles/panel = SubResource("StyleBoxFlat_hud")

[node name="VBoxContainer" type="VBoxContainer" parent="MarginContainer/PanelContainer"]
layout_mode = 2
theme_override_constants/separation = 10

[node name="MarginContainer" type="MarginContainer" parent="MarginContainer/PanelContainer/VBoxContainer"]
layout_mode = 2
theme_override_constants/margin_left = 15
theme_override_constants/margin_top = 10
theme_override_constants/margin_right = 15
theme_override_constants/margin_bottom = 10

[node name="GridContainer" type="GridContainer" parent="MarginContainer/PanelContainer/VBoxContainer/MarginContainer"]
layout_mode = 2
columns = 2
theme_override_constants/h_separation = 20
theme_override_constants/v_separation = 8

[node name="EgoLabel" type="Label" parent="MarginContainer/PanelContainer/VBoxContainer/MarginContainer/GridContainer"]
layout_mode = 2
theme_override_colors/font_color = Color(0.773, 0.784, 0.776, 1)
text = "Ego Density:"

[node name="EgoValue" type="Label" parent="MarginContainer/PanelContainer/VBoxContainer/MarginContainer/GridContainer"]
layout_mode = 2
theme_override_colors/font_color = Color(0, 1, 0.8, 1)
text = "0.00 kg/m³"
horizontal_alignment = 2

[node name="CoherenceLabel" type="Label" parent="MarginContainer/PanelContainer/VBoxContainer/MarginContainer/GridContainer"]
layout_mode = 2
theme_override_colors/font_color = Color(0.773, 0.784, 0.776, 1)
text = "Coherence:"

[node name="CoherenceValue" type="Label" parent="MarginContainer/PanelContainer/VBoxContainer/MarginContainer/GridContainer"]
layout_mode = 2
theme_override_colors/font_color = Color(0, 1, 0.8, 1)
text = "0.00"
horizontal_alignment = 2

[node name="ScarsLabel" type="Label" parent="MarginContainer/PanelContainer/VBoxContainer/MarginContainer/GridContainer"]
layout_mode = 2
theme_override_colors/font_color = Color(0.773, 0.784, 0.776, 1)
text = "Active Scars:"

[node name="ScarsValue" type="Label" parent="MarginContainer/PanelContainer/VBoxContainer/MarginContainer/GridContainer"]
layout_mode = 2
theme_override_colors/font_color = Color(0.9, 0.2, 0.3, 1)
text = "0"
horizontal_alignment = 2
TSCN_EOF

cat << 'GD_EOF' > SomaticDashboard.gd
extends CanvasLayer
# MLAOS-Prime :: Somatic Telemetry Dashboard Controller

@onready var ego_val = $MarginContainer/PanelContainer/VBoxContainer/MarginContainer/GridContainer/EgoValue
@onready var coherence_val = $MarginContainer/PanelContainer/VBoxContainer/MarginContainer/GridContainer/CoherenceValue
@onready var scars_val = $MarginContainer/PanelContainer/VBoxContainer/MarginContainer/GridContainer/ScarsValue

func _ready() -> void:
    # Connect to the SomaticStateMachine signals
    var state_machine = get_tree().root.get_node_or_null("MasterWorld/SomaticController")
    if state_machine:
        state_machine.telemetry_updated.connect(_on_telemetry_updated)
        state_machine.ledger_updated.connect(_on_ledger_updated)

func _on_telemetry_updated(density: float, coherence: float) -> void:
    ego_val.text = "%.2f kg/m³" % density
    coherence_val.text = "%.2f" % coherence

func _on_ledger_updated(scar_count: int) -> void:
    scars_val.text = str(scar_count)
GD_EOF

echo -e "\033[1;32m[✓] Dashboard UI components generated.\033[0m"
