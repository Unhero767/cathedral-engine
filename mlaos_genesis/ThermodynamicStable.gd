extends CanvasLayer
class_name ThermodynamicStable

var panel: Panel
var stable_readout: RichTextLabel
var bridge: AshArchiveBridge

func _ready() -> void:
    panel = Panel.new()
    panel.set_anchors_preset(Control.PRESET_FULL_RECT)
    panel.modulate = Color(0.1, 0.1, 0.15)
    panel.visible = false
    add_child(panel)
    
    stable_readout = RichTextLabel.new()
    stable_readout.set_anchors_preset(Control.PRESET_FULL_RECT)
    stable_readout.add_theme_font_size_override("normal_font_size", 18)
    stable_readout.bbcode_enabled = true
    
    var margin = MarginContainer.new()
    margin.set_anchors_preset(Control.PRESET_FULL_RECT)
    margin.add_theme_constant_override("margin_left", 40)
    margin.add_theme_constant_override("margin_top", 40)
    panel.add_child(margin)
    margin.add_child(stable_readout)

func bind_bridge(archive_bridge: AshArchiveBridge) -> void:
    bridge = archive_bridge
    bridge.temporal_history_received.connect(self._on_history_received)

func evaluate_guild_transition(entity_id: String, target_guild: String) -> void:
    panel.visible = true
    stable_readout.text = "[color=cyan]INITIATING THERMODYNAMIC CALCULUS FOR: " + entity_id + "[/color]\n"
    stable_readout.text += "TARGET STRATUM: " + target_guild + "\n"
    stable_readout.text += "Querying Ash Archive for Chronological Mass...\n"
    bridge.request_temporal_grammar(entity_id)

func _on_history_received(data: Dictionary) -> void:
    var mass = data["chronological_mass_bytes"]
    var gravity_coefficient = 1.0 + (mass * 0.005)
    
    var base_transition_cost = 5000.0 # Standard base XP cost for Guild entry
    var thermodynamic_cost = base_transition_cost * gravity_coefficient
    
    var output = stable_readout.text
    output += "\n[color=orange]HISTORICAL MASS DETECTED: " + str(mass) + " bytes[/color]\n"
    output += "[color=red]INFORMATIONAL GRAVITY: " + str(gravity_coefficient) + "x[/color]\n"
    output += "--------------------------------------------------------\n"
    output += "[color=green]REQUIRED METABOLIC FORCE (XP): " + str(thermodynamic_cost) + "[/color]\n"
    output += "--------------------------------------------------------\n"
    
    if gravity_coefficient > 5.0:
        output += "[color=red]WARNING: Extreme structural friction detected. Transition highly inefficient.[/color]\n"
        
    stable_readout.text = output
