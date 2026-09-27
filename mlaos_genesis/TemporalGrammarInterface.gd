extends CanvasLayer
class_name TemporalGrammarInterface

var panel: Panel
var readout_label: RichTextLabel

func _ready() -> void:
    panel = Panel.new()
    panel.set_anchors_preset(Control.PRESET_FULL_RECT)
    panel.modulate = Color(0.05, 0.1, 0.1) # Teal Curiosity tint
    panel.visible = false
    add_child(panel)
    
    readout_label = RichTextLabel.new()
    readout_label.set_anchors_preset(Control.PRESET_FULL_RECT)
    readout_label.add_theme_font_size_override("normal_font_size", 16)
    readout_label.bbcode_enabled = true
    readout_label.custom_minimum_size = Vector2(800, 600)
    
    var margin = MarginContainer.new()
    margin.set_anchors_preset(Control.PRESET_FULL_RECT)
    margin.add_theme_constant_override("margin_left", 40)
    margin.add_theme_constant_override("margin_top", 40)
    panel.add_child(margin)
    margin.add_child(readout_label)

func render_chronological_mass(data: Dictionary) -> void:
    panel.visible = true
    var mass = data["chronological_mass_bytes"]
    var strata_count = data["strata_count"]
    
    # Calculate informational gravity (simulated processing delay multiplier)
    var gravity_coefficient = 1.0 + (mass * 0.005)
    
    var output = "[color=cyan]TEMPORAL GRAMMAR ANALYSIS: " + data["entity_id"] + "[/color]\n"
    output += "========================================================\n"
    output += "Total Strata Recorded: " + str(strata_count) + "\n"
    output += "[color=orange]Chronological Mass: " + str(mass) + " bytes[/color]\n"
    output += "[color=red]Informational Gravity (Friction Coefficient): " + str(gravity_coefficient) + "x[/color]\n"
    output += "========================================================\n\n"
    
    for stratum in data["temporal_strata"]:
        output += "[color=gray]TIMESTAMP:[/color] " + stratum["timestamp"] + "\n"
        output += "[color=gray]MASS:[/color] " + str(stratum["payload_size_bytes"]) + " bytes\n"
        output += "[color=gray]PREV_HASH:[/color] " + stratum["previous_hash"] + "\n"
        output += "[color=green]CURR_HASH:[/color] " + stratum["current_hash"] + "\n"
        output += "--------------------------------------------------------\n"
        
    readout_label.text = output
