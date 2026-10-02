extends CanvasLayer

@onready var orchestrator = get_node_or_null("../StateOrchestrator")
@onready var status_label: Label = Label.new()

func _ready() -> void:
    layer = 129
    
    var panel = PanelContainer.new()
    panel.set_anchors_preset(Control.PRESET_TOP_RIGHT)
    panel.offset_left = -220
    panel.offset_top = 20
    panel.offset_right = -20
    panel.offset_bottom = 260
    add_child(panel)
    
    var vbox = VBoxContainer.new()
    panel.add_child(vbox)
    
    var title = Label.new()
    title.text = "STATE ORCHESTRATOR Ω"
    vbox.add_child(title)
    
    status_label.text = "Current State: IDLE"
    vbox.add_child(status_label)
    
    if orchestrator:
        orchestrator.connect("state_changed", Callable(self, "_on_state_changed"))
        
        for state_name in orchestrator.SystemState.keys():
            var btn = Button.new()
            btn.text = state_name
            var state_val = orchestrator.SystemState[state_name]
            btn.pressed.connect(func(): orchestrator.transition_to(state_val))
            vbox.add_child(btn)

func _on_state_changed(new_state: int) -> void:
    if orchestrator:
        for k in orchestrator.SystemState.keys():
            if orchestrator.SystemState[k] == new_state:
                status_label.text = "Current State: " + k
                break
