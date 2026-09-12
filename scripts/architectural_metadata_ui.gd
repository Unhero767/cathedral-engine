extends Control

@onready var orchestrator = get_node_or_null("../StateOrchestrator")
var telemetry_label: Label = Label.new()

func _ready() -> void:
    set_anchors_preset(Control.PRESET_FULL_RECT)
    mouse_filter = Control.MOUSE_FILTER_IGNORE
    
    # Construct Architectural Wireframe Border Panel
    var frame_panel = PanelContainer.new()
    frame_panel.set_anchors_preset(Control.PRESET_TOP_LEFT)
    frame_panel.offset_left = 40
    frame_panel.offset_top = 40
    frame_panel.offset_right = 380
    frame_panel.offset_bottom = 220
    add_child(frame_panel)
    
    var vbox = VBoxContainer.new()
    frame_panel.add_child(vbox)
    
    var header = Label.new()
    header.text = "SPECTRAL DOMINANCE & COLOR ARCHITECTURE"
    vbox.add_child(header)
    
    telemetry_label.text = "SUBSTRATE: BRONZE-OBSIDIAN NULL\nSTATUS: MONITORING VECTORS"
    vbox.add_child(telemetry_label)
    
    if orchestrator:
        orchestrator.connect("state_changed", Callable(self, "_on_system_state_changed"))

func _on_system_state_changed(new_state: int) -> void:
    if orchestrator:
        for state_name in orchestrator.SystemState.keys():
            if orchestrator.SystemState[state_name] == new_state:
                telemetry_label.text = "SUBSTRATE: ACTIVE RESONANCE\nSTATE VECTOR: " + state_name
                break
